// The Bharat test live demo: pick a language and a real test sentence (or write your own) and ask Jev live.
// Recorded answers come from bharat-samples.json; live answers come from POST /api/try. They are always labelled.
const $ = id => document.getElementById(id);
const node = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const pct = x => (Math.round(x * 1000) / 10).toFixed(1) + '%';
const fmt1 = x => (x == null ? '–' : Number(x).toFixed(1) + '%');
const MAX = 500;

let DATA = null, task = 'topic', lang = null, picked = null, seq = 0;

function languages() { return task === 'topic' ? DATA.topic.languages : DATA.intent.locales; }
function label(key) { return task === 'intent' ? DATA.spec.intent.criteria[key] || key : key; }
function langName(l) { return l.native === l.name ? l.name : l.native + ' · ' + l.name; }

function renderStats() {
  const s = DATA.summary, dl = $('stats');
  dl.replaceChildren();
  [[s.beats + ' / ' + s.of, 'Indian test sets where Jev scored above GPT-4’s published result'],
   [s.most_spoken_jev.toFixed(1) + '%', 'topic accuracy on the 10 most-spoken Indian languages'],
   [s.seconds_p50.toFixed(2) + ' s', 'median time per request'],
   ['$' + s.usd_per_1000.toFixed(3), 'per 1,000 requests at list price']].forEach(([n, t]) => {
    const d = node('div'); d.append(node('dt', null, n), node('dd', null, t)); dl.append(d);
  });
}

function renderTabs() {
  document.querySelectorAll('.tabs button').forEach(b => {
    const on = b.dataset.task === task;
    b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1;
  });
  $('panel').setAttribute('aria-labelledby', 'tab-' + task);
  $('samples-title').textContent = task === 'topic' ? 'Real test sentences' : 'Real voice requests';
  $('text-label').textContent = task === 'topic' ? 'Sentence' : 'Voice request (as text)';
  $('text').placeholder = task === 'topic' ? 'Type or paste a sentence in any Indian language…' : 'Type a request, e.g. “రేపు ఉదయం 6 గంటలకు అలారం పెట్టు”';
  $('run').textContent = 'Ask Jev live';
}

function renderLanguages(preferName) {
  const sel = $('lang'), list = languages();
  sel.replaceChildren(...list.map(l => { const o = node('option', null, langName(l)); o.value = l.code; return o; }));
  lang = list.find(l => l.name === preferName) || list.find(l => l.name === 'Telugu') || list[0];
  sel.value = lang.code;
  renderLanguage();
}

function renderLanguage() {
  const a = lang.accuracy, p = $('lang-stats');
  p.replaceChildren();
  if (task === 'topic') {
    p.append('Accuracy on all 204 ' + lang.name + ' test sentences: ', node('b', null, 'Jev ' + fmt1(a.jev)),
      ' · gpt-6-astra ' + fmt1(a.gpt6) + ' · GLM 5.3 ' + fmt1(a.glm) + ' · GPT-4 ' + fmt1(a.gpt4) + ' (published, 2023)');
  } else {
    p.append('Accuracy on all 2,974 ' + lang.name + ' test requests: ', node('b', null, 'Jev ' + fmt1(a.jev)),
      ...(a.xlmr_zero != null ? [' · XLM-R trained on English only ' + fmt1(a.xlmr_zero)] : []),
      ' · XLM-R trained on ' + lang.name + ' ' + fmt1(a.xlmr_full) + ' (published)');
  }
  const ol = $('samples');
  ol.replaceChildren(...lang.samples.map(s => {
    const li = node('li'), b = node('button');
    b.type = 'button'; b.setAttribute('aria-pressed', picked === s);
    const t = node('span', 's-text', s.text); t.dir = 'auto';
    b.append(t, node('span', 's-gold', 'Human label: ' + label(s.gold)));
    b.addEventListener('click', () => pick(s));
    li.append(b); return li;
  }));
}

function pick(sample) {
  picked = sample;
  $('text').value = sample.text;
  update();
  document.querySelectorAll('#samples button').forEach((b, i) => b.setAttribute('aria-pressed', lang.samples[i] === sample));
  ask();
  if (window.matchMedia('(max-width: 860px)').matches) $('text').scrollIntoView({behavior: 'smooth', block: 'start'});
}

function payload(text) {
  const q = DATA.spec[task];
  return {model: DATA.spec.model, state: {text}, questions: {[task]: {type: 'choice', instructions: q.instructions, criteria: q.criteria}}};
}

function update() {
  const text = $('text').value, n = text.trim().length;
  if (picked && text !== picked.text) {
    picked = null;
    document.querySelectorAll('#samples button').forEach(b => b.setAttribute('aria-pressed', false));
    $('recorded').replaceChildren();
  }
  $('count').textContent = text.length + ' / ' + MAX;
  $('count').classList.toggle('over', text.length > MAX);
  $('run').disabled = n < 1 || text.length > MAX;
  $('request-json').textContent = JSON.stringify(payload(text.trim() || '…'), null, 2);
}

