export const MAX_IDEA_CHARS = 6000;
export async function importIdeaFile(file, current = '') {
  if (!/\.(txt|md|csv|json)$/i.test(file.name)) throw new Error('Choose a TXT, MD, CSV or JSON text file. PDF, Word and images are not supported yet.');
  if (file.size > 256 * 1024) throw new Error('File exceeds 256 KB. Attach a shorter text excerpt.');
  let text;
  try { text = new TextDecoder('utf-8', {fatal: true}).decode(await file.arrayBuffer()).replace(/^\uFEFF/, '').trim(); }
  catch { throw new Error('Could not read this file as UTF-8 text. Export it as a text file and retry.'); }
  if (!text || /[\x00-\x08\x0B\x0C\x0E-\x1F]/.test(text)) throw new Error('File is empty or contains binary data. Choose a plain-text file.');
  const combined = [current.trim(), text].filter(Boolean).join('\n\n');
  if ([...combined].length > MAX_IDEA_CHARS) throw new Error('Combined text exceeds 6,000 characters. Use a shorter excerpt; nothing was imported.');
  return combined;
}
