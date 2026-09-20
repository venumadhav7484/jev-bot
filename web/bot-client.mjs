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

export function summarizeAnswer(result) {
  const judgments = result.judgments;
  if (!judgments || !result.coverage?.full_library_evaluated) return [
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
