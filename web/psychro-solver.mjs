// Moist-air state from two properties: a line-for-line port of experiments/psychrometric-charts/src/psychro.py
// (ASHRAE Handbook Fundamentals 2017, chapter 1; SI). tests/test_psychro_solver.mjs checks it against the Python solver.
export const P_SEA = 101325;
export const PROPS = ['tdb', 'twb', 'tdp', 'rh', 'w', 'h', 'v'];
const same = (a, b, x, y) => (a === x && b === y) || (a === y && b === x);

export const pressureAt = z => 101325 * (1 - 2.25577e-5 * z) ** 5.2559;

export function pws(t) {
  const T = t + 273.15;
  const ln = t <= 0.01
    ? -5.6745359e3 / T + 6.3925247 - 9.677843e-3 * T + 6.2215701e-7 * T ** 2 + 2.0747825e-9 * T ** 3 - 9.484024e-13 * T ** 4 + 4.1635019 * Math.log(T)
    : -5.8002206e3 / T + 1.3914993 - 4.8640239e-2 * T + 4.1764768e-5 * T ** 2 - 1.4452093e-8 * T ** 3 + 6.5459673 * Math.log(T);
  return Math.exp(ln);
}
export const wFromPw = (pw, p) => 0.621945 * pw / (p - pw);
export const pwFromW = (w, p) => p * w / (0.621945 + w);
export const enthalpy = (t, w) => 1.006 * t + w * (2501 + 1.86 * t);
export const volume = (t, w, p) => 0.287042 * (t + 273.15) * (1 + 1.607858 * w) / (p / 1000);

export function wFromWetBulb(t, twb, p) {
  const ws = wFromPw(pws(twb), p);
  return twb > 0
    ? ((2501 - 2.326 * twb) * ws - 1.006 * (t - twb)) / (2501 + 1.86 * t - 4.186 * twb)
    : ((2830 - 0.24 * twb) * ws - 1.006 * (t - twb)) / (2830 + 1.86 * t - 2.1 * twb);
}

export function bisect(f, lo, hi, tol = 1e-10) {
  let flo = f(lo);
  if (flo * f(hi) > 0) throw new Error('no root in range');
  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2, fm = f(mid);
    if (fm === 0 || hi - lo < tol) return mid;
    if ((fm > 0) === (flo > 0)) { lo = mid; flo = fm; } else hi = mid;
  }
  return (lo + hi) / 2;
}

export const dewPoint = (w, p) => { const pw = pwFromW(w, p); return bisect(x => pws(x) - pw, -100, 200); };
export const wetBulb = (t, w, p) => bisect(x => wFromWetBulb(t, x, p) - w, dewPoint(w, p) - 1e-6, t + 1e-6);

export class StateError extends Error {}

export function state(t, w, p = P_SEA) {
  const rh = pwFromW(w, p) / pws(t);
  if (w < 0 || rh > 1 + 1e-6) throw new StateError('These two values can’t occur together in moist air (the air would be above saturation).');
  return {tdb: t, twb: wetBulb(t, w, p), tdp: dewPoint(w, p), rh, w, h: enthalpy(t, w), v: volume(t, w, p)};
}

export function wAt(t, name, value, p) {
  switch (name) {
    case 'w': return value;
    case 'rh': return wFromPw(value * pws(t), p);
    case 'twb': return wFromWetBulb(t, value, p);
    case 'tdp': return wFromPw(pws(value), p);
    case 'h': return (value - 1.006 * t) / (2501 + 1.86 * t);
    case 'v': return (value * (p / 1000) / (0.287042 * (t + 273.15)) - 1) / 1.607858;
    default: throw new StateError('Unknown property ' + name);
  }
}

export function solve([na, va], [nb, vb], p = P_SEA, [lo, hi] = [-60, 120]) {
  if (na === nb) throw new StateError('Both values are the same property. Pick two different properties.');
  if (same(na, nb, 'tdp', 'w')) throw new StateError('Dew point and humidity ratio describe the same thing. Give one more property.');
  if (na === 'tdb' || nb === 'tdb') {
    const [t, n, v] = na === 'tdb' ? [va, nb, vb] : [vb, na, va];
    return state(t, wAt(t, n, v, p), p);
  }
  const residual = t => wAt(t, na, va, p) - wAt(t, nb, vb, p);
  let x0 = lo, r0 = residual(lo);
  while (x0 < hi) {
    const x1 = Math.min(hi, x0 + 0.25), r1 = residual(x1);
    if (r0 === 0 || r0 * r1 < 0) {
      const t = r0 === 0 ? x0 : bisect(residual, x0, x1);
      try { return state(t, wAt(t, na, va, p), p); } catch (e) { if (!(e instanceof StateError)) throw e; }
    }
    x0 = x1; r0 = r1;
  }
  throw new StateError('No moist-air state matches these two values.');
}

// Unit conversion driven by the property label (score_pilot.to_si). null means the label doesn't fit the unit.
export function toSI(prop, value, unit) {
  if (['tdb', 'twb', 'tdp'].includes(prop)) {
    if (['°C', 'C', 'degrees', ''].includes(unit)) return value;
    if (['°F', 'F', 'degrees F'].includes(unit)) return (value - 32) / 1.8;
    return null;
  }
  if (prop === 'rh') return ['%', ''].includes(unit) ? value / 100 : null;
  if (prop === 'w') return unit === 'g/kg' ? value / 1000 : null;
  if (prop === 'h') return unit === 'kJ/kg' ? value : null;
  return unit === 'm³/kg' ? value : null;
}
