"""Upload test on a real chart: calibrate the FlyCarpet sea-level SI chart from its own SVG lines, then check every
printed RH, enthalpy, specific-volume and wet-bulb line against psychro.py.

Criteria, set before running: calibration residual under 1 px, and each printed line within ±1 %RH, ±0.5 kJ/kg,
±0.005 m³/kg or ±0.3 °C wet-bulb of a single value along its visible length. The chart itself is © FlyCarpet Inc
(flycarpet.net/en/psyonline) and stays out of git (data/charts/ is ignored).

Usage: python chart_check.py  -> runs/chart_check.json, and the calibration printed as JSON for the web page.
"""
import json
from pathlib import Path
import re
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import psychro as ps

HERE = Path(__file__).resolve().parents[1]
SVG = HERE / 'data/charts/FlyCarpetPsyChart.svg'
Y0, PX_PER_G = 590.0, 18.0          # humidity-ratio gridlines: W = 0 at y 590, one line per g/kg every 18 px


def lines(svg, name):
    out = []
    for m in re.finditer(r'<(line|polyline)([^>]*)name="%s"([^>]*)/?>' % name, svg):
        attrs = m.group(2) + m.group(3)
        if m.group(1) == 'line':
            g = {k: float(re.search(k + r'="([^"]+)"', attrs).group(1)) for k in ('x1', 'y1', 'x2', 'y2')}
            out.append([(g['x1'], g['y1']), (g['x2'], g['y2'])])
        else:
            pts = re.search(r'points="([^"]+)"', attrs).group(1).split()
            out.append([tuple(map(float, p.split(','))) for p in pts])
    return out


def w_of(y):
    return (Y0 - y) / PX_PER_G / 1000


def solve_linear(rows, ys):
    """Least squares for x = a + b·t + c·W + d·t·W (normal equations, 4×4)."""
    n = 4
    A = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    B = [sum(r[i] * y for r, y in zip(rows, ys)) for i in range(n)]
    for i in range(n):
        piv = max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[piv], B[i], B[piv] = A[piv], A[i], B[piv], B[i]
        for k in range(i + 1, n):
            f = A[k][i] / A[i][i]
            A[k] = [a - f * b for a, b in zip(A[k], A[i])]
            B[k] -= f * B[i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (B[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


def main():
    svg = SVG.read_text(encoding='utf-8')
    # Dry-bulb gridlines are drawn every 5 °C from -5 to 45 °C (their feet on the W = 0 axis are 63.25 px apart).
    dry = sorted(lines(svg, 'psyt'), key=lambda l: l[0][0])
    rows, xs = [], []
    for i, seg in enumerate(dry):
        t = -5 + 5 * i
        for x, y in seg:
            w = w_of(y)
            rows.append([1, t, w, t * w]); xs.append(x)
    a, b, c, d = solve_linear(rows, xs)
    fit = lambda t, w: a + b * t + c * w + d * t * w
    residual = max(abs(fit(r[1], r[2]) - x) for r, x in zip(rows, xs))
    t_of = lambda x, y: (x - a - c * w_of(y)) / (b + d * w_of(y))

    def spread(name, prop, keep):
        """Value of `prop` along each printed line; returns (nominal, max deviation) per line."""
        out = []
        for seg in lines(svg, name):
            vals = []
            dense = [(x0 + (x1 - x0) * k / 20, y0 + (y1 - y0) * k / 20) for (x0, y0), (x1, y1) in zip(seg, seg[1:]) for k in range(21)]
            for x, y in dense:
                w, t = w_of(y), t_of(x, y)
                if w < 0 or not -10 <= t <= 50:
                    continue
                try:
                    vals.append(ps.state(t, w)[prop])
                except ValueError:
                    continue
            if len(vals) >= 2 and keep(seg):
                mid = statistics.median(vals)
                out.append({'value': round(mid, 4), 'max_dev': round(max(abs(v - mid) for v in vals), 4), 'points': len(vals)})
        return out

    long_enough = lambda seg: abs(seg[0][0] - seg[-1][0]) + abs(seg[0][1] - seg[-1][1]) > 40
    checks = {'rh': spread('psyrh', 'rh', lambda s: True), 'h': spread('psyh', 'h', long_enough),
              'v': spread('psyv', 'v', long_enough), 'twb': spread('psywbt', 'twb', long_enough)}
    limits = {'rh': 0.01, 'h': 0.5, 'v': 0.005, 'twb': 0.3}
    # Nominal check: RH lines should sit at 10 %…90 % and 100 % (saturation).
    rh_levels = sorted(round(x['value'] * 100) for x in checks['rh'])
    result = {'chart': 'FlyCarpet sea-level SI chart (© FlyCarpet Inc, flycarpet.net/en/psyonline)', 'pressure_pa': ps.P_SEA,
              'calibration': {'x = a + b·t + c·W + d·t·W': [a, b, c, d], 'y = Y0 - W_g_per_kg·18': Y0,
                              'residual_px': round(residual, 3), 'pass': residual < 1},
              'rh_levels_found': rh_levels,
              'lines': {k: {'count': len(v), 'worst_dev': max((x['max_dev'] for x in v), default=None), 'limit': limits[k],
                            'pass': bool(v) and all(x['max_dev'] <= limits[k] for x in v)} for k, v in checks.items()},
              'detail': checks}
    (HERE / 'runs').mkdir(exist_ok=True)
    (HERE / 'runs/chart_check.json').write_text(json.dumps(result, indent=1), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('calibration', 'rh_levels_found', 'lines')}, indent=1))


if __name__ == '__main__':
    main()
