const $ = (id) => document.getElementById(id);
const node = (tag, text, cls) => { const n = document.createElement(tag); if (text) n.textContent = text; if (cls) n.className = cls; return n; };
function section(title, parent) { const s = node('section', null, 'answer-section'); s.append(node('h2', title)); parent.append(s); return s; }
function link(label, url) { const a = node('a', label); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; }
function sourceLinks(text, parent) {
  // Content is text, never executable Markdown/HTML. Only HTTP(S) links are clickable.
  const urls = [...new Set(text.match(/https?:\/\/[^\s)\]>"']+/g) || [])];
  const box = node('div', null, 'source-links');
  for (const url of urls) { try { const u = new URL(url); if (['https:', 'http:'].includes(u.protocol)) box.append(link(u.hostname + u.pathname.slice(0, 80), u.href)); } catch {} }
  parent.append(box);
}
function cards(title, rows, parent) {
  const s = section(title, parent);
  if (!rows.length) { s.append(node('p', 'No matching curated evidence surfaced. This does not establish that none exists.')); return; }
  for (const c of rows) {
    const card = node('article', null, 'case'); card.append(node('span', c.evidence_role.replaceAll('_', ' '), 'eyebrow'), node('h3', c.title));
    for (const [label, field] of [['What', 'what'], ['Jev’s role', 'how'], ['Reported impact', 'reported_impact'], ['Limits', 'limits']]) {
      card.append(node('h4', label), node('p', c[field]));
    }
    const detail = node('details'); detail.append(node('summary', 'Sources and review status'), node('pre', c.sources)); sourceLinks(c.sources, detail); card.append(detail);
    card.append(link('Open complete case ↗', '/' + c.path)); s.append(card);
  }
}
function render(r) {
  const root = $('result'); root.replaceChildren();
  const overview = section(r.pattern_label, root); overview.append(node('p', r.fit, 'fit'));
  if (r.proposal) {
    overview.append(node('p', r.proposal.role), node('h3', 'Proposed place in your workflow'), node('p', 'Approved input → deterministic checks → focused Jev judgment → fallback or permitted action', 'flow'), node('p', r.proposal.host), node('p', r.proposal.caution, 'caution'));
    const proto = node('details'); proto.append(node('summary', 'Inspect proposed state and typed question'), node('p', 'Design template. Replace placeholders and define real options before use. Not executed.'), node('pre', JSON.stringify(r.prototype, null, 2))); overview.append(proto);
  }
  const why = section('Evidence to learn from', root); why.append(node('p', r.coverage.note));
  cards('Related implementations', r.support, root); cards('Counterexamples and mixed results', r.counterevidence, root);
  const plan = section('Validate before rollout', root); const ol = node('ol'); r.validation.forEach(t => ol.append(node('li', t))); plan.append(ol);
  const next = section('Refine your idea', root); r.questions.forEach(t => next.append(node('p', t))); next.append(node('p', 'Add these details to your description above and explore again. Ideas stay in this page; no chat history is saved.'));
  const refs = section('Capability references', root); r.references.forEach(url => refs.append(link(url, url)));
  const method = r.router.method === 'jev_choice' ? `Jev routing: ${r.router.model}. Confidence ${(r.router.confidence * 100).toFixed(0)}% is not a correctness guarantee.` : 'Local keyword routing; no API call required.';
  refs.append(node('p', method + (r.router.fallback_reason ? ' ' + r.router.fallback_reason : '')), node('p', `${r.coverage.curated_cases} case records; ${r.coverage.unreviewed_urls ?? 'unknown number of'} URLs await first review; ${r.coverage.urls_with_content_gaps ?? 'unknown number of'} URLs retain content gaps. ${r.answer_method}`));
}
document.querySelectorAll('[data-idea]').forEach(b => b.addEventListener('click', () => { $('idea').value = b.dataset.idea; $('idea').focus(); }));
$('ask').addEventListener('submit', async e => {
  e.preventDefault(); $('submit').disabled = true; $('status').textContent = 'Finding cases, limits, and counterexamples…';
  try {
    const response = await fetch('/api/answer', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({idea: $('idea').value, use_jev: $('jev').checked})});
    const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Request failed');
    render(result); $('status').textContent = 'Integration brief ready. Review source limits before applying it.'; $('result').scrollIntoView({behavior: 'smooth'});
  } catch (err) { $('status').textContent = err.message; }
  finally { $('submit').disabled = false; }
});
