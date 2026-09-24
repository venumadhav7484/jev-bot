import sys,unittest,json,tempfile
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from import_discord_pages import parse_html,run
class CaptureTests(unittest.TestCase):
 def test_thread_wrapper_does_not_replace_content_id(self):
  rows,issues=parse_html('<li id="chat-messages-10-11"><div>quoted preview</div><time id="message-timestamp-12" datetime="2026-09-24T01:00:00Z"></time><div id="message-content-12">Actual <b>body</b><br>next line</div><a href="https://example.com">source</a></li>','test.mhtml')
  self.assertEqual(rows[0]['id'],'chat-messages-10-12');self.assertEqual(rows[0]['body'],'Actual body\nnext line');self.assertEqual(rows[0]['links'][0]['text'],'source');self.assertEqual(issues[0]['issue'],'wrapper_content_difference')
 def test_nested_messages_not_duplicated_into_parent(self):
  html='<li id="chat-messages-10-11"><time id="message-timestamp-11"></time><div id="message-content-11">Parent</div><li id="chat-messages-10-12"><time id="message-timestamp-12"></time><div id="message-content-12">Child</div></li></li>'
  rows,_=parse_html(html,'test.mhtml');self.assertEqual(len(rows),2);self.assertNotIn('Child',rows[0]['text'])
 def test_missing_canonical_time_is_gap_not_invented_message(self):
  rows,issues=parse_html('<li id="chat-messages-10-11"><div id="message-content-11">Unknown</div></li>','test.mhtml');self.assertEqual(rows,[]);self.assertEqual(issues[0]['issue'],'canonical_timestamp_missing')
 def test_inline_spacing_and_context_are_preserved(self):
  html='<li id="chat-messages-10-11"><time id="message-timestamp-11"></time><div id="message-reply-context-11">Earlier claim</div><div id="message-content-11"><span>Look at </span><a href="https://example.com">https://example.com</a><span> for code.</span></div><article class="embed_x">Page preview</article></li>'
  row=parse_html(html,'test.mhtml')[0][0]
  self.assertEqual(row['body'],'Look at https://example.com for code.')
  self.assertIn('Earlier claim',row['reply_context']);self.assertIn('Page preview',row['reply_context'])
  self.assertNotIn('omitted',row['reply_context']);self.assertNotIn('Look at',row['reply_context'])
 def test_thread_sidebar_cannot_bridge_missing_main_history(self):
  with tempfile.TemporaryDirectory() as directory:
   folder=Path(directory);(folder/'pages').mkdir()
   known=folder/'known.json';known.write_text(json.dumps({'messages':[]}))
   cp={'guild_id':'1','main_channel_id':'10','thread_high_water_message_ids':{'20':'999'},'main_snapshot':str(known),'thread_snapshot':str(known),'capture_high_water_message_id':'101'}
   def row(ch,mid):return {'id':f'chat-messages-{ch}-{mid}','timestamp_utc':None,'has_thread':False,'body':'message','text':'message','links':[]}
   for name in ['main-001.mhtml','main-002.mhtml']:(folder/'pages'/name).write_text(name)
   def archive(path):return ([row('10','101' if path.stem=='main-001' else '102'),row('20','999'),row('30','888')],[])
   with patch('import_discord_pages.parse_archive',side_effect=archive):
    report=run(folder,cp,'2026-09-24T11:03:05Z')
   self.assertEqual(len(report['main_overlap_components']),2)
   self.assertEqual(report['unique'],3)
   self.assertEqual(report['out_of_scope_ids_excluded'],['chat-messages-30-888'])
if __name__=='__main__':unittest.main()
