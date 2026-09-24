"""AWS HTTP API and asynchronous worker; public assets live behind CloudFront.

Jobs expire after one day. Complete answers are reused for identical questions for up
to seven days (S3 lifecycle), keyed by the normalized idea, prompt version and library. Conditional concurrency slots and a daily quota bound the
public deployment. Only explicitly submitted feedback is logged; ideas, answer
bodies and provider errors are not logged.
"""
import base64
import hashlib
import json
import os
import re
import time
import uuid


_fingerprint = None


def cache_key(idea, mode):
    """Same idea text, answer mode, pipeline version and research library → same answer."""
    global _fingerprint
    import knowledge_corpus
    from research_answer import PROMPT_VERSION
    if _fingerprint is None:
        _fingerprint = knowledge_corpus.load('local')['fingerprint']
    normalized = ' '.join(idea.split()).casefold()
    return 'cache/'+hashlib.sha256(json.dumps([PROMPT_VERSION, _fingerprint, mode, normalized]).encode()).hexdigest()+'.json'


def reusable(result):
    """Cache only complete, checked designs; failures and requests for detail are retried."""
    return (result.get('coverage', {}).get('search_complete') and result.get('judgments')
            and result.get('writer', {}).get('status') == 'success' and result.get('execution', {}).get('status') == 'complete')


def log_outcome(identifier, result, seconds):
    """Operational metrics only: no idea text, evidence or model output is logged."""
    rows = {r['provider']: r for r in result.get('comparison', {}).get('rows', [])}
    print(json.dumps({'event': 'answer_outcome', 'job_id': identifier, 'seconds': seconds,
        'status': 'needs_detail' if result.get('needs_detail') else 'design' if reusable(result) else
                  'writer_'+result.get('writer', {}).get('status', 'not_run') if result.get('judgments') else 'no_assessment',
        'search_complete': bool(result.get('coverage', {}).get('search_complete')),
        'execution': result.get('execution', {}).get('status', 'not_run'),
        'citations_removed': result.get('writer', {}).get('citations_removed'),
        'glm_requests': result.get('writer', {}).get('requests', 1 if 'glm' in rows else 0),
        'jev_tokens': rows.get('jev', {}).get('tokens', {}).get('total_tokens'),
        'glm_tokens': rows.get('glm', {}).get('tokens', {}).get('total_tokens'),
        'usd': result.get('comparison', {}).get('total_estimated_usd')}), flush=True)


def clients():
    import boto3
    return boto3.client('dynamodb'), boto3.client('s3'), boto3.client('lambda')


def item(**values):
    return {key: {'N': str(value)} if isinstance(value, int) else {'S': value}
            for key, value in values.items()}


def reply(code, body, retry_after=None):
    return {'statusCode': code, 'headers': {'content-type': 'application/json',
            'cache-control': 'no-store', 'x-content-type-options': 'nosniff',
            **({'retry-after': str(retry_after)} if retry_after is not None else {})},
            'body': json.dumps(body)}


def parse_request(event):
    body = event.get('body') or ''
    if event.get('isBase64Encoded'):
        body = base64.b64decode(body, validate=True).decode()
    if len(body.encode()) > 30000:
        raise ValueError('Request too large.')
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError('Expected a JSON object.')
    idea, mode = data.get('idea'), data.get('mode', 'evidence')
    if not isinstance(idea, str) or not 3 <= len(idea.strip()) <= 6000:
        raise ValueError('Enter an idea of 3 to 6000 characters.')
    if mode not in ('evidence', 'written') or data.get('source', 'local') != 'local':
        raise ValueError('Select a supported mode and the deployed research library.')
    return idea.strip(), mode


