// Reject service errors before they can be mistaken for feature availability.
export async function loadConfig(fetcher = fetch) {
  const response = await fetcher('/api/config', {cache: 'no-store', signal: AbortSignal.timeout(15000)});
  if (!response.ok) throw new Error('Service connection failed');
  const config = await response.json();
  if (!config || typeof config.jev_available !== 'boolean' || typeof config.writer_available !== 'boolean' ||
      (config.hosted === true && typeof config.access_required !== 'boolean')) {
    throw new Error('Invalid service configuration');
  }
  return config;
}

// Older saved answers used full_library_evaluated; newer ones report a completed shortlist search.
export const searchComplete = result => Boolean(result.coverage?.search_complete ?? result.coverage?.full_library_evaluated);

export function summarizeAnswer(result) {
  const judgments = result.judgments;
  if (!judgments || !searchComplete(result)) return [
    ['Can Jev help?', 'Assessment incomplete', 'No fit recommendation is available yet.'],
    ['What else is needed?', 'Not established', 'The available result does not support a complete design.'],
    ['Suggested next step', 'Retry the assessment', 'Review the error or missing evidence before acting on this result.']
  ];
  const fit = judgments.fit?.choice;
  const role = {choice: 'Choose between defined options.', noul: 'Judge a specific yes/no condition.', score: 'Rate supplied information against a rubric.', multiple: 'Combine several bounded decision types.', none: 'No suitable Jev decision was established.'}[judgments.primitive?.choice] || 'Its decision role still needs clarification.';
  const fitText = {conditional: 'Potential fit', boundary: 'Cannot cover the whole task', insufficient: 'Not enough evidence'}[fit] || 'Fit unclear';
  const likely = [], unclear = [];
  for (const [key, label] of [['generation_needed', 'Writing or summarization'], ['perception_needed', 'Image/audio understanding'], ['exact_code_needed', 'Application logic or actions']]) {
    const value = judgments[key]?.noul;
    if (typeof value !== 'number' || (value > .3 && value < .7)) unclear.push(label);
    else if (value >= .7) likely.push(label);
  }
  const next = fit === 'conditional' ? ['Prototype one decision', 'Use labeled examples to check errors before connecting real actions.'] :
    fit === 'boundary' ? ['Design the missing capabilities', 'Separate the core task from any smaller decision Jev could support.'] :
    ['Clarify the task', 'Specify the input, desired outcome and examples of a correct answer.'];
  return [
    ['Can Jev help?', fitText, fit === 'insufficient' ? 'The evidence does not yet support a specific integration.' : role],
    ['What else is needed?', likely.join(' · ') || 'Needs validation', (unclear.length ? 'Unclear: '+unclear.join(', ')+'. ' : '')+'These are design indications, not a validated architecture.'],
    ['Suggested next step', ...next]
  ];
}

// Messages safe to show visitors. Browser, proxy and parser errors never reach the page.
export class ServiceError extends Error {}
const OFFLINE = 'Connection interrupted. Check your connection and try again.';
const FAILED = 'Couldn’t complete this answer. Please retry.';
const TRANSIENT = new Set([408, 429, 500, 502, 503, 504]);
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

// CloudFront error pages are HTML; treat any unparseable body as absent.
export async function readReply(response) {
  try { return await response.json(); } catch { return null; }
}
function message(data, fallback) {
  return typeof data?.error === 'string' && data.error.trim() ? data.error : fallback;
}

export async function sendJson(url, body, fallback, fetcher = fetch) {
  let response;
  try {
    response = await fetcher(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body), signal: AbortSignal.timeout(30000)});
  } catch { throw new ServiceError(OFFLINE); }
  const data = await readReply(response);
  if (!response.ok || !data) throw new ServiceError(message(data, fallback));
  return data;
}

export async function startJob(idea, mode, fetcher = fetch) {
  const started = await sendJson('/api/jobs', {idea, mode}, 'Couldn’t start your answer. Please try again.', fetcher);
  if (typeof started.id !== 'string') throw new ServiceError('Couldn’t start your answer. Please try again.');
  return started.id;
}