function renderRecorded(sample) {
  const box = $('recorded');
  box.replaceChildren();
  if (!sample) return;
  const card = node('div', 'card');
  const meta = node('div', 'meta'); meta.append(node('span', 'pill rec', 'RECORDED'), node('span', null, 'Same sentence, answered on ' + DATA.recorded));
  const table = node('table', 'rec-table'), body = node('tbody');
  const row = (who, key, compare = true) => {
    const tr = node('tr'), th = node('th', null, who), td = node('td', null, label(key));
    if (compare) { const ok = key === sample.gold; td.append(node('span', 'mark ' + (ok ? 'ok' : 'no'), ok ? '✓' : '✗')); }
    tr.append(th, td); body.append(tr);
  };
  row('Human label', sample.gold, false);
  row('Jev', sample.jev.choice);
  if (task === 'topic') { row('gpt-6-astra', sample.gpt6); row('GLM 5.3', sample.glm); }
  table.append(body); card.append(meta, table); box.append(card);
}

function renderLive(r, sample) {
  const card = node('div', 'card live');
  const meta = node('div', 'meta');
  meta.append(node('span', 'pill live', 'LIVE'), node('span', null, r.model), node('span', null, r.seconds.toFixed(2) + ' s'),
              node('span', null, r.usd != null ? '$' + r.usd.toFixed(6) + ' · ' + r.input_tokens + ' input tokens' : 'cost not reported'));
  const ans = node('div', 'answer', r.label); ans.lang = 'en';
  card.append(meta, ans, node('p', 'conf', r.confidence != null ? 'Confidence ' + pct(r.confidence) : 'Confidence not reported'));
  const bars = node('div', 'bars');
  r.ranked.forEach((o, i) => {
    const b = node('div', 'bar' + (o.key === r.choice ? ' top' : ''));
    const track = node('div', 'track'), fill = node('div', 'fill');
    track.append(fill); b.append(node('span', 'name', o.label), node('span', 'p', pct(o.p)), track);
    bars.append(b);
    requestAnimationFrame(() => requestAnimationFrame(() => { fill.style.width = Math.max(0.5, o.p * 100) + '%'; }));
  });
  card.append(bars);
  if (task === 'intent' && r.ranked.length) card.append(node('p', 'hint', 'Top ' + r.ranked.length + ' of 60 intents shown.'));
  if (sample) {
    const ok = r.choice === sample.gold;
    card.append(node('p', 'check ' + (ok ? 'ok' : 'no'), ok ? '✓ Matches the human label' : '✗ The human label is “' + label(sample.gold) + '”'));
  }
  $('result').replaceChildren(card);
}

function fail(message, retry) {
  const s = $('status');
  s.className = 'status err'; s.replaceChildren(message);
  if (retry) { const b = node('button', 'ghost retry', 'Try again'); b.type = 'button'; b.addEventListener('click', ask); s.append(b); }
}

async function ask() {
  const text = $('text').value.trim();
  if (!text || text.length > MAX) return;
  const mine = ++seq, sample = picked && picked.text.trim() === text ? picked : null, forTask = task;
  $('result').replaceChildren();                   // clear the previous answer immediately
  renderRecorded(sample);
  const s = $('status'); s.className = 'status'; s.replaceChildren(node('span', 'spin'), 'Asking Jev…');
  $('run').disabled = true;
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 30000);
  try {
    const res = await fetch('/api/try', {method: 'POST', headers: {'Content-Type': 'application/json'},
                                         body: JSON.stringify({task: forTask, text}), signal: controller.signal});
    const data = await res.json().catch(() => ({}));
    if (mine !== seq) return;
    if (!res.ok) return fail(data.error || 'Jev couldn’t answer right now.', res.status !== 400);
    s.replaceChildren();
    renderLive(data, sample);
  } catch {
    if (mine === seq) fail('Couldn’t reach the server. Check your connection and try again.', true);
  } finally {
    clearTimeout(timer);
    if (mine === seq) update();
  }
}

function setTask(next) {
  if (next === task) return;
  const keep = lang && lang.name;
  task = next; picked = null; seq++;
  $('result').replaceChildren(); $('recorded').replaceChildren(); $('status').replaceChildren();
  renderTabs(); renderLanguages(keep); update();
  history.replaceState(null, '', '#' + task);
}

async function init() {
  try {
    DATA = await (await fetch('/bharat-samples.json')).json();
  } catch {
    $('samples').replaceChildren(node('li', 'status err', 'Couldn’t load the test sentences. Reload the page to try again.'));
    return;
  }
  task = location.hash === '#intent' ? 'intent' : 'topic';
  renderStats(); renderTabs(); renderLanguages(); update();
  $('lang').addEventListener('change', e => {
    lang = languages().find(l => l.code === e.target.value);
    renderLanguage(); update();
  });
  $('text').addEventListener('input', update);
  $('text').addEventListener('keydown', e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); ask(); } });
  $('ask').addEventListener('submit', e => { e.preventDefault(); ask(); });
  document.querySelectorAll('.tabs button').forEach(b => b.addEventListener('click', () => setTask(b.dataset.task)));
  document.querySelector('.tabs').addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { setTask(task === 'topic' ? 'intent' : 'topic'); $('tab-' + task).focus(); }
  });
  window.addEventListener('hashchange', () => setTask(location.hash === '#intent' ? 'intent' : 'topic'));
  $('copy').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('request-json').textContent); $('copy').textContent = 'Copied'; }
    catch { $('copy').textContent = 'Copy failed'; }
    setTimeout(() => { $('copy').textContent = 'Copy JSON'; }, 1500);
  });
}
init();
