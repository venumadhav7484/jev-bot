"""Import locally saved Discord MHTML pages; no browser, network or model calls.

Canonical IDs come from message timestamp/content nodes, not thread wrappers.
Preserves variants and page overlap; never advances published checkpoints.
"""
import argparse
import datetime as dt
from email import policy
from email.parser import BytesParser
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
BLOCK = {'div','li','p','br','pre','h1','h2','h3','h4','blockquote'}
WRAPPER = re.compile(r'chat-messages-(\d+)-(\d+)')
PARSER_VERSION = 'discord-mhtml-v2'

class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag':'root','attrs':{},'children':[]}
        self.stack = [self.root]
        self.nodes = []
    def handle_starttag(self, tag, attrs):
        n = {'tag':tag,'attrs':dict(attrs),'children':[]}
        self.stack[-1]['children'].append(n)
        self.nodes.append(n)
        if tag not in VOID: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i]['tag']==tag:
                self.stack=self.stack[:i]
                break
    def handle_data(self, text): self.stack[-1]['children'].append(text)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)

def descendants(n):
    for c in n['children']:
        if not isinstance(c,dict) or WRAPPER.fullmatch(c['attrs'].get('id','')): continue
        yield c
        yield from descendants(c)

def raw_content(n):
    chunks=[]
    for c in n['children']:
        if isinstance(c,str): chunks.append(c)
        elif not WRAPPER.fullmatch(c['attrs'].get('id','')):
            if c['tag'] in BLOCK: chunks.append('\n')
            if c['tag']=='img': chunks.append(c['attrs'].get('alt',''))
            chunks.append(raw_content(c))
            if c['tag'] in BLOCK: chunks.append('\n')
    return ''.join(chunks)

def content(n):
    return re.sub(r'\n[ \t]*\n+', '\n', raw_content(n)).strip()

def parse_html(html, archive):
    tree=Tree();tree.feed(html)
    rows=[];issues=[]
    for node in tree.nodes:
        wrapper=node['attrs'].get('id','');match=WRAPPER.fullmatch(wrapper)
        if not match: continue
        kids=list(descendants(node))
        times=[k for k in kids if k['tag']=='time' and re.fullmatch(r'message-timestamp-\d+',k['attrs'].get('id',''))]
        if not times:
            issues.append({'wrapper':wrapper,'issue':'canonical_timestamp_missing'});continue
        time=times[0]['attrs'];mid=time['id'].split('-')[-1]
        bodies=[k for k in kids if k['attrs'].get('id')=='message-content-'+mid]
        if len(bodies)>1:
            issues.append({'wrapper':wrapper,'issue':'multiple_target_bodies'});continue
        body=content(bodies[0]) if bodies else ''
        text=content(node)
        context=[]
        for k in kids:
            if k['attrs'].get('id')=='message-reply-context-'+mid:
                context.append('Quoted reply (another message):\n'+content(k))
            elif k['tag']=='article' and 'embed' in k['attrs'].get('class',''):
                context.append('Link preview (not independently inspected):\n'+content(k))
        links=[{'url':k['attrs']['href'],'text':content(k)} for k in kids if k['tag']=='a' and k['attrs'].get('href','').startswith('http')]
        row={'id':f'chat-messages-{match[1]}-{mid}','wrapper_id':wrapper,'body':body,'text':text,
             'timestamp_utc':time.get('datetime'),'archive':archive,'format':'discord_browser',
             'reply_context':'\n\n'.join(context),
             'links':list({l['url']:l for l in links}.values()),
             'images':[{'tag':k['tag'],'url':k['attrs'].get('src',''),'alt':k['attrs'].get('alt','')} for k in kids if k['tag'] in ('img','video','source') and '/attachments/' in k['attrs'].get('src','')],
             'has_thread':any('threadMessageAccessory' in k['attrs'].get('class','') for k in kids)}
        if mid!=match[2]: issues.append({'wrapper':wrapper,'content_id':mid,'issue':'wrapper_content_difference'})
        rows.append(row)
    return rows,issues

