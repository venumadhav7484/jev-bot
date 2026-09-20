"""Read-only Discord bot collector. Capture privately; never publish or call a model.

Optional dependency: discord.py>=2.5,<3. Credentials: discord_bot_token in
.env.local or DISCORD_BOT_TOKEN in the environment. No user-account tokens.
"""
import argparse
import asyncio
import datetime as dt
import json
import os
from pathlib import Path
import re
import uuid

from backup_private import load_env
from jev_triage import dump
from stage_capture import stage

ROOT = Path(__file__).resolve().parents[1]


def serialize(message):
    """Preserve message content separately from reply and embed context."""
    attachments = [a.to_dict() for a in message.attachments]
    embeds = [e.to_dict() for e in message.embeds]
    urls = set(re.findall(r'https?://[^\s<>]+', message.content))
    urls.update(a['url'] for a in attachments)
    urls.update(e['url'] for e in embeds if e.get('url'))
    reference = message.reference
    resolved = getattr(reference, 'resolved', None)
    quote = getattr(resolved, 'content', '')
    return {
        'id': f'chat-messages-{message.channel.id}-{message.id}',
        'text': message.content,
        'links': [{'url': u, 'text': ''} for u in sorted(urls)],
        'format': 'discord_api',
        'reply_context': quote,
        'api_metadata': {
            'author_id': str(message.author.id),
            'created_at': message.created_at.isoformat(),
            'edited_at': message.edited_at.isoformat() if message.edited_at else None,
            'type': message.type.value,
            'attachments': attachments, 'embeds': embeds,
            'reference': reference.to_dict() if reference else None,
            'reply_context_available': bool(quote),
        },
    }


async def capture_history(channel, after_id, before, limit, object_type, save):
    """Library paginates; one extra row detects a bounded run without silent loss."""
    count = 0
    high_water = str(after_id)
    async for message in channel.history(
        after=object_type(id=int(after_id)), before=before,
        oldest_first=True, limit=limit + 1 if limit else None,
    ):
        if count == limit and limit:
            return {'count': count, 'complete': False, 'high_water': high_water}
        if int(message.id) <= int(after_id) or message.created_at >= before:
            raise ValueError('Discord history returned a message outside the requested interval.')
        save(serialize(message))
        count += 1
        high_water = str(message.id)
    return {'count': count, 'complete': True, 'high_water': high_water}


