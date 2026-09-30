// Read an uploaded psychrometric chart in the visitor's browser. Nothing is uploaded to a server.
//  1. OCR (Tesseract.js, self-hosted under /vendor/tesseract) finds the chart's text and tick labels.
//  2. Code lines up the axes from the tick labels: a row of numbers along the bottom (dry-bulb) and a column
//     of numbers up the side (humidity ratio).
//  3. Code refines the fit by matching the chart's own printed RH curves to the equations. Many charts (ASHRAE,
//     FlyCarpet) slant their dry-bulb lines, so x = a + b·T + c·W + d·t·W, with W in kg/kg.
// Jev's part, reading the OCR text to decide the unit system and chart kind, is called by psychro.js.
import {P_SEA, pressureAt, wAt} from '/psychro-solver.mjs';

let workerPromise = null;

function loadScript(src) {
  return new Promise((resolve, reject) => {
    if (window.Tesseract) return resolve();
    const s = document.createElement('script'); s.src = src; s.onload = resolve; s.onerror = () => reject(new Error('Couldn’t load the chart reader.'));
    document.head.append(s);
  });
}

export function ocrWorker(onProgress) {
  if (!workerPromise) workerPromise = (async () => {
    await loadScript('/vendor/tesseract/tesseract.min.js');
    const worker = await window.Tesseract.createWorker('eng', 1, {
      workerPath: '/vendor/tesseract/worker.min.js', corePath: '/vendor/tesseract/core/tesseract-core-simd-lstm.wasm.js',
      langPath: '/vendor/tesseract/lang', workerBlobURL: false, gzip: true, logger: m => onProgress && onProgress(m)});
    await worker.setParameters({tessedit_pageseg_mode: '11'});   // sparse text: scattered chart labels
    return worker;
  })().catch(e => { workerPromise = null; throw e; });
  return workerPromise;
}

// Draw the image onto a canvas, upscaled so small tick labels are at least legible to OCR.
export function toCanvas(img, minWidth = 1600, maxWidth = 2600) {
  const w0 = img.naturalWidth || img.width, h0 = img.naturalHeight || img.height;
  const scale = Math.min(maxWidth / w0, Math.max(1, minWidth / w0));
  const c = document.createElement('canvas'); c.width = Math.round(w0 * scale); c.height = Math.round(h0 * scale);
  const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(img, 0, 0, c.width, c.height);
  return {canvas: c, scale};
}

// OCR copy of the canvas: keep only near-black pixels. Axis labels are usually black, while curves and grids are coloured
// or grey and otherwise confuse OCR badly.
export function blackMask(canvas, threshold) {
  const c = document.createElement('canvas'); c.width = canvas.width; c.height = canvas.height;
  const d = canvas.getContext('2d').getImageData(0, 0, c.width, c.height), p = d.data;
  for (let i = 0; i < p.length; i += 4) { const v = Math.max(p[i], p[i + 1], p[i + 2]) < threshold ? 0 : 255; p[i] = p[i + 1] = p[i + 2] = v; p[i + 3] = 255; }
  c.getContext('2d').putImageData(d, 0, 0);
  return c;
}

export async function ocr(canvas, onProgress) {
  const worker = await ocrWorker(onProgress);
  const {data} = await worker.recognize(canvas, {}, {text: true, blocks: true});
  const words = [];
  for (const b of data.blocks || []) for (const p of b.paragraphs || []) for (const l of p.lines || []) for (const w of l.words || []) words.push({text: w.text, conf: w.confidence, ...w.bbox});
  if (!words.length) for (const w of data.words || []) words.push({text: w.text, conf: w.confidence, ...w.bbox});
  return {text: data.text || words.map(w => w.text).join(' '), words};
}

export function numbersOf(words) {
  return words.map(w => {
    const t = w.text.replace(/[−–—]/g, '-').replace(/[,;:)]+$/, '').replace(/^[(]+/, '');
    const m = t.match(/^(-?\d+(?:\.\d+)?)$/);
    return m ? {v: +m[1], cx: (w.x0 + w.x1) / 2, cy: (w.y0 + w.y1) / 2, x0: w.x0, x1: w.x1, h: Math.max(4, w.y1 - w.y0)} : null;
  }).filter(Boolean);
}

