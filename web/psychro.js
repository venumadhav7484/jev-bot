// /psychro-data: upload (or pick) a psychrometric chart; the page reads it on the visitor's device (psychro-upload.mjs),
// Jev reads the chart's OCR text and the visitor's question (POST /api/psychro), and the page computes all seven
// properties exactly (psychro-solver.mjs) and plots them on the chart. Clicking the chart needs no AI at all.
import {P_SEA, PROPS, StateError, pressureAt, solve, state, toSI, wAt} from '/psychro-solver.mjs';
import {blackMask, findAxes, ocr, readChart, toCanvas} from '/psychro-upload.mjs';

const $ = id => document.getElementById(id);
const NS = 'http://www.w3.org/2000/svg';
const node = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const svg = (tag, attrs = {}, text) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); if (text != null) e.textContent = text; return e; };
const MAX = 300, MAX_BYTES = 12e6;
const NAMES = {tdb: 'Dry-bulb temperature', twb: 'Wet-bulb temperature', tdp: 'Dew-point temperature', rh: 'Relative humidity',
               w: 'Humidity ratio', h: 'Specific enthalpy', v: 'Specific volume'};
const EXAMPLES = ['DB 30 °C, WB 22 °C → dew point?', 'measured 30 degrees and 60% humidity in the server room, what’s the dew point?',
  'Moist air has a dry-bulb temperature of 86 °F and a relative humidity of 40%. Find the enthalpy.',
  'RH 55%, DP 14 C. Need WB and W.', 'enthalpy 58 kJ/kg and humidity 70% — what’s the air temperature?', 'Tdb 24, W 9.5 g/kg -> rest of the properties?'];
const ALTITUDES = [['sea', 'Sea level · 101,325 Pa', 0], ['z540', '≈ 540 m (e.g. Hyderabad)', 540], ['z920', '≈ 920 m (e.g. Bengaluru)', 920],
                   ['z1500', '1,500 m', 1500], ['z2200', '≈ 2,200 m (e.g. Shimla)', 2200]];
const pa = p => Math.round(p).toLocaleString('en-US') + ' Pa';

// Sample chart: FlyCarpet's sea-level SI chart with its exact calibration (experiments/psychrometric-charts/src/chart_check.py).
const FLY = [196.50819040671797, 12.650652248307082, -1135.1876243472282, 22.660842737203765];
const flyGeom = {
  toPx: (t, w) => [FLY[0] + FLY[1] * t + FLY[2] * w + FLY[3] * t * w, 590 - 18000 * w],
  fromPx: (x, y) => { const w = (590 - y) / 18000; return [(x - FLY[0] - FLY[2] * w) / (FLY[1] + FLY[3] * w), w]; },
};
const drawnGeom = {toPx: (t, w) => [70 + (t + 10) * 760 / 60, 590 - 18000 * w], fromPx: (x, y) => [(x - 70) * 60 / 760 - 10, (590 - y) / 18000]};

let source = null, pressure = P_SEA, reading = null, clicked = null, seq = 0, overlay = null, readSeq = 0;

function fmt(prop, s) {
  const x = s[prop];
  switch (prop) {
    case 'tdb': case 'twb': case 'tdp': return [x.toFixed(1) + ' °C', (x * 1.8 + 32).toFixed(1) + ' °F'];
    case 'rh': return [(x * 100).toFixed(1) + ' %', ''];
    case 'w': return [(x * 1000).toFixed(2) + ' g/kg', (x * 7000).toFixed(1) + ' gr/lb'];
    case 'h': return [x.toFixed(1) + ' kJ/kg', ''];
    default: return [x.toFixed(3) + ' m³/kg', (x * 16.018463).toFixed(2) + ' ft³/lb'];
  }
}