def parse_feedback(event):
    body = event.get('body') or ''
    if event.get('isBase64Encoded'):
        body = base64.b64decode(body, validate=True).decode()
    if len(body.encode()) > 12000:
        raise ValueError('Feedback too large.')
    data = json.loads(body)
    if not isinstance(data, dict) or set(data) not in ({'job_id', 'rating'}, {'job_id', 'comment'}):
        raise ValueError('Send a rating or comment.')
    identifier = data['job_id']
    if not isinstance(identifier, str) or not re.fullmatch('[a-f0-9]{32}', identifier):
        raise ValueError('Invalid answer ID.')
    field = 'rating' if 'rating' in data else 'comment'
    value = data[field]
    if not isinstance(value, str):
        raise ValueError('Invalid feedback.')
    value = value.strip()
    if field == 'rating' and value not in ('up', 'down'):
        raise ValueError('Choose thumbs up or down.')
    if field == 'comment' and not 1 <= len(value) <= 2000:
        raise ValueError('Enter 1 to 2,000 characters.')
    return identifier, field, value


def accept_feedback(event):
    if event.get('headers', {}).get('content-type', '').split(';')[0] != 'application/json':
        return reply(415, {'error': 'Expected JSON.'})
    try:
        identifier, field, value = parse_feedback(event)
    except (ValueError, TypeError, UnicodeError):
        return reply(400, {'error': 'Send thumbs up/down or a comment of 1 to 2,000 characters.'})
    db, _, _ = clients()
    now = int(time.time())
    key = item(pk='job#'+identifier)
    job = db.get_item(TableName=os.environ['TABLE'], Key=key, ConsistentRead=True).get('Item', {})
    if int(job.get('ttl', {}).get('N', '0')) <= now or job.get('status', {}).get('S') != 'complete':
        return reply(404, {'error': 'This answer has expired or is not ready for feedback.'})
    # One rating and one comment per completed answer. Retries are idempotent;
    # arbitrary IDs and repeated submissions cannot fill the feedback logs.
    try:
        db.update_item(TableName=os.environ['TABLE'], Key=key,
            UpdateExpression='SET #feedback = :value',
            ConditionExpression='attribute_not_exists(#feedback) AND #status = :complete AND #ttl > :now',
            ExpressionAttributeNames={'#feedback': 'feedback_'+field, '#status': 'status', '#ttl': 'ttl'},
            ExpressionAttributeValues=item(**{':value': value, ':complete': 'complete', ':now': now}))
    except db.exceptions.ConditionalCheckFailedException:
        current = db.get_item(TableName=os.environ['TABLE'], Key=key, ConsistentRead=True).get('Item', {})
        if current.get('feedback_'+field, {}).get('S') == value:
            return reply(200, {'saved': True})
        return reply(409, {'error': 'Feedback already submitted for this answer.'})
    print(json.dumps({'event': 'answer_feedback', 'job_id': identifier,
                      'submitted_at': now, field: value}, ensure_ascii=True), flush=True)
    return reply(200, {'saved': True})


def release(db, identifier, slot='lock'):
    try:
        db.delete_item(TableName=os.environ['TABLE'], Key=item(pk=slot),
                       ConditionExpression='#owner = :id', ExpressionAttributeNames={'#owner': 'owner'},
                       ExpressionAttributeValues=item(**{':id': identifier}))
    except db.exceptions.ConditionalCheckFailedException:
        pass