async def collect(client, discord, checkpoint, directory, limit=0, overlap=20):
    app = await client.application_info()
    if not client.user.bot:
        raise ValueError('Only Discord bot credentials are supported.')
    if not (app.flags.gateway_message_content or app.flags.gateway_message_content_limited):
        raise ValueError('Enable Message Content Intent for this bot in the Discord Developer Portal.')
    guild = await client.fetch_guild(int(checkpoint['guild_id']))
    member = await guild.fetch_member(client.user.id)
    channels = await guild.fetch_channels()
    main = next((c for c in channels if str(c.id) == checkpoint['main_channel_id']), None)
    if main is None or not isinstance(main, discord.TextChannel):
        raise ValueError('The saved source must be an accessible text channel.')
    permissions = main.permissions_for(member)
    if not (permissions.view_channel and permissions.read_message_history):
        raise ValueError('Bot needs View Channel and Read Message History on the source channel.')

    cutoff = dt.datetime.now(dt.timezone.utc)
    receipt = {'started_at': cutoff.isoformat(), 'status': 'collecting', 'channels': {},
               'scope': 'Main text channel and its accessible public threads; private threads excluded.',
               'older_edits': f'Only the last {overlap} messages at/before each saved cursor are revisited.',
               'frozen_checkpoint_advanced': False, 'review_checkpoint_advanced': False}
    dump(directory/'receipt.json', receipt)
    rows = {}
    journal = directory/'messages.jsonl'
    def save(row):
        rows[row['id']] = row
        with journal.open('a') as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')

    try:
        threads = {t.id: t for t in await guild.active_threads()
                   if t.parent_id == main.id and not t.is_private()}
        async for thread in main.archived_threads(limit=None):
            threads[thread.id] = thread
        # Known thread IDs must not disappear silently from discovery.
        for tid in checkpoint.get('thread_high_water_message_ids', {}):
            if int(tid) not in threads:
                thread = await client.fetch_channel(int(tid))
                if thread.parent_id != main.id or thread.is_private():
                    raise ValueError('A saved thread is outside the public source channel.')
                threads[thread.id] = thread
        cursors = checkpoint.get('thread_high_water_message_ids', {})
        for channel in [main, *sorted(threads.values(), key=lambda t: t.id)]:
            cursor = checkpoint['capture_high_water_message_id'] if channel.id == main.id else cursors.get(str(channel.id))
            # Unknown threads start from the global capture boundary, not creation time.
            lower = cursor or checkpoint['capture_high_water_message_id']
            if cursor and overlap:
                async for message in channel.history(
                    before=discord.Object(id=int(cursor) + 1), oldest_first=False, limit=overlap,
                ):
                    save(serialize(message))
            result = await capture_history(channel, lower, cutoff, limit if channel.id == main.id else 0,
                                           discord.Object, save)
            receipt['channels'][str(channel.id)] = result
            dump(directory/'receipt.json', receipt)
        document = {'guild_id': checkpoint['guild_id'], 'captured_before': cutoff.isoformat(),
                    'format': 'discord_api', 'messages': list(rows.values())}
        dump(directory/'capture.json', document)
        receipt['status'] = 'captured' if all(c['complete'] for c in receipt['channels'].values()) else 'partial'
        receipt['saved_messages'] = len(rows)
        dump(directory/'receipt.json', receipt)
        return document, receipt
    except Exception as exc:
        # Never print provider response bodies or credentials. Keep partial capture recoverable.
        receipt.update(status='failed', error_type=type(exc).__name__, saved_messages=len(rows))
        dump(directory/'capture.json', {'guild_id': checkpoint['guild_id'], 'messages': list(rows.values())})
        dump(directory/'receipt.json', receipt)
        raise


async def execute(args):
    values = load_env(ROOT/'.env.local')
    token = os.environ.get('DISCORD_BOT_TOKEN') or values.get('discord_bot_token')
    if not token:
        raise ValueError('No bot token configured. Add discord_bot_token to .env.local; keep it out of chat and Git.')
    try:
        import discord
    except ImportError:
        raise ValueError('Install the optional collector dependency: python3 -m pip install -r requirements-discord.txt') from None
    checkpoint = json.loads((ROOT/'resource-pool/sources/collection-checkpoint.json').read_text())
    directory = ROOT/'research/discord-captures'/uuid.uuid4().hex
    async with discord.Client(intents=discord.Intents.none()) as client:
        await client.login(token)
        document, receipt = await collect(client, discord, checkpoint, directory, args.limit, args.overlap)
    if document['messages']:
        receipt['staged_batch'] = stage(document)['batch_id']
        dump(directory/'receipt.json', receipt)
    print(json.dumps({'status': receipt['status'], 'saved_messages': receipt['saved_messages'],
                      'receipt': str(directory/'receipt.json'),
                      'staged_batch': receipt.get('staged_batch'), 'models_called': False}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=0, help='New main-channel messages; 0 means all through run start. Threads are additional.')
    parser.add_argument('--overlap', type=int, default=20, help='Recent messages at/before each saved cursor to check for edits.')
    args = parser.parse_args()
    if args.limit < 0 or args.overlap < 0:
        parser.error('Limits must be nonnegative.')
    try:
        asyncio.run(execute(args))
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    except Exception as exc:
        raise SystemExit(f'Collection stopped ({type(exc).__name__}); check bot access and private capture receipts. No checkpoint advanced.') from None


if __name__ == '__main__':
    main()
