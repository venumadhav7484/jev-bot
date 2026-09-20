// A failed or incomplete custom answer must never become an unrelated template.
export function exampleDesign(result) {
  if (!result.coverage?.full_library_evaluated || !result.judgments || result.writer?.status !== 'success') return null;
  const design = result.writer.blueprint;
  return design ? {...design, tailored: true} : null;
}

export const runCommand = `curl --fail-with-body https://api.typesafe.ai/v1/systemone \\
  -H "Authorization: Bearer $JEV_API_KEY" \\
  -H "Content-Type: application/json" \\
  --data-binary @request.json`;