// ---------- a chart drawn from the equations (any pressure) ----------
function drawnChart(p) {
  const g = drawnGeom, root = svg('svg', {viewBox: '0 0 902 652', role: 'img', 'aria-label': 'Psychrometric chart drawn from the equations at ' + Math.round(p) + ' Pa'});
  root.append(svg('rect', {width: 902, height: 652, fill: '#fff'}));
  const sat = []; for (let t = -10; t <= 50.001; t += 0.25) { const w = wAt(t, 'rh', 1, p); if (w > 0.030) break; sat.push([t, w]); }
  const [tTop] = sat[sat.length - 1];
  const region = [...sat.map(([t, w]) => g.toPx(t, w)), g.toPx(tTop, 0.030), g.toPx(50, 0.030), g.toPx(50, 0), g.toPx(-10, 0)];
  const clip = svg('clipPath', {id: 'under-sat'}); clip.append(svg('polygon', {points: region.map(q => q.join(',')).join(' ')}));
  const defs = svg('defs'); defs.append(clip); root.append(defs);
  const grid = svg('g', {stroke: '#9CA3AF', 'stroke-width': 0.8, 'stroke-dasharray': '4,4', 'clip-path': 'url(#under-sat)'});
  for (let t = -10; t <= 50; t += 5) grid.append(svg('line', {x1: g.toPx(t, 0)[0], y1: 590, x2: g.toPx(t, 0.03)[0], y2: 50}));
  for (let w = 0.002; w <= 0.0301; w += 0.002) grid.append(svg('line', {x1: 70, y1: g.toPx(0, w)[1], x2: 830, y2: g.toPx(0, w)[1]}));
  root.append(grid);
  const curve = (f, from, to, step = 0.5) => { const pts = []; for (let t = from; t <= to + 1e-9; t += step) { const w = f(t); if (w >= -0.001 && w <= 0.0312) pts.push(g.toPx(t, w).map(n => n.toFixed(1)).join(',')); } return pts.join(' '); };
  const lines = svg('g', {fill: 'none', 'clip-path': 'url(#under-sat)'});
  for (let h = -10; h <= 120; h += 10) lines.append(svg('polyline', {points: curve(t => (h - 1.006 * t) / (2501 + 1.86 * t), -10, 50, 5), stroke: '#15803D', 'stroke-width': 1}));
  for (let v = 0.76; v <= 0.961; v += 0.02) lines.append(svg('polyline', {points: curve(t => wAt(t, 'v', v, p), -10, 50, 1), stroke: '#0F766E', 'stroke-width': 1, 'stroke-dasharray': '14,7'}));
  for (let wb = -10; wb <= 35; wb += 5) lines.append(svg('polyline', {points: curve(t => (t >= wb ? wAt(t, 'twb', wb, p) : NaN), wb, 50, 1), stroke: '#6B7280', 'stroke-width': 0.8, 'stroke-dasharray': '3,4'}));
  for (let r = 0.1; r <= 0.91; r += 0.1) lines.append(svg('polyline', {points: curve(t => wAt(t, 'rh', r, p), -10, 50, 0.5), stroke: '#991B1B', 'stroke-width': 1}));
  root.append(lines);
  root.append(svg('polyline', {points: sat.map(([t, w]) => g.toPx(t, w).join(',')).join(' '), fill: 'none', stroke: '#111827', 'stroke-width': 2}));
  const axes = svg('g', {stroke: '#111827', 'stroke-width': 1.5, fill: 'none'});
  axes.append(svg('line', {x1: 70, y1: 590, x2: 830, y2: 590}), svg('line', {x1: 830, y1: 590, x2: 830, y2: 50}));
  root.append(axes);
  const text = svg('g', {'font-family': 'Helvetica, Arial, sans-serif', 'font-size': 13, fill: '#111827'});
  for (let t = -10; t <= 50; t += 5) text.append(svg('text', {x: g.toPx(t, 0)[0], y: 608, 'text-anchor': 'middle'}, String(t)));
  for (let w = 0; w <= 30; w += 2) text.append(svg('text', {x: 838, y: g.toPx(0, w / 1000)[1] + 4}, String(w)));
  for (let r = 10; r <= 90; r += 20) { const t = 36 - r / 10; const [x, y] = g.toPx(t, wAt(t, 'rh', r / 100, p)); if (y > 58) text.append(svg('text', {x: x + 4, y: y - 4, fill: '#991B1B', 'font-size': 12}, r + '%')); }
  text.append(svg('text', {x: 450, y: 632, 'text-anchor': 'middle', 'font-weight': 700}, 'Dry-bulb temperature, °C · Pressure = ' + Math.round(p).toLocaleString('en-US') + ' Pa'));
  text.append(svg('text', {x: 880, y: 320, 'text-anchor': 'middle', 'font-weight': 700, transform: 'rotate(90 880 320)'}, 'Humidity ratio, g/kg dry air'));
  text.append(svg('text', {x: 80, y: 70, fill: '#4B5563', 'font-size': 12}, 'Green: enthalpy every 10 kJ/kg · teal dashed: volume every 0.02 m³/kg · grey dotted: wet-bulb every 5 °C'));
  root.append(text);
  return root;
}

