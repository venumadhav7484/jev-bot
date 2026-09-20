import {importIdeaFile} from './file-input.mjs';
import {exampleDesign, runCommand} from './answer-design.mjs?v=20260920-custom-only';
import {newsRequest, newsPython, newsSource} from './case-examples.mjs';
import {loadConfig, summarizeAnswer} from './bot-client.mjs?v=20260920-practical';
import {categories, prepare, short, plain, links, referenceUrls, signal, filterCases, shuffled} from './evidence.mjs?v=20260920-blueprint';
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
  if (!urls.length) parent.append(node('p', 'No public artifact link recorded.', 'muted'));
  for (const item of urls) {
    const a = link('', item.url, 'artifact'); a.append(node('span', `${item.kind} ↗`, 'eyebrow'), node('strong', item.label)); parent.append(a);
  }
}
let catalogPromise;
async function catalog() {
  if (!catalogPromise) catalogPromise = fetch('/docs/bot-cases.json?v=20260920-case-designs').then(r => { if (!r.ok) throw new Error('Case catalog could not be loaded.'); return r.json(); }).then(rows => rows.map(prepare)).catch(e => { catalogPromise = null; throw e; });
  return catalogPromise;
}
let designsPromise;
async function caseDesigns() {
  if (!designsPromise) designsPromise = fetch('/docs/case-designs.json?v=20260920-case-designs').then(r => {
    if (!r.ok) throw new Error('Examples could not be loaded.');
    return r.json();
  }).then(data => data.cases).catch(error => { designsPromise = null; throw error; });
  return designsPromise;
}
const library = {group: 'All', query: '', limit: 18, random: false, order: null};
let caseReturn = '#use-cases';
function caseTile(c, origin = '#use-cases', counter = false) {
  const s = c.signal || signal(c);
  const a = link('', `#case/${encodeURIComponent(c.id)}`, 'case-tile');
  a.addEventListener('click', () => { caseReturn = origin; });
  const top = node('div', null, 'tile-top'); top.append(node('span', c.group || c.evidence_role.replaceAll('_', ' '), 'eyebrow'), node('span', '↗', 'tile-arrow'));
  a.append(top, node('h3', c.title), node('p', short(counter ? c.limits : c.what, 175), 'tile-caption'));
  const foot = node('div', null, 'tile-foot'); foot.append(badge(s.label, s.tone), node('small', c.default_retrieval === false ? 'Limited evidence; caveats apply' : c.evidence_role.replaceAll('_', ' ')));
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
    caseDesigns().catch(() => {}); // Warm static examples while visitors browse tiles.
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
    pageIntro(root, caseReturn, c.title, short(c.what, 300));
    const tags = node('div', null, 'library-stats'); tags.append(badge(c.group), badge(c.signal.label, c.signal.tone)); root.append(tags);
    // Source facts and teaching examples are deliberately separate: examples are
    // adaptations, never a claim about the original project's implementation.
    const report = node('details', null, 'case-report');
    report.append(node('summary', 'What this project reported'));
    if (plain(c.what).length > 300) report.append(node('p', plain(c.what), 'preserve'));
    for (const [label, text] of [['Jev’s role', c.how], ['Reported value', c.impact], ['Limits', c.limits]]) {
      report.append(node('h3', label), node('p', plain(text), 'preserve'));
    }
    const caution = c.default_retrieval === false || c.signal.tone === 'warn';
    if (caution) root.append(node('p', `${c.signal.label}: ${short(c.limits, 280)}`, 'case-limit'));
    root.append(report);
    const designRoot = node('section', null, 'case-design'); root.append(designRoot);
    designRoot.append(node('p', 'Loading example…', 'muted'));
    const refs = node('section', null, 'case-source-links');
    heading('Explore the original', null, refs);
    sourceLinks(c.sources, refs); root.append(refs);
    if (c.id === 'news-aggregator') {
      const original = node('details', null, 'case-report');
      original.append(node('summary', 'Original news pipeline & runnable Python example'));
      renderNewsExample(original); root.append(original);
    }
    const adapt = node('div', null, 'case-adapt');
    adapt.append(node('h2', 'Adapt this to your idea'), node('p', 'Bring your own input and rules. Get a design for your workflow.'));
    adapt.append(button('Explore your idea ↗', () => {
      if (researchBusy) { location.hash = '#bot'; return; }
      $('idea').value = `I want to adapt ${c.title}. My input is… The decision I need is…`;
      $('result').replaceChildren();
      if (!researchBusy) $('status').textContent = '';
      ++fileReadVersion; $('idea-file').value = ''; $('file-status').textContent = '';
      location.hash = '#bot';
      $('idea').focus();
    })); root.append(adapt);
    root.querySelector('h1').focus({preventScroll: true});
    try {
      const designs = await caseDesigns(); if (version !== routeVersion) return;
      const saved = designs[c.id];
      if (!saved || saved.case_id !== c.id || saved.source_hash !== c.design_source_hash) throw new Error('No current example');
      designRoot.replaceChildren(node('p', 'TEACHING EXAMPLE · ADAPT TO YOUR APP', 'eyebrow'), node('h2', saved.blueprint.title));
      renderBlueprint(saved.blueprint, designRoot);
    } catch {
      if (version !== routeVersion) return;
      designRoot.replaceChildren(node('p', 'Example unavailable. Project details and sources remain below.'), button('Retry example', () => showCase(id, version)));
      report.open = true;
    }
  } catch (e) { if (version === routeVersion) showError(root, e, () => showCase(id, version)); }
}
function exampleCode(parent, title, value) {
  const block = node('div', null, 'example-code');
  const bar = node('div', null, 'example-code-bar');
  const copy = button('Copy code', async () => {
    try { await navigator.clipboard.writeText(value); copy.textContent = 'Copied'; }
    catch { copy.textContent = 'Select and copy the code below'; }
  });
  bar.append(node('strong', title), copy);
  const pre = node('pre'); pre.append(node('code', value)); block.append(bar, pre); parent.append(block);
}
function renderNewsExample(parent) {
  const section = node('section', null, 'implementation-example');
  heading('How to build this', 'A small working pattern you can adapt to your own feed.', section);
  section.append(node('h3', 'How the original project applies Jev'),
    node('p', 'The published implementation uses Choice to classify relevance and Noul to judge importance. Relevance determines retention; importance does not independently discard an article. The surrounding application handles collection and downstream writing.'));
  const sources = node('p', null, 'example-sources');
  sources.append(link('Original implementation ↗', newsSource+'agents/jev_relevance.py'), document.createTextNode(' · '),
    link('Frozen decision policy ↗', newsSource+'config/shadow/news-relevance-v4-frozen.json'));
  section.append(sources, node('p', 'Links are pinned to the inspected source revision. This is source-code inspection, not an independent reproduction of the project’s performance.', 'muted'));
  section.append(node('h3', 'Minimal example'), node('p', 'Original teaching code with a fictional article. It illustrates the same decision pattern; it is not the original project’s full implementation or a live sandbox.'));
  const steps = node('ol', null, 'example-flow');
  for (const step of ['Supply an article title, source and short snippet.', 'Ask Jev for a relevance category and an importance judgment.', 'Let application code keep, skip or retain the article for review. A separate writer can summarize kept articles.']) steps.append(node('li', step));
  section.append(steps);
  exampleCode(section, '1. Save as request.json', JSON.stringify(newsRequest, null, 2));
  exampleCode(section, '2. Save as filter_news.py', newsPython);
  section.append(node('p', 'Run on your computer or server with Python 3 and your own Jev API key in JEV_API_KEY. No extra packages are required. Running the script makes one API request; viewing or copying this example makes none.'));
  exampleCode(section, '3. Run', 'python3 filter_news.py');
  section.append(node('h3', 'What happens with the answer?'));
  const table = node('table', null, 'summary-table'); const body = node('tbody');
  for (const [decision, action] of [['relevant', 'send_to_writer — send the article to a separate summarizer.'], ['irrelevant', 'skip — leave it out of this AI-news feed.'], ['insufficient_evidence', 'retain_for_review — keep it available for a person or later analysis.'], ['Request failure or malformed response', 'retain_for_review — never silently discard an article because the service failed.']]) {
    const row = node('tr'); const th = node('th', decision); th.scope = 'row'; row.append(th, node('td', action)); body.append(row);
  }
  table.append(body); section.append(table, node('p', 'The script prints an action; it does not publish, delete or summarize anything. The importance answer is available at answers.importance.noul (0–1), but this minimal example leaves ranking to your application.'));
  section.append(node('p', 'Try clear AI news, unrelated news and an ambiguous headline against a labeled sample before automating your feed. Inspect false exclusions as well as correct keeps.'));
  section.append(link('Jev request and response reference ↗', 'https://docs.typesafe.ai/api'));
  parent.append(section);
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
document.querySelector('.brand').addEventListener('click', event => {
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
  event.preventDefault();
  $('ask').reset();
  history.replaceState(null, '', '/#bot');
  location.reload();
});
function evidenceCards(title, caption, rows, parent, counter = false) {
  heading(title, caption, parent); const grid = node('div', null, 'case-grid related');
  if (!rows.length) grid.append(node('p', 'No matching evidence surfaced. Absence here does not establish that none exists.', 'empty'));
  rows.forEach(c => grid.append(caseTile(c, '#bot-results', counter))); parent.append(grid);
}
function render(r) {
  if (r.mode) return renderResearch(r);
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
function renderComparison(comparison, root) {
  if (!comparison) return;
  const section = node('section', null, 'usage-comparison');
  heading('Tokens and estimated cost', comparison.scope, section);
  const wrap = node('div', null, 'usage-table-wrap');
  const table = node('table', null, 'usage-table');
  table.append(node('caption', 'Model usage for this query'));
  const head = node('thead'), header = node('tr');
  for (const label of ['Model / stage', 'Status', 'Input tokens', 'Output tokens', 'Estimated USD']) {
    const th = node('th', label); th.scope = 'col'; header.append(th);
  }
  head.append(header); table.append(head);
  const body = node('tbody');
  const number = value => Number.isFinite(value) ? value.toLocaleString() : 'Unknown';
  const dollars = value => Number.isFinite(value) ? (value === 0 ? '$0.000000' : value < .000001 ? '< $0.000001' : '$'+value.toFixed(6)) : 'Unknown';
  const statuses = {success: 'Complete', incomplete: 'Incomplete', not_run: 'Not run', failed: 'Failed', invalid_output: 'Invalid answer'};
  for (const row of comparison.rows) {
    const tr = node('tr'), model = node('th'); model.scope = 'row';
    model.append(node('strong', row.model), node('small', row.role)); tr.append(model);
    for (const value of [statuses[row.status] || row.status, number(row.tokens.input_tokens), number(row.tokens.output_tokens), dollars(row.cost.usd)]) tr.append(node('td', value));
    body.append(tr);
  }
  table.append(body); wrap.append(table); section.append(wrap);
  section.append(node('p', 'Total estimated model cost: '+dollars(comparison.total_estimated_usd), 'usage-total'), node('p', comparison.cost_note, 'mode-note'));
  const details = node('details'); details.append(node('summary', 'Pricing and cache details'));
  for (const row of comparison.rows) {
    const p = node('p'); p.append(node('strong', row.model+': '));
    if (row.provider === 'jev') p.append(document.createTextNode(`${row.api_requests} requests with reported usage; ${row.cached_requests} cached evaluations reused; ${row.unreported_attempts} attempts without usage. `));
    else if (Number.isFinite(row.tokens.cached_input_tokens)) p.append(document.createTextNode(`${number(row.tokens.cached_input_tokens)} cached input tokens included in input total. `));
    if (row.cost.assumption) p.append(document.createTextNode(row.cost.assumption+' '));
    if (row.cost.reason) p.append(document.createTextNode(row.cost.reason+' '));
    if (Number.isFinite(row.cost.known_usage_usd)) p.append(document.createTextNode(`Reported portion: ${dollars(row.cost.known_usage_usd)}. `));
    if (row.cost.pricing_url) p.append(link('Published pricing ↗', row.cost.pricing_url));
    details.append(p);
  }
  section.append(details); root.append(section);
}
const publicReferences = referenceUrls;
function renderBlueprint(design, root) {
  root.append(node('p', design.summary, 'design-summary'));
  const flow = node('ol', null, 'design-flow');
  flow.setAttribute('aria-label', 'Proposed workflow');
  for (const step of design.flow) {
    const item = node('li', null, 'flow-node owner-'+step.owner);
    item.append(node('span', {app: 'YOUR APP', jev: 'JEV', writer: 'WRITER', human: 'PEOPLE'}[step.owner], 'eyebrow'), node('strong', step.title), node('p', step.detail));
    flow.append(item);
  }
  root.append(flow);
  const workspace = node('section', null, 'example-workspace');
  const preview = node('div', null, 'worked-example');
  preview.append(node('h3', 'See it on an example'), node('p', 'Illustrative preview · no API call', 'muted'));
  const tabs = node('div', null, 'example-tabs');
  tabs.setAttribute('role', 'group'); tabs.setAttribute('aria-label', 'Example inputs');
  const input = node('p', null, 'sample-input'), output = node('pre', null, 'sample-output');
  const code = node('div', null, 'request-example');
  const buttons = [];
  function select(example, index) {
    input.textContent = example.input;
    output.textContent = JSON.stringify(example.output, null, 2);
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
    code.replaceChildren();
    exampleCode(code, 'request.json', JSON.stringify({...design.request, state: example.state}, null, 2));
  }
  design.examples.forEach((example, index) => {
    const control = button(example.label, () => select(example, index));
    buttons.push(control); tabs.append(control);
  });
  preview.append(tabs, node('p', 'INPUT', 'eyebrow'), input, node('p', 'EXPECTED APP ACTION', 'eyebrow'), output);
  preview.append(node('p', 'Jev returns typed answers. Your application maps them to this action; preview values are not live results.', 'muted'));
  workspace.append(preview, code); root.append(workspace); select(design.examples[0], 0);
  const run = node('details', null, 'run-example');
  run.append(node('summary', 'Run this request'), node('p', 'Save JSON as request.json. Run on your computer or server with JEV_API_KEY set. This makes one paid API request. Your application must validate the response and carry out any action; the request alone executes no actions.'));
  exampleCode(run, 'Terminal', runCommand);
  run.append(link('Jev API reference ↗', 'https://docs.typesafe.ai/api'));
  root.append(run);
  const outcome = node('div', null, 'design-outcome');
  for (const [label, text] of [['What you gain', design.impact], ['Keep this boundary', design.caution]]) {
    const item = node('div'); item.append(node('h3', label), node('p', text)); outcome.append(item);
  }
  root.append(outcome);
}
async function renderResearch(r) {
  const root = $('result'); root.replaceChildren();
  const rows = await catalog().catch(() => []);
  const byPath = new Map(rows.map(row => [row.path, row]));
  const evidence = r.evidence || [];
  const match = evidence.find(row => row.id === r.judgments?.closest_case?.choice);
  const closest = match && byPath.get(match.path);
  const ready = Boolean(r.judgments && r.coverage?.full_library_evaluated);
  const fit = r.judgments?.fit?.choice;
  const design = exampleDesign(r);
  const title = design?.title || 'Your answer couldn’t be completed';
  const intro = node('div', null, 'answer-intro');
  intro.append(node('p', 'YOUR IDEA', 'eyebrow'), node('p', r.idea, 'user-idea'), node('h2', title)); root.append(intro);
  if (!design) {
    root.append(node('p', 'Couldn’t generate a valid design for this idea. Please retry. No substitute example has been shown.'));
    if (r.comparison) {
      const usage = node('details', null, 'answer-usage'); usage.append(node('summary', 'Token usage and cost')); renderComparison(r.comparison, usage); root.append(usage);
    }
    return;
  }
  else if (design) {
    root.append(node('p', design.tailored ? 'PROPOSED DESIGN · TAILORED TO YOUR IDEA' : 'PROPOSED EXAMPLE PATTERN · ADAPT TO YOUR APP', 'eyebrow'));
    renderBlueprint(design, root);
  } else root.append(node('p', 'Name the input, allowed decisions and desired action. The available assessment does not establish a concrete implementation yet.'));
  const cited = new Set((r.narrative || []).flatMap(section => section.paragraphs.flatMap(p => p.citations)));
  const relevant = evidence.filter(row => !cited.size || cited.has(row.id));
  const ordered = [...(match ? [match] : []), ...relevant.filter(row => row.path.startsWith('docs/use-cases/')), ...relevant.filter(row => !row.path.startsWith('docs/use-cases/'))];
  const references = ordered.map(row => ({row, record: byPath.get(row.path), urls: publicReferences(row, byPath.get(row.path))})).filter(item => item.urls.length);
  // Teaching patterns also carry explicit analogies from the public catalog. They
  // are labeled related examples, never fabricated citations for model claims.
  for (const id of design?.sourceIds || []) {
    const record = rows.find(row => row.id === id);
    if (record) references.unshift({record, row: record, urls: publicReferences(null, record)});
  }
  if (references.length) {
    heading('Projects to learn from', 'Related implementations and examples; their results are not guarantees for your app.', root);
    const list = node('div', null, 'answer-references');
    const seen = new Set();
    for (const item of references) {
      const urls = item.urls.filter(url => !seen.has(url));
      if (!urls.length) continue;
      const card = node('div', null, 'reference-card'); card.append(node('strong', item.record?.title || item.row.title));
      if (item.record?.how) card.append(node('p', short(item.record.how.split(/Source review:|Media review:/)[0], 170)));
      for (const url of urls) { seen.add(url); card.append(link(new URL(url).hostname.replace(/^www\./, '')+' ↗', url)); }
      list.append(card);
      if (list.children.length === 3) break;
    }
    root.append(list);
  }
  if (r.narrative?.length) {
    const notes = node('details', null, 'answer-notes'); notes.append(node('summary', 'Why this design'));
    for (const section of r.narrative) for (const paragraph of section.paragraphs) {
      const p = node('p', paragraph.text);
      const urls = [...new Set(evidence.filter(row => paragraph.citations.includes(row.id)).flatMap(row => publicReferences(row, byPath.get(row.path))))];
      for (const url of urls.slice(0, 2)) p.append(document.createTextNode(' '), link('Source ↗', url));
      notes.append(p);
    }
    root.append(notes);
  }
  if (r.comparison) {
    const usage = node('details', null, 'answer-usage'); usage.append(node('summary', 'Token usage and cost')); renderComparison(r.comparison, usage); root.append(usage);
  }
}
function renderFeedback(jobId) {
  const section = node('section', null, 'answer-feedback');
  section.setAttribute('aria-label', 'Response feedback');
  const row = node('div', null, 'feedback-rating');
  row.append(node('strong', 'Did this help?'));
  const status = node('p', '', 'feedback-status'); status.setAttribute('role', 'status');
  const ratings = [];
  for (const [value, label] of [['up', 'Helpful'], ['down', 'Not helpful']]) {
    const b = button('', async () => {
      ratings.forEach(el => { el.disabled = true; });
      status.textContent = 'Saving…';
      try {
        await send({rating: value});
        b.setAttribute('aria-pressed', 'true');
        status.textContent = 'Thanks for your feedback.';
      } catch (error) {
        ratings.forEach(el => { el.disabled = false; });
        status.textContent = error.message;
      }
    }, 'feedback-thumb');
    b.setAttribute('aria-label', label); b.title = label; b.setAttribute('aria-pressed', 'false');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('aria-hidden', 'true');
    const path = document.createElementNS(svg.namespaceURI, 'path');
    path.setAttribute('d', 'M7 10v11H3V10h4Zm0 0 5-8c2 0 3 2 2 5l-1 3h6c2 0 2 2 1 4l-2 7H7');
    svg.append(path); if (value === 'down') svg.classList.add('thumb-down'); b.append(svg);
    ratings.push(b); row.append(b);
  }
  const form = node('form', null, 'feedback-form');
  const text = node('textarea'); text.rows = 2; text.maxLength = 2000;
  text.placeholder = 'What worked? What could be better? (optional)';
  text.setAttribute('aria-label', 'Feedback comment');
  const submit = node('button', 'Send feedback', 'secondary'); submit.type = 'submit'; submit.disabled = true;
  text.addEventListener('input', () => { submit.disabled = !text.value.trim(); });
  form.addEventListener('submit', async event => {
    event.preventDefault(); if (!text.value.trim() || submit.disabled) return;
    submit.disabled = true; text.disabled = true; status.textContent = 'Sending…';
    try { await send({comment: text.value.trim()}); status.textContent = 'Thanks for your feedback.'; submit.textContent = 'Sent'; }
    catch (error) { text.disabled = false; submit.disabled = false; status.textContent = error.message; }
  });
  async function send(data) {
    const response = await fetch('/api/feedback', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({job_id: jobId, ...data}), signal: AbortSignal.timeout(30000)});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Couldn’t save feedback. Please retry.');
  }
  form.append(text, submit);
  section.append(row, form, node('p', 'Shared with the site owner.', 'muted'), status);
  $('result').append(section);
}
document.querySelectorAll('[data-idea]').forEach(b => b.addEventListener('click', () => { $('idea').value = b.dataset.idea; $('idea').focus(); }));
let researchConfig = null;
let researchBusy = false;
let connectionState = 'loading';
const selectedMode = () => 'written';
function updateMode() {
  $('mode-note').textContent = 'Get a workflow, example request and relevant sources. Your text is sent to Jev and GLM when you submit.';
  let message = '';
  if (connectionState === 'loading') message = 'Connecting…';
  else if (connectionState === 'error') message = 'Can’t connect right now. Retry to load answer options.';
  else if (!researchConfig.jev_available || !researchConfig.writer_available) message = 'Answers are temporarily unavailable. Please try again later.';
  $('connection-status').textContent = message;
  $('retry-connection').hidden = connectionState !== 'error';
  $('submit').disabled = researchBusy || Boolean(message);
  $('status').classList.toggle('is-loading', researchBusy);
  $('result').setAttribute('aria-busy', String(researchBusy));
}
async function connect() {
  connectionState = 'loading'; updateMode();
  try {
    researchConfig = await loadConfig();
    connectionState = 'ready';
  } catch {
    researchConfig = null;
    connectionState = 'error';
  }
  updateMode();
}
$('attach-file').addEventListener('click', () => $('idea-file').click());
let fileReadVersion = 0;
$('idea-file').addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;
  const version = ++fileReadVersion;
  const draft = $('idea').value;
  $('file-status').textContent = 'Reading file…';
  try {
    const text = await importIdeaFile(file, draft);
    if (version !== fileReadVersion) return;
    if ($('idea').value !== draft) throw new Error('Your draft changed while the file was loading. Attach it again to keep both.');
    $('idea').value = text;
    $('file-status').textContent = file.name;
  } catch (error) { if (version === fileReadVersion) $('file-status').textContent = error.message; }
  finally { if (version === fileReadVersion) event.target.value = ''; }
});
$('retry-connection').addEventListener('click', connect);
connect();
$('ask').addEventListener('submit', async e => {
  e.preventDefault();
  if (connectionState !== 'ready' || researchBusy) return;
  $('result').replaceChildren();
  researchBusy = true; updateMode(); $('status').textContent = 'Checking your idea against the research…';
  const headers = {'Content-Type': 'application/json'};
  try {
    const response = await fetch('/api/jobs', {method: 'POST', headers, body: JSON.stringify({idea: $('idea').value, mode: selectedMode()})});
    const started = await response.json(); if (!response.ok) throw new Error(started.error || 'Request failed');
    while (true) {
      const poll = await fetch('/api/jobs/'+started.id, {headers}); const job = await poll.json();
      if (!poll.ok || job.status === 'failed') throw new Error(job.error || 'Answer job failed');
      if (job.status === 'complete') { await render(job.result); renderFeedback(started.id); $('status').textContent = exampleDesign(job.result) ? 'Your recommendation is ready.' : 'Couldn’t complete this answer. Please retry.'; $('result').scrollIntoView({behavior: 'smooth'}); break; }
      const p = job.progress || {};
      const stage = p.stage || '';
      $('status').textContent = stage === 'GLM is writing the explanation'
        ? 'Jev assessment complete. GLM is writing your explanation…'
        : stage === 'Jev is assessing the selected evidence' || (p.total && p.completed === p.total)
          ? 'Library review complete. Jev is forming your recommendation…'
          : stage === 'Jev is evaluating every research passage'
            ? `Jev is reviewing the library for your idea… ${Math.floor(100 * p.completed / p.total)}%`
            : 'Preparing your idea for review…';
      await new Promise(resolve => setTimeout(resolve, 1500));
    }
  } catch (err) { $('status').textContent = err.message; }
  finally { researchBusy = false; updateMode(); }
});
route();