def claim_job(db, table, identifier, now):
    limit = int(os.environ.get('DAILY_LIMIT', '50'))
    slots = int(os.environ.get('MAX_CONCURRENT', '1'))
    if not 1 <= limit <= 100000 or not 1 <= slots <= 50:
        raise ValueError('Invalid deployment capacity.')
    day = 'day#'+time.strftime('%Y-%m-%d', time.gmtime(now))
    resets_at = (now // 86400 + 1) * 86400
    for index in range(slots):
        slot = 'lock' if index == 0 else f'lock#{index}'
        for attempt in range(2):
            try:
                db.transact_write_items(ClientRequestToken=f'{identifier[:28]}-{index}-{attempt}', TransactItems=[
                    {'Put': {'TableName': table, 'Item': item(pk=slot, owner=identifier, lease=now+960, ttl=now+960),
                             'ConditionExpression': 'attribute_not_exists(pk) OR lease < :now',
                             'ExpressionAttributeValues': item(**{':now': now})}},
                    {'Update': {'TableName': table, 'Key': item(pk=day),
                                'UpdateExpression': 'SET #ttl = :ttl ADD used :one',
                                'ConditionExpression': 'attribute_not_exists(used) OR used < :limit',
                                'ExpressionAttributeNames': {'#ttl': 'ttl'},
                                'ExpressionAttributeValues': item(**{':ttl': now+172800, ':one': 1, ':limit': limit})}},
                    {'Put': {'TableName': table, 'Item': item(pk='job#'+identifier, slot=slot, status='running', created=now,
                                deadline=now+960, ttl=now+86400, progress=json.dumps({'stage': 'Starting research evaluation'})),
                             'ConditionExpression': 'attribute_not_exists(pk)'}}])
                return slot, None
            except db.exceptions.TransactionCanceledException:
                # Cancellation means no quota increment or job/slot write committed.
                # Read actual conditions instead of treating every DB failure as busy.
                quota = db.get_item(TableName=table, Key=item(pk=day), ConsistentRead=True).get('Item', {})
                if int(quota.get('used', {}).get('N', '0')) >= limit:
                    return None, reply(429, {'code': 'daily_limit',
                        'error': 'The site’s daily answer limit has been reached. It resets at 00:00 UTC.',
                        'limit': limit, 'resets_at': resets_at}, resets_at-now)
                lease = db.get_item(TableName=table, Key=item(pk=slot), ConsistentRead=True).get('Item', {})
                if int(lease.get('lease', {}).get('N', '0')) >= now:
                    break  # Try the next independently leased slot.
                if attempt == 0:
                    time.sleep(.05)  # A brief transaction conflict can clear.
                else:
                    return None, reply(503, {'code': 'capacity_check_failed',
                        'error': 'Could not start this answer. Please try again shortly.'}, 2)
    return None, reply(429, {'code': 'busy',
        'error': 'All answer slots are busy. Please try again in a few seconds.',
        'simultaneous_limit': slots}, 5)


def update(db, identifier, **values):
    names = {f'#k{n}': key for n, key in enumerate(values)}
    vals = item(**{f':v{n}': value for n, value in enumerate(values.values())})
    db.update_item(TableName=os.environ['TABLE'], Key=item(pk='job#'+identifier),
                   UpdateExpression='SET '+', '.join(f'#k{n} = :v{n}' for n in range(len(values))),
                   ExpressionAttributeNames=names, ExpressionAttributeValues=vals)


def api(event, context):
    try:
        return api_request(event, context)
    except Exception:
        return reply(503, {'error': 'Hosting service temporarily unavailable. Try again shortly.'})


def api_request(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('rawPath', '')
    if method == 'GET' and path == '/api/config':
        return reply(200, {'jev_available': os.environ.get('JEV_AVAILABLE') == 'true',
                          'writer_available': os.environ.get('WRITER_AVAILABLE') == 'true',
                          'writer_model': 'glm-5.3', 's3_available': False,
                          'hosted': True, 'access_required': False})
    if method == 'POST' and path == '/api/feedback':
        return accept_feedback(event)
    if method == 'POST' and path == '/api/jobs':
        if event.get('headers', {}).get('content-type', '').split(';')[0] != 'application/json':
            return reply(415, {'error': 'Expected JSON.'})
        try:
            idea, mode = parse_request(event)
        except (ValueError, TypeError, UnicodeError):
            return reply(400, {'error': 'Enter an idea of 3 to 6000 characters and select a supported mode.'})
        if mode == 'written' and os.environ.get('WRITER_AVAILABLE') != 'true':
            return reply(400, {'error': 'Answers are temporarily unavailable. Please try again later.'})
        db, s3, functions = clients()
        now = int(time.time())
        identifier = uuid.uuid4().hex
        table = os.environ['TABLE']
        key = cache_key(idea, mode)
        try:
            s3.head_object(Bucket=os.environ['BUCKET'], Key=key)
            hit = True
        except Exception:
            hit = False  # Missing, expired or unreadable: compute a fresh answer.
        if hit:
            # A reused answer makes no model calls, so it uses no quota or answer slot.
            db.put_item(TableName=table, Item=item(pk='job#'+identifier, status='complete', created=now, ttl=now+86400,
                        deadline=now, progress=json.dumps({'stage': 'Reused answer'}), result_key=key))
            print(json.dumps({'event': 'answer_reused', 'job_id': identifier}), flush=True)
            return reply(202, {'id': identifier})
        slot, rejected = claim_job(db, table, identifier, now)
        if rejected:
            return rejected
        try:
            functions.invoke(FunctionName=os.environ['WORKER'], InvocationType='Event',
                             Payload=json.dumps({'id': identifier, 'idea': idea, 'mode': mode, 'slot': slot}).encode())
        except Exception:
            # A transport error can follow an accepted invocation. Preserve the
            # lease and job ID so retrying the page cannot start duplicate work.
            update(db, identifier, progress=json.dumps({'stage': 'Waiting for worker confirmation'}))
        return reply(202, {'id': identifier})
    match = re.fullmatch('/api/jobs/([a-f0-9]{32})', path)
    if method == 'GET' and match:
        db, s3, _ = clients()
        identifier = match[1]
        job = db.get_item(TableName=os.environ['TABLE'], Key=item(pk='job#'+identifier), ConsistentRead=True).get('Item')
        now = int(time.time())
        if not job or int(job['ttl']['N']) < now:
            return reply(404, {'error': 'Answer job not found or expired.'})
        status = job['status']['S']
        if status == 'running' and now > int(job['deadline']['N']):
            return reply(200, {'status': 'failed', 'error': 'Research exceeded the hosting time limit. Please retry.'})
        data = {'status': status, 'created': int(job['created']['N']), 'progress': json.loads(job['progress']['S'])}
        if status == 'complete':
            key = job.get('result_key', {}).get('S') or 'jobs/'+identifier+'.json'
            data['result'] = json.loads(s3.get_object(Bucket=os.environ['BUCKET'], Key=key)['Body'].read())
            if 'result_key' in job:
                data['result']['reused'] = True
        elif status == 'failed':
            data['error'] = job.get('error', {}).get('S', 'Research answer failed.')
        return reply(200, data)
    return reply(404, {'error': 'Not found.'})


def worker(event, context):
    identifier = event.get('id', '')
    slot = event.get('slot', 'lock')  # Compatibility with in-flight pre-upgrade jobs.
    if not re.fullmatch('[a-f0-9]{32}', identifier) or not re.fullmatch(r'lock(?:#[0-9]{1,2})?', slot):
        return
    db, s3, _ = clients()
    # Async delivery can duplicate events even with retries disabled. Claim once.
    try:
        db.update_item(TableName=os.environ['TABLE'], Key=item(pk='job#'+identifier),
                       UpdateExpression='SET started = :yes',
                       ConditionExpression='attribute_not_exists(started) AND #s = :running AND deadline > :now',
                       ExpressionAttributeNames={'#s': 'status'},
                       ExpressionAttributeValues=item(**{':yes': 1, ':running': 'running', ':now': int(time.time())}))
    except db.exceptions.ConditionalCheckFailedException:
        return
    started_at = int(time.time())
    try:
        from research_answer import answer
        def progress(value):
            update(db, identifier, progress=json.dumps(value))
        result = answer(event['idea'], event['mode'], 'local', progress)
        body = json.dumps(result).encode()
        s3.put_object(Bucket=os.environ['BUCKET'], Key='jobs/'+identifier+'.json',
                      Body=body, ContentType='application/json', ServerSideEncryption='AES256')
        update(db, identifier, status='complete')
        log_outcome(identifier, result, int(time.time())-started_at)
        if reusable(result):
            try:
                s3.put_object(Bucket=os.environ['BUCKET'], Key=cache_key(event['idea'], event['mode']),
                              Body=body, ContentType='application/json', ServerSideEncryption='AES256')
            except Exception:
                pass  # The answer is already delivered; a missed cache write only costs a recomputation.
    except Exception:
        update(db, identifier, status='failed', error='Couldn’t complete this answer. Please retry.')
        print(json.dumps({'event': 'answer_outcome', 'job_id': identifier, 'status': 'error',
                          'seconds': int(time.time())-started_at}), flush=True)
    finally:
        release(db, identifier, slot)