// ---------- chart sources ----------
function setSource(next) {
  source = next; clicked = null;
  const wrap = $('chart-wrap'); wrap.replaceChildren();
  if (source.svg) wrap.append(source.svg); else { const img = node('img'); img.src = source.src; img.alt = source.alt; img.width = source.w; img.height = source.h; wrap.append(img); }
  overlay = svg('svg', {class: 'overlay', viewBox: `0 0 ${source.w} ${source.h}`, preserveAspectRatio: 'none', 'aria-hidden': 'true'});
  overlay.addEventListener('click', onChartClick);
  wrap.append(overlay);
  $('chart-credit').replaceChildren(...source.credit);
  renderPressure();
  redraw();
}

function useSample() {
  readSeq++;
  const ol = $('steps'); ol.hidden = false; ol.replaceChildren();
  const li = node('li', 'cta'); const b = Object.assign(node('button', 'primary', '▶ Read this chart like an upload'), {type: 'button', onclick: () => readSample()});
  li.append(b, node('span', 'hint', 'OCR on your device → Jev reads the chart text → axes lined up → checked against the equations'));
  ol.append(li);
  setSource({kind: 'sample', src: '/psychro-flycarpet.svg', alt: 'Sea-level psychrometric chart (SI) by FlyCarpet Inc', w: 902, h: 652, geom: flyGeom, range: {t: [-10, 50], w: 0.030},
             chartP: P_SEA, chartPNote: 'stated on the chart', credit: ['Sample chart © FlyCarpet Inc, ', Object.assign(node('a', null, 'flycarpet.net/en/psyonline'), {href: 'https://www.flycarpet.net/en/psyonline', rel: 'noopener'}),
             ', used with credit. Ask a question or click anywhere on it.']});
}

function useDrawn(id) {
  const [, label, z] = ALTITUDES.find(a => a[0] === id), p = pressureAt(z);
  $('steps').hidden = true; readSeq++;
  setSource({kind: 'drawn', svg: drawnChart(p), w: 902, h: 652, geom: drawnGeom, range: {t: [-10, 50], w: 0.030}, chartP: p, chartPNote: label,
             credit: ['Drawn by this page from the ASHRAE equations at ' + pa(p) + ' (' + label + ').']});
}

function renderPressure() {
  const sel = $('pressure'); sel.replaceChildren();
  const chartOpt = node('option', null, 'From the chart: ' + pa(source.chartP) + ' (' + source.chartPNote + ')'); chartOpt.value = 'chart'; sel.append(chartOpt);
  ALTITUDES.forEach(([id, label, z]) => { const o = node('option', null, label + ' · ' + pa(pressureAt(z))); o.value = id; sel.append(o); });
  sel.value = 'chart'; pressure = source.chartP;
}

// ---------- reading an uploaded chart ----------
function steps(list) {
  const ol = $('steps'); ol.hidden = false; ol.replaceChildren();
  return list.map(([key, text]) => { const li = node('li'); li.dataset.key = key; li.append(node('span', 'ic', '·'), Object.assign(node('span'), {textContent: text})); ol.append(li); return li; });
}
function mark(li, state, detail) {
  li.className = state; li.querySelector('.ic').textContent = {run: '…', done: '✓', fail: '✗', warn: '!'}[state];
  const body = li.children[1]; body.querySelector('small')?.remove(); if (detail) body.append(node('small', null, detail));
}

