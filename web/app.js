import {categories, prepare, short, plain, links, signal, filterCases, shuffled} from './evidence.mjs';
const $ = id => document.getElementById(id);
const node = (tag, text, cls) => { const n = document.createElement(tag); if (text != null) n.textContent = text; if (cls) n.className = cls; return n; };
function link(label, url, cls) { const a = node('a', label, cls); a.href = url; if (/^https?:/.test(url) || url.startsWith('/docs/')) { a.target = '_blank'; a.rel = 'noopener noreferrer'; } return a; }
function button(label, action, cls = 'secondary') { const b = node('button', label, cls); b.type = 'button'; b.addEventListener('click', action); return b; }
function heading(title, caption, parent) { const h = node('div', null, 'section-heading'); h.append(node('h2', title)); if (caption) h.append(node('p', caption)); parent.append(h); }
function badge(text, tone = 'neutral') { return node('span', text, `pill ${tone}`); }
function metric(value, label, note) { const el = node('div', null, 'metric'); el.append(node('span', label, 'eyebrow'), node('strong', value)); if (note) el.append(node('small', note)); return el; }
function expand(label, text, parent) { if (!text) return; const d = node('details'); d.append(node('summary', label), node('p', plain(text), 'preserve')); parent.append(d); }
function sourceLinks(text, parent) {
  const urls = links(text);
  if (!urls.length) parent.append(node('p', 'No public artifact link recorded. Discord source provenance remains private.', 'muted'));
  for (const item of urls) {
    const a = link('', item.url, 'artifact'); a.append(node('span', `${item.kind} ↗`, 'eyebrow'), node('strong', item.label)); parent.append(a);
  }
}
let catalogPromise;
async function catalog() {
  if (!catalogPromise) catalogPromise = fetch('/docs/bot-cases.json').then(r => { if (!r.ok) throw new Error('Case catalog could not be loaded.'); return r.json(); }).then(rows => rows.map(prepare)).catch(e => { catalogPromise = null; throw e; });
  return catalogPromise;
}
const library = {group: 'All', query: '', limit: 18, random: false, order: null};
let caseReturn = '#use-cases';
function caseTile(c, origin = '#use-cases', counter = false) {
  const s = c.signal || signal(c);
  const a = link('', `#case/${encodeURIComponent(c.id)}`, 'case-tile');
  a.addEventListener('click', () => { caseReturn = origin; });
  const top = node('div', null, 'tile-top'); top.append(node('span', c.group || c.evidence_role.replaceAll('_', ' '), 'eyebrow'), node('span', '↗', 'tile-arrow'));
  a.append(top, node('h3', c.title), node('p', short(counter ? c.limits : c.what, 175), 'tile-caption'));
  const foot = node('div', null, 'tile-foot'); foot.append(badge(s.label, s.tone), node('small', c.default_retrieval === false ? 'Held from bot retrieval' : c.evidence_role.replaceAll('_', ' ')));
  a.append(foot); return a;
}
function pageIntro(root, back, title, caption) {
  root.append(link(back.startsWith('#bot') ? '← Back to bot' : '← Back to use cases', back, 'back'));
  const h = node('h1', title); h.tabIndex = -1;
  root.append(h, node('p', caption, 'lede')); return h;
}
async function showExplorer(version) {
  const root = $('explorer-view'); root.replaceChildren(node('p', 'Loading use cases…', 'muted'));
  try {
    const rows = await catalog(); if (version !== routeVersion) return;
    root.replaceChildren();
    pageIntro(root, '#bot', 'Explore what’s possible.', 'Real applications. Useful tools. Honest limits. Find a pattern worth testing.');
    const stats = node('div', null, 'library-stats'); stats.append(badge(`${rows.length} case records`, 'green'), node('span', `${categories.length} broad categories`), node('span', 'Reports, experiments & counterexamples')); root.append(stats);
    const controls = node('div', null, 'filters');
    const searchLabel = node('label', 'Find a use case'); const search = node('input'); search.type = 'search'; search.id = 'case-search'; search.placeholder = 'Search ideas, tools, or Jev’s role'; search.value = library.query; searchLabel.append(search);
    const categoryLabel = node('label', 'Category'); const select = node('select'); select.id = 'case-category';
    for (const group of ['All', ...categories]) { const option = node('option', group); option.value = group; select.append(option); } select.value = library.group; categoryLabel.append(select);
    const random = button('↻ Randomize', () => { library.random = true; library.order = shuffled(filterCases(rows, library.group, library.query)); library.limit = 18; draw(); }); random.id = 'randomize';
    controls.append(searchLabel, categoryLabel, random); root.append(controls);
    const status = node('p', null, 'results-count'); status.id = 'case-count'; status.setAttribute('role', 'status');
    const grid = node('div', null, 'case-grid'); grid.id = 'case-grid';
    const more = button('Show more use cases', () => { library.limit += 18; draw(); }); more.id = 'load-more';
    root.append(status, grid, more);
    const explanation = node('details', null, 'fit-explainer'); explanation.append(node('summary', 'How to read fit signals'), node('p', 'Signals summarize the editorial evidence type, not measured Jev quality. Conditional fit means reported use with limits. Mixed results, reported limitations and known limitations highlight caution. Exploratory and not established records need more evidence. Integration tools support development. No case benchmark has been independently reproduced. Categories are browsing aids; some cases span several.')); root.append(explanation);
    function draw() {
      const matched = filterCases(rows, library.group, library.query);
      const ordered = library.random ? (library.order ||= shuffled(matched)) : matched;
      grid.replaceChildren(...ordered.slice(0, library.limit).map(c => caseTile(c)));
      status.textContent = `${library.random ? 'Randomized · ' : ''}Showing ${Math.min(library.limit, ordered.length)} of ${ordered.length} use cases`;
      more.hidden = ordered.length <= library.limit;
      if (!ordered.length) grid.append(node('div', 'No matches. Try a broader search or choose All.', 'empty'));
    }
    function update() { library.group = select.value; library.query = search.value; library.limit = 18; library.order = null; draw(); }
    search.addEventListener('input', update); select.addEventListener('change', update); draw();
    root.querySelector('h1').focus({preventScroll: true});
  } catch (e) { if (version === routeVersion) showError(root, e, () => showExplorer(version)); }
}
function showError(root, e, retry) { root.replaceChildren(link('← Back to bot', '#bot', 'back'), node('h1', 'Couldn’t load this view'), node('p', e.message), button('Try again', retry)); }
async function showCase(id, version) {
  const root = $('detail-view'); root.replaceChildren(node('p', 'Loading case…', 'muted'));
  try {
    const rows = await catalog(); if (version !== routeVersion) return;
    const c = rows.find(r => r.id === id);
    if (!c) { root.replaceChildren(link('← Browse use cases', '#use-cases', 'back'), node('h1', 'Use case not found'), node('p', 'This link does not match the current catalog.')); return; }
    root.replaceChildren();
    pageIntro(root, caseReturn, c.title, plain(c.what));
    const tags = node('div', null, 'library-stats'); tags.append(badge(c.group), badge(c.evidence_role.replaceAll('_', ' ')), badge(c.default_retrieval ? 'Available to bot' : 'Held from bot retrieval', c.default_retrieval ? 'green' : 'warn')); root.append(tags);
    const metrics = node('div', null, 'metrics three'); metrics.append(metric(c.signal.label, 'Fit signal', c.signal.note), metric(String(links(c.sources).length), 'Public links', 'Artifacts and context; review status varies.'), metric('Not reproduced', 'Validation', 'Reported results are not independent benchmarks.')); root.append(metrics);
    const layout = node('div', null, 'detail-layout'); const main = node('div'); const aside = node('aside', null, 'artifact-panel');
    heading('The integration, at a glance', 'Source-grounded summary. No inferred architecture.', main);
    const table = node('table', null, 'summary-table'); const tbody = node('tbody');
    for (const [label, text] of [['Jev’s role', c.how], ['Value / reported impact', c.impact], ['Weaknesses & unknowns', c.limits]]) {
      const tr = node('tr'); tr.append(node('th', label)); tr.firstChild.scope = 'row'; const td = node('td');
      // Long review histories stay available without dominating the summary table.
      const full = plain(text || 'Not specified in the available record.');
      let destination = td;
      if (full.length > 650) {
        td.append(node('p', short(full, 300)));
        const all = node('details'); all.append(node('summary', label === 'Weaknesses & unknowns' ? 'Read all limitations & review updates' : 'Read full account'));
        td.append(all); destination = all;
      }
      for (const part of full.split(/\n\n+|(?=(?:Source review|Media review|Follow-up review):)/)) if (part.trim()) destination.append(node('p', part.trim()));
      tr.append(td); tbody.append(tr);
    }
    table.append(tbody); main.append(table);
    const checklist = node('div', null, 'callout'); checklist.append(node('strong', 'Before reusing this pattern'), node('p', 'Define the exact input and bounded decision. Test near-matches, failure cases, and a safe fallback against your current workflow.')); main.append(checklist);
    heading('Important links', 'Source access does not establish implementation quality.', aside); sourceLinks(c.sources, aside);
    expand('Source review notes', c.sources, aside); aside.append(link('Full evidence record ↗', '/' + c.path, 'record-link'));
    layout.append(main, aside); root.append(layout); root.querySelector('h1').focus({preventScroll: true});
  } catch (e) { if (version === routeVersion) showError(root, e, () => showCase(id, version)); }
}
let routeVersion = 0;
function route() {
  const hash = location.hash || '#bot'; const version = ++routeVersion;
  if (hash !== '#bot-results') window.scrollTo(0, 0);
  const isCase = hash.startsWith('#case/'); const isExplorer = hash === '#use-cases';
  $('bot-view').hidden = isCase || isExplorer; $('explorer-view').hidden = !isExplorer; $('detail-view').hidden = !isCase;
  document.title = isCase ? 'Use case · Jev-bot' : isExplorer ? 'Explore use cases · Jev-bot' : 'Jev-bot · Idea to integration';
  if (isExplorer) showExplorer(version);
  else if (isCase) { let id; try { id = decodeURIComponent(hash.slice(6)); } catch { id = ''; } showCase(id, version); }
  else if (hash === '#bot-results') $('result').scrollIntoView();
  else window.scrollTo(0, 0);
}
window.addEventListener('hashchange', route);
document.querySelector('.brand').href = '#bot';
function evidenceCards(title, caption, rows, parent, counter = false) {
  heading(title, caption, parent); const grid = node('div', null, 'case-grid related');
  if (!rows.length) grid.append(node('p', 'No matching evidence surfaced. Absence here does not establish that none exists.', 'empty'));
  rows.forEach(c => grid.append(caseTile(c, '#bot-results', counter))); parent.append(grid);
}
function render(r) {
  const root = $('result'); root.replaceChildren();
  const intro = node('div', null, 'answer-intro'); intro.append(node('p', 'YOUR INTEGRATION MAP', 'eyebrow'), node('h2', r.pattern_label), node('p', r.fit, 'fit')); root.append(intro);
  const primitive = r.prototype?.questions?.decision?.type || '—';
  const metrics = node('div', null, 'metrics'); metrics.append(metric(primitive === '—' ? 'Not proposed' : primitive.toUpperCase(), 'Decision primitive', primitive === '—' ? 'See fit assessment' : 'Proposed design, not executed'), metric(String(r.support.length), 'Related cases', 'Analogies, not proof of fit'), metric(String(r.counterevidence.length), 'Counterexamples', 'Failures and mixed results'), metric(r.router.method === 'jev_choice' ? 'Jev' : 'Local rules', 'Idea routing', r.router.method === 'jev_choice' ? 'Typed classification' : r.router.fallback_reason ? 'Local fallback; see notice' : 'No API call')); root.append(metrics);
  if (r.router.fallback_reason) root.append(node('p', r.router.fallback_reason, 'caution'));
  if (r.proposal) {
    heading('Where Jev fits', 'A bounded decision inside your application.', root);
    const flow = node('ol', null, 'workflow');
    for (const [name, detail] of [['Prepare', 'Approved input + deterministic checks'], ['Judge', `Focused ${primitive} question`], ['Act', 'Permitted action or fallback']]) { const li = node('li'); li.append(node('strong', name), node('span', detail)); flow.append(li); } root.append(flow);
    const roles = node('div', null, 'role-grid');
    for (const [title, text, cls] of [['Jev’s job', r.proposal.role, ''], ['Your application’s job', r.proposal.host, ''], ['Watch out for', r.proposal.caution, 'warning-panel']]) { const box = node('section', null, 'panel ' + cls); box.append(node('h3', title), node('p', text)); roles.append(box); } root.append(roles);
  }
  evidenceCards('Patterns to borrow', r.coverage.note, r.support, root);
  evidenceCards('Limits to design around', 'Keep these counterexamples in the design—not only the footnotes.', r.counterevidence, root, true);
  heading('Test before rollout', 'Three checks before this becomes a real integration.', root);
  const checks = node('ol', null, 'check-grid'); r.validation.forEach((text, i) => { const li = node('li'); li.append(node('span', `0${i + 1}`, 'step-number'), node('p', text)); checks.append(li); }); root.append(checks);
  const next = node('details'); next.append(node('summary', 'Refine this recommendation')); const ul = node('ul'); r.questions.forEach(q => ul.append(node('li', q))); next.append(ul, node('p', 'Add these details to your idea above, then explore again.')); root.append(next);
  if (r.prototype) { const d = node('details'); d.append(node('summary', 'Inspect proposed API shape'), node('p', 'Unexecuted design template. Replace placeholders and define real options.'), node('pre', JSON.stringify(r.prototype, null, 2))); root.append(d); }
  const method = node('details'); method.append(node('summary', 'Sources, routing & coverage'));
  r.references.forEach(url => method.append(link(url, url, 'record-link')));
  if (r.router.method === 'jev_choice') method.append(node('p', `Routing model: ${r.router.model}. Model confidence ${Number.isFinite(r.router.confidence) ? (r.router.confidence * 100).toFixed(0) + '%' : 'unavailable'} is not calibrated accuracy or a correctness guarantee.`));
  method.append(node('p', `${r.coverage.curated_cases} case records · ${r.coverage.urls_with_content_gaps ?? 'Unknown'} URLs with content gaps. ${r.answer_method}`)); root.append(method);
}
document.querySelectorAll('[data-idea]').forEach(b => b.addEventListener('click', () => { $('idea').value = b.dataset.idea; $('idea').focus(); }));
$('ask').addEventListener('submit', async e => {
  e.preventDefault(); $('submit').disabled = true; $('status').textContent = 'Finding cases, limits, and counterexamples…';
  try {
    const response = await fetch('/api/answer', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({idea: $('idea').value, use_jev: $('jev').checked})});
    const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Request failed');
    render(result); $('status').textContent = 'Integration map ready. Review evidence limits before applying it.'; $('result').scrollIntoView({behavior: 'smooth'});
  } catch (err) { $('status').textContent = err.message; }
  finally { $('submit').disabled = false; }
});
route();
