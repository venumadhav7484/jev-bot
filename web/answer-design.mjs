// A failed or incomplete custom answer must never become an unrelated template.
export function exampleDesign(result) {
  const searched = result.coverage?.search_complete ?? result.coverage?.full_library_evaluated;
  if (!searched || !result.judgments || result.writer?.status !== 'success') return null;
  const design = result.writer.blueprint;
  if (!design) return null;
  const execution = result.execution?.status === 'complete' && result.execution.examples?.length === design.examples.length ? result.execution : null;
  return {...design, tailored: true, execution};
}

export const runCommand = `curl --fail-with-body https://api.typesafe.ai/v1/systemone \\
  -H "Authorization: Bearer $JEV_API_KEY" \\
  -H "Content-Type: application/json" \\
  --data-binary @request.json`;