async function readImage(img, meta) {
  const mine = ++readSeq;
  const [s1, s2, s3, s4] = steps([['ocr', 'Reading the chart’s text on your device'], ['jev', 'Jev: what kind of chart, which units'],
                                  ['axes', 'Lining up the axes from the tick labels'], ['check', 'Checking the fit against the equations’ RH curves']]);
  const t0 = performance.now();
  try {
    mark(s1, 'run', 'Loading the reader (first time about 7 MB)…');
    const {canvas, scale} = toCanvas(img, 1800, 2600);
    // Several OCR passes: black-only masks first (labels are usually black; coloured curves confuse OCR), then the raw image.
    let found = null;
    // Mask thresholds: 110 suits crisp images; 140–170 recover labels that upscaling a small image has blurred and lightened.
    const passes = [110, 140, 170, 80, null];
    for (const [i, thr] of passes.entries()) {
      const pass = await ocr(thr ? blackMask(canvas, thr) : canvas, m => { if (mine === readSeq && m.status) mark(s1, 'run', 'Pass ' + (i + 1) + ' of ' + passes.length + ' · ' + m.status + (m.progress ? ' · ' + Math.round(m.progress * 100) + '%' : '')); });
      if (mine !== readSeq) return;
      pass.axes = findAxes(pass.words, canvas.width);
      if (!found || (pass.axes?.score || 0) > (found.axes?.score || 0)) found = pass;
      if (found.axes?.yAxis && found.axes.xAxis.count >= 5 && found.axes.yAxis.count >= 5) break;
    }
    mark(s1, 'done', found.words.length + ' words and numbers found · ' + ((performance.now() - t0) / 1000).toFixed(1) + ' s');
    mark(s2, 'run');
    const res = await fetch('/api/psychro', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({chart_text: found.text.slice(0, 3000)})});
    const jev = await res.json().catch(() => ({}));
    if (mine !== readSeq) return;
    if (!res.ok) { mark(s2, 'fail', jev.error || 'Jev couldn’t read the chart text right now.'); return; }
    mark(s2, 'done', jev.kind + ' (' + Math.round((jev.kind_confidence ?? 0) * 100) + '%) · ' + jev.units + ' (' + Math.round((jev.units_confidence ?? 0) * 100) + '%) · ' + jev.seconds.toFixed(2) + ' s');
    // Jev's verdict stops the reading only when it is confident; otherwise the axes and the curve check decide.
    if (jev.kind !== 'psychrometric chart' && (jev.kind_confidence ?? 0) >= 0.7) {
      mark(s3, 'fail', jev.kind === 'Mollier diagram' ? 'Mollier diagrams aren’t supported yet. Try a chart with dry-bulb along the bottom.' : 'This doesn’t look like a psychrometric chart. Try another image.');
      return;
    }
    const xr = found.axes?.xAxis, units = (jev.units_confidence ?? 0) >= 0.6 ? jev.units : (xr && xr.min >= 20 && xr.max >= 90 ? 'IP units' : 'SI units');
    mark(s3, 'run');
    let result;
    try { result = await readChart(canvas, {units, words: found.words, text: found.text, onStep: k => k === 'match' && mark(s4, 'run')}); }
    catch (e) { mark(s3, 'fail', e.message + ' Try a sharper, straight-on image.'); return; }
    if (mine !== readSeq) return;
    const r = result.report, ip = r.ip;
    mark(s3, 'done', 'Dry-bulb ' + r.xRange[0] + '…' + r.xRange[1] + (ip ? ' °F' : ' °C') + ' (' + r.xLabels + ' labels) · humidity ratio ' + r.yRange[0] + '…' + r.yRange[1] +
         ' ' + {g: 'g/kg', gr: 'gr/lb', kg: 'kg/kg'}[r.yUnit] + ' (' + r.yLabels + ' labels)');
    const good = r.matchRatio >= 2;
    const g = result.geometry, geom = {toPx: (t, w) => g.toPx(t, w).map(v => v / scale), fromPx: (x, y) => g.fromPx(x * scale, y * scale)};
    let extra = '';
    if (meta.truth) {   // the sample chart has an exact calibration, so show how close the automatic reading got
      let dt = 0, dw = 0;
      for (let t = 0; t <= 45; t += 5) for (let w = 0.002; w <= 0.024; w += 0.004) { const [x, y] = meta.truth.toPx(t, w), [t2, w2] = geom.fromPx(x, y); dt = Math.max(dt, Math.abs(t2 - t)); dw = Math.max(dw, Math.abs(w2 - w) * 1000); }
      extra = ' · vs the exact calibration: within ' + dt.toFixed(2) + ' °C and ' + dw.toFixed(2) + ' g/kg';
    }
    const assumed = /assumed/.test(r.pressure.source);
    mark(s4, good && !assumed ? 'done' : 'warn', (good ? 'The equations’ RH curves (teal, dashed) should sit on the chart’s own curves' : 'The curves only partly line up. Answers are still exact, but the plotted point may be off')
         + ' (match ' + r.matchRatio.toFixed(1) + '× background)' + extra
         + (assumed ? '. The pressure isn’t printed on this chart, so sea level is assumed. If your chart is for another altitude, pick it under the chart and check that the dashed curves line up.' : ''));
    const toC = v => (ip ? (v - 32) / 1.8 : v), toKg = v => ({g: v / 1000, gr: v / 7000, kg: v}[r.yUnit]);
    setSource({...meta, geom, range: {t: [toC(r.xRange[0]), toC(r.xRange[1])], w: toKg(r.yRange[1])}, chartP: r.pressure.pa, chartPNote: r.pressure.source, credit: meta.credit});
    $('show-curves').checked = true; redraw();
  } catch (e) {
    if (mine === readSeq) mark(s1, 'fail', (e && e.message) || 'The chart reader failed in this browser.');
  }
}

