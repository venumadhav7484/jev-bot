// Presentation helpers consume the sanitized public catalog only.
export const categories = ['Work & business', 'Code & agents', 'Search & data', 'Games & robotics', 'Creative & interfaces', 'Safety & evaluation'];
const groups = {
  business: 0, consumer: 0, operations: 0, productivity: 0, routing: 0, 'finance-experiments': 0,
  agents: 1, browser: 1, 'developer-tools': 1, 'Developer tooling': 1, engineering: 1,
  retrieval: 2, data: 2, games: 3, robotics: 3,
  content: 4, interfaces: 4, voice: 4, creative: 4,
  security: 5, quality: 5, 'domain-review': 5, experiments: 5, limitations: 5,
};
export function sections(body = '') {
  return Object.fromEntries([...body.matchAll(/^## (.+)\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)].map(m => [m[1], m[2].trim()]));
}
export function category(row) {
  if (row.evidence_role === 'community_tool') return categories[1];
  const overrides = {'synthetic-email-filter': 0, 'document-profile': 2, 'jev-code': 1, 'semantic-relationships': 2, 'news-aggregator': 2};
  if (row.id in overrides) return categories[overrides[row.id]];
  if (row.category in groups) return categories[groups[row.category]];
  const t = `${row.id} ${row.title}`.toLowerCase();
  const rules = [
    [3, /game|tetris|minecraft|chess|poker|rubik|\batc\b|traffic|drone|robot|npc|simulation|valley|cubefield|nethack|mordhau|sims|2048|driving|hollow-knight|roblox|embodiment|pokemon|mario|codenames|holdem|catan|arcade|sonic|zombies|twenty-questions|permission-fatigue|almost-certain/],
    [5, /security|antivirus|vulnerab|faircheck|alignment|benchmark|comparison|legal|rubric|redaction|moderation|classifier|classification|codecheck|rules|quality|time-horizon/],
    [1, /sdk|client|wrapper|mcp|cli\b|jevctl|jev-axi|agent|browser|computer-use|code-router|opencode|schema|code-review|review-dev|session-to-skill|gemini/],
    [2, /search|sqlite|duckdb|bookmark|ranking|ranker|hacker-news|enron|filter/],
    [0, /trading|trade|arb|polymarket|lottery|sentiment|crypto|btc|price|inbox|email|intent|routing|phone|breed/],
    [4, /render|music|drum|pixel|drawing|keyboard|buttons|interface|drag-drop|parody|satire|generation|alphabet|chatjev|text-workaround|rivendell|suspicion|tweet|journal/],
  ];
  return categories[rules.find(([, re]) => re.test(t))?.[0] ?? 5];
}
export function plain(text = '') { return text.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/[*`]/g, '').trim(); }
export function short(text = '', max = 170) {
  const clean = plain(text).replace(/\s+/g, ' ');
  if (clean.length <= max) return clean;
  return clean.slice(0, max).replace(/\s+\S*$/, '') + '…';
}
export function links(text = '') {
  const found = [];
  for (const match of text.matchAll(/https?:\/\/[^\s)\]>"']+/g)) {
    try {
      const url = new URL(match[0]);
      if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) continue;
      if (!found.some(x => x.url === url.href)) {
        const host = url.hostname.replace(/^www\./, '');
        const kind = host === 'github.com' || host === 'gitlab.com' ? 'Repository' : /^(x.com|twitter.com)$/.test(host) ? 'Post' : /youtube.com|youtu.be/.test(host) ? 'Video' : 'Website / article';
        found.push({url: url.href, host, kind, label: `${host}${url.pathname === '/' ? '' : url.pathname}`});
      }
    } catch { /* Invalid source URLs stay in the full evidence record. */ }
  }
  return found;
}
export function referenceUrls(row, record) {
  return links(record?.sources || row?.text || '').map(item => item.url)
    .filter(url => !/\.(?:svg|png|jpg|css|woff2?)(?:[?#]|$)/i.test(url))
    .sort((a, b) => Number(b.includes('github.com')) - Number(a.includes('github.com'))).slice(0, 2);
}
export function signal(row) {
  const role = row.evidence_role;
  // These editorial titles explicitly identify a failure or unresolved validity concern.
  if (['tetris-dayton', 'alignment-monitor-gemma'].includes(row.id)) return {label: 'Reported limitation', tone: 'warn', note: 'The case highlights a failure or unresolved validity concern; inspect the evidence.'};
  if (role === 'counterexample') return {label: 'Known limitation', tone: 'warn', note: 'This record documents a failure or boundary.'};
  if (role === 'mixed') return {label: 'Mixed results', tone: 'warn', note: 'Useful behavior and limitations appear together.'};
  if (['thin', 'context_only'].includes(role)) return {label: 'Not established', tone: 'neutral', note: 'Evidence is too thin to establish application fit.'};
  if (['proposal', 'novelty', 'unvalidated_finance'].includes(role)) return {label: 'Exploratory', tone: 'neutral', note: 'An idea or experiment; effectiveness is not established.'};
  if (role === 'community_tool') return {label: 'Integration tool', tone: 'neutral', note: 'Supporting tooling, not a measured application outcome.'};
  return {label: 'Conditional fit', tone: 'green', note: 'Reported use; inspect limitations and validate for your workload.'};
}
export function prepare(row) {
  const s = sections(row.body);
  return {...row, group: category(row), what: s.What || '', how: s['How Jev fits'] || '', impact: s['Why and impact'] || '', limits: s['Limits and reuse'] || '', sources: s.Sources || '', signal: signal(row)};
}
export function filterCases(rows, group, query) {
  const terms = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return rows.filter(r => (group === 'All' || r.group === group) && terms.every(t => `${r.title} ${r.what} ${r.how}`.toLowerCase().includes(t)));
}
export function shuffled(rows, random = Math.random) {
  const copy = [...rows];
  for (let i = copy.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [copy[i], copy[j]] = [copy[j], copy[i]]; }
  return copy;
}