// Largest set of numbers on one line (a row for the bottom axis, a column for the side axis) whose values map linearly
// onto position. pos = a + b·value.
function axisFit(nums, axis, tol) {
  const pos = axis === 'x' ? 'cx' : 'cy', along = n => (axis === 'x' ? n.cy : n.cx);
  const aligned = (p, q) => axis === 'x' ? Math.abs(p.cy - q.cy) < 0.8 * Math.max(p.h, q.h)
                                         : Math.abs(p.x0 - q.x0) < 0.8 * Math.max(p.h, q.h) || Math.abs(p.x1 - q.x1) < 0.8 * Math.max(p.h, q.h);
  let best = null;
  for (let i = 0; i < nums.length; i++) for (let j = i + 1; j < nums.length; j++) {
    const p = nums[i], q = nums[j];
    if (p.v === q.v || !aligned(p, q)) continue;
    const b = (q[pos] - p[pos]) / (q.v - p.v);
    if (axis === 'x' ? b <= 0 : b >= 0) continue;          // x grows rightwards; the side axis grows upwards
    const a = p[pos] - b * p.v, inl = nums.filter(n => aligned(p, n) && Math.abs(n[pos] - (a + b * n.v)) < tol);
    const values = new Set(inl.map(n => n.v));
    const score = values.size + (axis === 'x' ? along(p) * 1e-6 : p.cx * 1e-6);   // tie-break: lowest row / rightmost column
    if (values.size >= 4 && (!best || score > best.score)) best = {score, inliers: inl};
  }
  if (!best) return null;
  const pts = best.inliers, n = pts.length, mv = pts.reduce((s, p) => s + p.v, 0) / n, mp = pts.reduce((s, p) => s + p[pos], 0) / n;
  const b = pts.reduce((s, p) => s + (p.v - mv) * (p[pos] - mp), 0) / pts.reduce((s, p) => s + (p.v - mv) ** 2, 0);
  const vals = pts.map(p => p.v);
  return {a: mp - b * mv, b, min: Math.min(...vals), max: Math.max(...vals), count: new Set(vals).size, inliers: pts};
}

// Both axes from OCR words, or null. Used to pick the best OCR pass before the full fit.
export function findAxes(words, width) {
  const nums = numbersOf(words), tol = Math.max(5, width / 160);
  const xAxis = axisFit(nums, 'x', tol);
  if (!xAxis) return null;
  const yAxis = axisFit(nums.filter(n => !xAxis.inliers.includes(n)), 'y', tol);
  return yAxis ? {xAxis, yAxis, score: xAxis.count + yAxis.count} : {xAxis, yAxis: null, score: xAxis.count};
}

export function findPressure(text) {
  const t = text.replace(/,/g, '');
  let m = t.match(/pressure[^0-9]{0,12}([0-9]+(?:\.[0-9]+)?)\s*(kpa|pa|psia|psi|in\.?\s*hg|inhg|mbar|hpa|bar)/i);
  if (m) {
    const v = +m[1], u = m[2].toLowerCase().replace(/\s|\./g, '');
    const pa = {pa: v, kpa: v * 1000, psia: v * 6894.757, psi: v * 6894.757, inhg: v * 3386.389, mbar: v * 100, hpa: v * 100, bar: v * 1e5}[u];
    if (pa > 50000 && pa < 110000) return {pa, source: 'read from the chart'};
  }
  m = t.match(/(?:altitude|elevation)[^0-9]{0,12}([0-9]+(?:\.[0-9]+)?)\s*(m|ft|feet)\b/i);
  if (m) { const z = +m[1] * (m[2].toLowerCase() === 'm' ? 1 : 0.3048); if (z < 5000) return {pa: pressureAt(z), source: 'from the altitude on the chart'}; }
  return {pa: P_SEA, source: 'not stated on the chart, so sea level is assumed'};
}

// Ink map: how far each pixel is from white, max-filtered over 3×3 so antialiased 1-px lines are found.
function inkMap(canvas) {
  const {width: W, height: H} = canvas, d = canvas.getContext('2d').getImageData(0, 0, W, H).data, ink = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) ink[i] = 1 - Math.min(d[4 * i], d[4 * i + 1], d[4 * i + 2]) / 255 * 0.5 - (d[4 * i] + d[4 * i + 1] + d[4 * i + 2]) / 765 * 0.5;
  const out = new Float32Array(W * H);
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    let m = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) m = Math.max(m, ink[(y + dy) * W + x + dx]);
    out[y * W + x] = m;
  }
  return {W, H, at: (x, y) => (x < 0 || y < 0 || x >= W || y >= H ? 0 : out[(y | 0) * W + (x | 0)])};
}