// The server enforces the job deadline. Brief network or proxy failures are
// retried so a running answer is not abandoned and resubmitted against the daily limit.
export async function waitForJob(id, onProgress, {fetcher = fetch, sleep = pause, interval = 1500, maxMisses = 5} = {}) {
  let misses = 0;
  while (true) {
    let response = null, job = null;
    try {
      response = await fetcher('/api/jobs/'+id, {cache: 'no-store', signal: AbortSignal.timeout(30000)});
      job = await readReply(response);
    } catch {}
    if (response?.ok && job) {
      misses = 0;
      if (job.status === 'complete') { if (!job.result) throw new ServiceError(FAILED); return job.result; }
      if (job.status === 'failed') throw new ServiceError(message(job, FAILED));
      onProgress(job.progress || {});
    } else if (response && job && !TRANSIENT.has(response.status)) {
      throw new ServiceError(message(job, FAILED));
    } else if (++misses >= maxMisses) {
      throw new ServiceError('Connection interrupted while your answer was being prepared. Please retry.');
    }
    await sleep(interval * (misses + 1));
  }
}

export function progressMessage(p = {}) {
  const stage = p.stage || '';
  const total = Number(p.total), completed = Number(p.completed);
  const counted = Number.isFinite(total) && total > 0 && Number.isFinite(completed);
  const percent = counted ? ` ${Math.min(100, Math.max(0, Math.floor(100 * completed / total)))}%` : '';
  if (stage === 'Jev is testing the design') return 'Jev is running the proposed design on its examples…';
  if (stage === 'GLM is writing the explanation') return 'Jev assessment complete. GLM is drafting your design…';
  if (stage === 'Jev is assessing the selected evidence') return 'Research reviewed. Jev is forming your recommendation…';
  if (stage === 'Jev is checking the shortlisted research' || stage === 'Jev is evaluating every research passage') {
    return counted && completed >= total ? 'Research reviewed. Jev is forming your recommendation…' : 'Jev is reviewing the most relevant research…'+percent;
  }
  if (stage === 'Finding related research') return 'Finding related projects and research…';
  return 'Preparing your idea for review…';
}

const pct = value => `${Math.round(value * 100)}%`;
// One readable line per executed Jev answer, using only fields the API documents.
export function jevAnswerLines(answers = {}) {
  return Object.entries(answers).map(([id, a]) => {
    if (a?.type === 'noul' && Number.isFinite(a.noul)) return {id, type: 'Noul', text: `${pct(a.noul)} probability of yes`};
    if (a?.type === 'choice' && typeof a.choice === 'string') {
      const p = a.probabilities?.[a.choice];
      return {id, type: 'Choice', text: `${a.choice}${Number.isFinite(p) ? ` (${pct(p)})` : ''}${Number.isFinite(a.confidence) ? ` · confidence ${a.confidence.toFixed(2)}` : ''}`};
    }
    if (a?.type === 'score' && Number.isFinite(a.score)) {
      const top = Object.keys(a.legend || {}).length - 1;
      return {id, type: 'Score', text: `${a.score.toFixed(2)}${top > 0 ? ` on 0–${top}` : ''}${Number.isFinite(a.confidence) ? ` · confidence ${a.confidence.toFixed(2)}` : ''}`};
    }
    return {id, type: 'Answer', text: 'Unrecognized answer'};
  });
}

// Compare the design's expected application branch with what Jev actually returned.
// Only unambiguous links are compared; anything else stays "unknown" rather than guessed.
export function agreement(expected = {}, answers = {}, questions = {}) {
  const values = Object.values(expected || {});
  const notes = [];
  for (const [id, a] of Object.entries(answers)) {
    const q = questions[id] || {};
    if (a?.type === 'choice' && q.criteria && !Array.isArray(q.criteria)) {
      const wanted = values.find(v => typeof v === 'string' && Object.hasOwn(q.criteria, v));
      if (wanted !== undefined) notes.push({id, match: wanted === a.choice, expected: wanted, actual: a.choice});
    } else if (a?.type === 'noul' && typeof expected?.[id] === 'boolean') {
      notes.push({id, match: expected[id] === (a.noul >= .5), expected: String(expected[id]), actual: a.noul >= .5 ? 'true' : 'false'});
    }
  }
  return {status: !notes.length ? 'unknown' : notes.every(n => n.match) ? 'match' : 'differs', notes};
}