function readSample() {
  const img = new Image(); img.onload = () => readImage(img, {kind: 'sample', src: '/psychro-flycarpet.svg', alt: 'Sea-level psychrometric chart (SI) by FlyCarpet Inc', w: 902, h: 652, truth: flyGeom,
    credit: ['Sample chart © FlyCarpet Inc, ', Object.assign(node('a', null, 'flycarpet.net/en/psyonline'), {href: 'https://www.flycarpet.net/en/psyonline', rel: 'noopener'}), ', read automatically on your device.']});
  img.src = '/psychro-flycarpet.svg';
}

function readFile(file) {
  if (!file) return;
  if (!/^image\/(png|jpeg|webp|svg\+xml)$/.test(file.type)) return status('Use a PNG, JPEG, WebP or SVG image of a psychrometric chart.', 'err');
  if (file.size > MAX_BYTES) return status('That image is larger than 12 MB. Use a smaller screenshot.', 'err');
  status('');
  const url = URL.createObjectURL(file), img = new Image();
  img.onload = () => {
    const meta = {kind: 'upload', src: url, alt: 'Your uploaded chart', w: img.naturalWidth, h: img.naturalHeight, credit: ['Your chart: ' + file.name + ', read on your device and not uploaded.']};
    setSource({...meta, geom: null, chartP: P_SEA, chartPNote: 'until the chart is read'});
    readImage(img, meta);
  };
  img.onerror = () => status('Couldn’t open that image.', 'err');
  img.src = url;
}