// Geometry in canvas pixels. x = xa + xb·T(t) + c·w + d·t·w; y = ya + yb·Y(w). T: °C or °F; Y: g/kg, gr/lb or kg/kg.
export function geometry(fit) {
  const {xa, xb, ya, yb, c, d, ip, yUnit} = fit;
  const T = t => (ip ? t * 1.8 + 32 : t), Y = {g: w => w * 1000, gr: w => w * 7000, kg: w => w}[yUnit], Yinv = {g: v => v / 1000, gr: v => v / 7000, kg: v => v}[yUnit];
  return {
    toPx: (t, w) => [xa + xb * T(t) + c * w + d * t * w, ya + yb * Y(w)],
    fromPx: (x, y) => { const w = Yinv((y - ya) / yb); const t = ip ? (x - xa - 32 * xb - c * w) / (1.8 * xb + d * w) : (x - xa - c * w) / (xb + d * w); return [t, w]; },
  };
}

// Full pipeline on a canvas: OCR → axes → curve match. Returns {fit, geometry, text, report} or throws with a visitor message.
export async function readChart(canvas, {units = 'SI units', onStep = () => {}, words = null, text = null} = {}) {
  if (!words) { onStep('ocr'); ({words, text} = await ocr(canvas)); }
  const axes = findAxes(words, canvas.width);
  if (!axes) throw new Error('Couldn’t find the temperature scale along the bottom of this chart.');
  if (!axes.yAxis) throw new Error('Couldn’t find the humidity-ratio scale up the side of this chart.');
  const {xAxis, yAxis} = axes;
  const ip = units === 'IP units', yUnit = yAxis.max <= 0.06 ? 'kg' : ip && yAxis.max > 40 ? 'gr' : 'g';
  const pressure = findPressure(text || '');
  const fit = {xa: xAxis.a, xb: xAxis.b, ya: yAxis.a, yb: yAxis.b, c: 0, d: 0, ip, yUnit, p: pressure.pa};
  // Curve match: slide the slant terms (c, d) and a small offset so the equations' RH curves sit on the chart's ink.
  onStep('match');
  const ink = inkMap(canvas), tLo = ip ? (xAxis.min - 32) / 1.8 : xAxis.min, tHi = ip ? (xAxis.max - 32) / 1.8 : xAxis.max;
  const wHi = {g: yAxis.max / 1000, gr: yAxis.max / 7000, kg: yAxis.max}[yUnit];
  const samples = [];
  for (const rh of [0.2, 0.4, 0.6, 0.8, 1.0]) for (let t = tLo; t <= tHi; t += (tHi - tLo) / 120) { const w = wAt(t, 'rh', rh, fit.p); if (w > 0 && w <= wHi) samples.push([t, w]); }
  const score = f => { const g = geometry(f); let s = 0; for (const [t, w] of samples) { const [x, y] = g.toPx(t, w); s += ink.at(x, y); } return s / samples.length; };
  const span = xAxis.b * (ip ? 1.8 : 1) * 60 / wHi;                       // pixel scale for the slant search
  let best = {...fit, s: score(fit)};
  for (let c = -2 * span; c <= 0.6 * span; c += span / 40) for (let d = -0.02 * span; d <= 0.05 * span; d += span / 2000) {
    const f = {...fit, c, d}, s = score(f); if (s > best.s) best = {...f, s};
  }
  // Coordinate refinement with halving steps: offsets to 1/16 px, slant terms to fine resolution.
  for (let round = 0; round < 5; round++) for (const k of ['xa', 'ya', 'c', 'd', 'xb', 'yb']) {
    const step = {xa: 1, ya: 1, c: span / 100, d: span / 5000, xb: fit.xb / 400, yb: fit.yb / 400}[k] / 2 ** round;
    for (let i = -8; i <= 8; i++) { const f = {...best, [k]: best[k] + i * step}, s = score(f); if (s > best.s) best = {...f, s}; }
  }
  let base = 0; for (let i = 0; i < 400; i++) base += ink.at(Math.random() * canvas.width, Math.random() * canvas.height); base /= 400;
  const report = {xRange: [xAxis.min, xAxis.max], xLabels: xAxis.count, yRange: [yAxis.min, yAxis.max], yLabels: yAxis.count, yUnit, ip,
                  pressure, curveInk: best.s, backgroundInk: base, matchRatio: best.s / Math.max(base, 1e-3)};
  return {fit: best, geometry: geometry(best), text, words, report};
}