def parse_archive(path):
    rows=[];issues=[]
    for part in BytesParser(policy=policy.default).parsebytes(path.read_bytes()).walk():
        if part.get_content_type()=='text/html':
            r,i=parse_html(part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8',errors='replace'),path.name)
            rows.extend(r);issues.extend(i)
    return rows,issues

def run(directory,checkpoint,cutoff):
    end=dt.datetime.fromisoformat(cutoff.replace('Z','+00:00'))
    rows={};variants={};pages=[]
    cache=directory/'parsed-pages';cache.mkdir(exist_ok=True,mode=0o700)
    for path in sorted((directory/'pages').glob('*.mhtml'),key=lambda p:p.stat().st_mtime_ns):
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        cache_file=cache/(path.stem+'-'+PARSER_VERSION+'-'+sha+'.json')
        if cache_file.exists():
            parsed=json.loads(cache_file.read_text());captured,issues=parsed['rows'],parsed['issues']
        else:
            captured,issues=parse_archive(path)
            cache_file.write_text(json.dumps({'rows':captured,'issues':issues},ensure_ascii=False))
            cache_file.chmod(0o600)
        ids=[];main_ids=[]
        for row in captured:
            mid=row['id'].split('-')[-1]
            timestamp=dt.datetime.fromtimestamp(((int(mid)>>22)+1420070400000)/1000,dt.timezone.utc)
            if not row['timestamp_utc']:row['timestamp_utc']=timestamp.isoformat()
            if timestamp>end:continue
            ids.append(mid)
            if row['id'].split('-')[2] == checkpoint['main_channel_id']:
                main_ids.append(mid)
            variants.setdefault(row['id'],[]).append(row)
            rows[row['id']]=row
        pages.append({'file':path.name,'sha256':sha,'ids':list(dict.fromkeys(ids)),
                      'main_ids':list(dict.fromkeys(main_ids)),'issues':issues})
    allowed={checkpoint['main_channel_id'],*checkpoint['thread_high_water_message_ids']}
    allowed.update(r['id'].split('-')[-1] for r in rows.values()
                   if r['id'].split('-')[2]==checkpoint['main_channel_id'] and r['has_thread'])
    excluded=[r['id'] for r in rows.values() if r['id'].split('-')[2] not in allowed]
    canonical={}
    for row in rows.values():
        channel,mid=row['id'].split('-')[2:]
        if channel not in allowed: continue
        # A thread's rendered starter can repeat the main-channel message.
        if mid not in canonical or channel==checkpoint['main_channel_id']:
            canonical[mid]=row
    ordered=sorted(canonical.values(),key=lambda r:int(r['id'].split('-')[-1]))
    known={}
    root=Path(__file__).resolve().parents[1]
    for key in ('main_snapshot','thread_snapshot'):
        for row in json.loads((root/checkpoint[key]).read_text())['messages']:
            known[row['id'].split('-')[-1]]=row
    new=[r for r in ordered if r['id'].split('-')[-1] not in known]
    def save(name,value):
        path=directory/name;path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');path.chmod(0o600)
    save('capture-all.json',{'guild_id':checkpoint['guild_id'],'captured_before':cutoff,'messages':ordered})
    save('capture-new.json',{'guild_id':checkpoint['guild_id'],'captured_before':cutoff,'messages':new})
    save('page-index.json',pages);save('capture-variants.json',variants)
    # Connected overlap is evidence of traversal continuity, not server exhaustiveness.
    # A still-open thread sidebar must not falsely connect two main-channel pages.
    main=[p for p in pages if p['file'].startswith('main-') and p['main_ids']]
    remaining=set(range(len(main)));groups=[]
    while remaining:
        component={remaining.pop()};ids=set(main[next(iter(component))]['main_ids'])
        while True:
            linked={i for i in remaining if ids.intersection(main[i]['main_ids'])}
            if not linked:break
            component.update(linked);remaining-=linked
            for i in linked:ids.update(main[i]['main_ids'])
        groups.append({'pages':[main[i]['file'] for i in sorted(component)],'unique_ids':len(ids)})
    summary={'parser_version':PARSER_VERSION,'out_of_scope_ids_excluded':excluded,'pages':len(pages),'unique':len(ordered),'new':len(new),'checkpoint_present':any(r['id'].endswith('-'+checkpoint['capture_high_water_message_id']) for r in ordered),
             'main_overlap_components':groups,'first':ordered[0]['timestamp_utc'] if ordered else None,'last':ordered[-1]['timestamp_utc'] if ordered else None,
             'new_thread_starters':[r['id'] for r in new if r['has_thread']],'published_checkpoint_advanced':False}
    save('import-summary.json',summary)
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--cutoff',required=True)
    args=p.parse_args();root=Path(__file__).resolve().parents[1]
    cp=json.loads((root/'resource-pool/sources/collection-checkpoint.json').read_text())
    print(json.dumps(run(args.directory,cp,args.cutoff),indent=2))
if __name__=='__main__':main()