// ---------- overlay: point, guides, equations' curves ----------
function redraw() {
  if (!overlay) return;
  overlay.replaceChildren();
  const g = source.geom;
  if (!g) return;
  if ($('show-curves').checked) {
    const grp = svg('g', {fill: 'none', stroke: '#0D9488', 'stroke-width': Math.max(1.5, source.w / 500), 'stroke-dasharray': '8,5', opacity: 0.9});
    for (const rh of [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) {
      const [t0, t1] = source.range.t, wMax = source.range.w;
      const pts = []; for (let t = t0; t <= t1 + 1e-9; t += (t1 - t0) / 240) { const w = wAt(t, 'rh', rh, pressure); if (w < 0 || w > wMax) continue; const [x, y] = g.toPx(t, w); pts.push(x.toFixed(1) + ',' + y.toFixed(1)); }
      if (pts.length > 1) grp.append(svg('polyline', {points: pts.join(' ')}));
    }
    overlay.append(grp);
  }
  const s = clicked ? stateAt(clicked) : reading?.state;
  if (!s) return;
  const [x, y] = g.toPx(s.tdb, s.w);
  if (!(x >= 0 && x <= source.w && y >= 0 && y <= source.h)) {
    overlay.append(svg('text', {x: source.w / 2, y: 40, 'text-anchor': 'middle', 'font-size': source.w / 50, fill: '#B45309', 'font-weight': 700}, 'This state is off the chart’s range'));
    return;
  }
  const [xb, yb] = g.toPx(s.tdb, 0), [xr, yr] = g.toPx(s.tdb + 200, s.w), k = source.w / 900;
  const guide = {stroke: '#0F766E', 'stroke-width': 2 * k, 'stroke-dasharray': `${6 * k},${4 * k}`};
  overlay.append(svg('line', {x1: x, y1: y, x2: xb, y2: Math.min(yb, source.h), ...guide}), svg('line', {x1: x, y1: y, x2: source.w, y2: y + (yr - y) * (source.w - x) / Math.max(1, xr - x), ...guide}));
  overlay.append(svg('circle', {cx: x, cy: y, r: 9 * k, fill: '#2DD4BF', stroke: '#062A26', 'stroke-width': 3 * k}));
  const label = s.tdb.toFixed(1) + ' °C · ' + (s.w * 1000).toFixed(1) + ' g/kg · ' + Math.round(s.rh * 100) + '% RH';
  const lx = Math.min(x + 14 * k, source.w - label.length * 7.4 * k - 10 * k), ly = Math.max(y - 14 * k, 30 * k);
  overlay.append(svg('rect', {x: lx - 6 * k, y: ly - 17 * k, width: (label.length * 7.4 + 12) * k, height: 24 * k, rx: 6 * k, fill: '#0B0D12', opacity: 0.85}));
  overlay.append(svg('text', {x: lx, y: ly, fill: '#fff', 'font-size': 14 * k, 'font-weight': 700, 'font-family': 'Helvetica, Arial, sans-serif'}, label));
}

function stateAt([t, w]) { try { return state(t, w, pressure); } catch { return null; } }

// ---------- results ----------
function showAnswer(s, given = [], highlight = null, note = '') {
  const card = node('div', 'card'), meta = node('div', 'meta');
  meta.append(node('span', 'pill live', 'COMPUTED'), node('span', null, 'Exact, from the equations at ' + pa(pressure) + (note ? ' · ' + note : '')));
  const table = node('table', 'answer-table'), body = node('tbody');
  const hl = highlight === 'all' ? PROPS.filter(p => !given.includes(p)) : highlight ? [highlight] : [];
  for (const p of PROPS) {
    const tr = node('tr', hl.includes(p) ? 'hl' : ''), [v, alt] = fmt(p, s), name = node('td', null, NAMES[p]);
    if (given.includes(p)) name.append(node('span', 'tag-given', 'GIVEN'));
    tr.append(name, node('td', 'v', v), node('td', 'alt', alt)); body.append(tr);
  }
  table.append(body); card.append(meta, table);
  $('answer').replaceChildren(card);
  redraw();
}

function showError(message) {
  const card = node('div', 'card err-card'); card.append(node('p', null, message));
  $('answer').replaceChildren(card);
  if (reading) reading.state = null;
  redraw();
}

function compute() {
  if (clicked) { const s = stateAt(clicked); return s ? showAnswer(s, [], null, 'clicked point') : showError('That point is above the saturation curve at this pressure.'); }
  if (!reading) return;
  const [a, b] = reading.numbers, si = reading.numbers.map(n => toSI(n.label, n.value, n.unit));
  const bad = reading.numbers.find((n, i) => si[i] === null);
  if (bad) return showError('“' + bad.raw + '” can’t be a ' + NAMES[bad.label].toLowerCase() + '. Pick another property for it.');
  try { reading.state = solve([a.label, si[0]], [b.label, si[1]], pressure); showAnswer(reading.state, [a.label, b.label], reading.highlight); }
  catch (e) { if (e instanceof StateError) showError(e.message); else throw e; }
}

function renderReading(r) {
  const card = node('div', 'card live'), meta = node('div', 'meta');
  meta.append(node('span', 'pill live', 'JEV READ'), node('span', null, r.model), node('span', null, r.seconds.toFixed(2) + ' s'),
              node('span', null, r.usd != null ? '$' + r.usd.toFixed(6) : 'cost not reported'));
  card.append(meta, node('p', 'hint', 'Wrong? Change it here and the answer updates instantly, no new request.'));
  r.numbers.forEach(n => {
    const row = node('div', 'reading-row'), sel = node('select');
    (n.source === 'unit' ? [n.label] : n.options).forEach(p => { const o = node('option', null, NAMES[p]); o.value = p; sel.append(o); });
    sel.value = n.label; sel.disabled = n.source === 'unit'; sel.setAttribute('aria-label', 'Property for ' + n.raw);
    sel.addEventListener('change', () => { n.label = sel.value; compute(); });
    const who = node('span', 'who');
    if (n.source === 'unit') who.append('set by the unit'); else who.append(node('b', null, 'Jev ' + Math.round((n.confidence ?? 0) * 100) + '%'));
    const chip = node('span', 'chip', n.raw); chip.dir = 'auto';
    row.append(chip, sel, who); card.append(row);
  });
  const row = node('div', 'reading-row'), sel = node('select');
  [...PROPS.map(p => [p, NAMES[p]]), ['all', 'All the other properties']].forEach(([k, t]) => { const o = node('option', null, t); o.value = k; sel.append(o); });
  sel.value = r.highlight; sel.setAttribute('aria-label', 'Property you asked for');
  sel.addEventListener('change', () => { r.highlight = sel.value; compute(); });
  row.append(node('span', 'chip', 'You asked for'), sel, node('span', 'who', 'highlight only'));
  card.append(row);
  $('reading').replaceChildren(card);
}

function status(message, kind = '') { const s = $('status'); s.className = 'status ' + kind; s.replaceChildren(...(Array.isArray(message) ? message : [message])); }
const retryButton = () => Object.assign(node('button', 'ghost retry', 'Try again'), {type: 'button', onclick: ask});

async function ask() {
  const text = $('text').value.trim();
  if (!text || text.length > MAX) return;
  const mine = ++seq;
  reading = null; clicked = null;
  $('reading').replaceChildren(); $('answer').replaceChildren(); redraw();      // clear the previous result immediately
  status([node('span', 'spin'), 'Jev is reading your question…']);
  $('run').disabled = true;
  const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 30000);
  try {
    const res = await fetch('/api/psychro', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text}), signal: controller.signal});
    const data = await res.json().catch(() => ({}));
    if (mine !== seq) return;
    if (!res.ok) return status([data.error || 'Jev couldn’t read this right now.', ...(res.status !== 400 ? [retryButton()] : [])], 'err');
    status(''); reading = data; renderReading(data); compute();
  } catch {
    if (mine === seq) status(['Couldn’t reach the server. Check your connection and try again.', retryButton()], 'err');
  } finally {
    clearTimeout(timer);
    if (mine === seq) update();
  }
}

function onChartClick(e) {
  if (!source?.geom) return;
  const pt = overlay.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
  const {x, y} = pt.matrixTransform(overlay.getScreenCTM().inverse()), [t, w] = source.geom.fromPx(x, y);
  if (!(w >= 0) || !Number.isFinite(t)) return;
  seq++; reading = null; clicked = [t, w];
  const card = node('div', 'card'); card.append(node('p', 'hint', 'Clicked point on the chart: no AI involved, just the equations.'));
  $('reading').replaceChildren(card); status('');
  compute();
}

function update() {
  const n = $('text').value.length;
  $('count').textContent = n + ' / ' + MAX; $('count').classList.toggle('over', n > MAX);
  $('run').disabled = $('text').value.trim().length < 3 || n > MAX;
}

function init() {
  [['194 / 200', 'test questions read correctly (pass line 194)'], ['0.38 s', 'median time for Jev’s reading'],
   ['< 1 ms', 'to compute all seven properties exactly'], ['On device', 'your chart image is read in the browser, never uploaded']].forEach(([n, t]) => {
    const d = node('div'); d.append(node('dt', null, n), node('dd', null, t)); $('stats').append(d);
  });
  ALTITUDES.forEach(([id, label]) => { const o = node('option', null, label); o.value = id; $('drawn').append(o); });
  $('drawn').addEventListener('change', e => { if (e.target.value) useDrawn(e.target.value); });
  $('use-sample').addEventListener('click', () => { $('drawn').value = ''; useSample(); });
  $('file').addEventListener('change', e => { $('drawn').value = ''; readFile(e.target.files[0]); e.target.value = ''; });
  $('pressure').addEventListener('change', e => { pressure = e.target.value === 'chart' ? source.chartP : pressureAt(ALTITUDES.find(a => a[0] === e.target.value)[2]); compute(); redraw(); });
  $('show-curves').addEventListener('change', redraw);
  const zone = $('dropzone');
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag'));
  zone.addEventListener('drop', e => { e.preventDefault(); zone.classList.remove('drag'); readFile(e.dataTransfer.files[0]); });
  document.addEventListener('paste', e => { const f = [...(e.clipboardData?.files || [])].find(x => x.type.startsWith('image/')); if (f) readFile(f); });
  EXAMPLES.forEach(x => { const b = node('button', null, x); b.type = 'button'; b.addEventListener('click', () => { $('text').value = x; update(); ask(); }); $('examples').append(b); });
  $('text').addEventListener('input', update);
  $('text').addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(); } });
  $('ask').addEventListener('submit', e => { e.preventDefault(); ask(); });
  useSample(); update();
}
init();
