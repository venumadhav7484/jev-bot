"""Moist-air state from any two independent properties: the math behind every psychrometric chart.

SI units, ASHRAE Handbook Fundamentals (2017) chapter 1 relations, the same ones PsychroLib implements:
Hyland-Wexler saturation pressure over ice and water, humidity ratio, enthalpy, specific volume, and the
wet-bulb relation. Properties:
    tdb dry-bulb °C · twb wet-bulb °C · tdp dew point °C · rh relative humidity 0-1
    w humidity ratio kg/kg dry air · h enthalpy kJ/kg dry air · v specific volume m³/kg dry air
Every state is found as (tdb, w) and then all seven properties are computed from it.
"""
import math

P_SEA = 101325.0
PROPS = ('tdb', 'twb', 'tdp', 'rh', 'w', 'h', 'v')
DEPENDENT = [{'tdp', 'w'}]           # dew point and humidity ratio carry the same information
ILL_CONDITIONED = [{'twb', 'h'}]    # wet-bulb and enthalpy lines are nearly parallel on the chart


def pressure_at(altitude_m):
    """Standard atmospheric pressure (Pa) at an altitude (ASHRAE eq. 3)."""
    return 101325.0 * (1 - 2.25577e-5 * altitude_m) ** 5.2559


def pws(t):
    """Saturation vapour pressure (Pa) over ice at or below 0.01 °C, over liquid water above."""
    T = t + 273.15
    if t <= 0.01:
        ln = (-5.6745359e3 / T + 6.3925247 - 9.677843e-3 * T + 6.2215701e-7 * T ** 2
              + 2.0747825e-9 * T ** 3 - 9.484024e-13 * T ** 4 + 4.1635019 * math.log(T))
    else:
        ln = (-5.8002206e3 / T + 1.3914993 - 4.8640239e-2 * T + 4.1764768e-5 * T ** 2
              - 1.4452093e-8 * T ** 3 + 6.5459673 * math.log(T))
    return math.exp(ln)


def w_from_pw(pw, p):
    return 0.621945 * pw / (p - pw)


def pw_from_w(w, p):
    return p * w / (0.621945 + w)


def enthalpy(t, w):
    return 1.006 * t + w * (2501 + 1.86 * t)


def volume(t, w, p):
    return 0.287042 * (t + 273.15) * (1 + 1.607858 * w) / (p / 1000)


def w_from_wet_bulb(t, twb, p):
    ws = w_from_pw(pws(twb), p)
    if twb > 0:
        return ((2501 - 2.326 * twb) * ws - 1.006 * (t - twb)) / (2501 + 1.86 * t - 4.186 * twb)
    return ((2830 - 0.24 * twb) * ws - 1.006 * (t - twb)) / (2830 + 1.86 * t - 2.1 * twb)


def bisect(f, lo, hi, tol=1e-10):
    flo = f(lo)
    if flo * f(hi) > 0:
        raise ValueError('no root in range')
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm == 0 or hi - lo < tol:
            return mid
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def dew_point(w, p):
    pw = pw_from_w(w, p)
    return bisect(lambda x: pws(x) - pw, -100, 200)


def wet_bulb(t, w, p):
    return bisect(lambda x: w_from_wet_bulb(t, x, p) - w, dew_point(w, p) - 1e-6, t + 1e-6)


def state(t, w, p=P_SEA):
    """All seven properties of the state (t, w)."""
    rh = pw_from_w(w, p) / pws(t)
    if w < 0 or rh > 1 + 1e-6:
        raise ValueError('not a moist-air state (humidity above saturation or negative)')
    return {'tdb': t, 'twb': wet_bulb(t, w, p), 'tdp': dew_point(w, p), 'rh': rh, 'w': w,
            'h': enthalpy(t, w), 'v': volume(t, w, p)}


def w_at(t, name, value, p):
    """Humidity ratio at dry-bulb t implied by one other property."""
    if name == 'w':
        return value
    if name == 'rh':
        return w_from_pw(value * pws(t), p)
    if name == 'twb':
        return w_from_wet_bulb(t, value, p)
    if name == 'tdp':
        return w_from_pw(pws(value), p)
    if name == 'h':
        return (value - 1.006 * t) / (2501 + 1.86 * t)
    if name == 'v':
        return (value * (p / 1000) / (0.287042 * (t + 273.15)) - 1) / 1.607858
    raise ValueError('unknown property ' + name)


def solve(a, b, p=P_SEA, t_range=(-60.0, 120.0)):
    """State from two (property, value) pairs, e.g. solve(('tdb', 25), ('rh', 0.5))."""
    (na, va), (nb, vb) = a, b
    if na == nb or na not in PROPS or nb not in PROPS:
        raise ValueError('give two different properties from ' + ', '.join(PROPS))
    if {na, nb} in DEPENDENT:
        raise ValueError('dew point and humidity ratio describe the same thing; give one more property')
    if 'tdb' in (na, nb):
        t, (n, v) = (va, (nb, vb)) if na == 'tdb' else (vb, (na, va))
        return state(t, w_at(t, n, v, p), p)
    # Neither is dry-bulb: find the dry-bulb where both properties imply the same humidity ratio.
    residual = lambda t: w_at(t, na, va, p) - w_at(t, nb, vb, p)
    lo, hi = t_range
    step = 0.25
    x0, r0 = lo, residual(lo)
    while x0 < hi:
        x1 = min(hi, x0 + step)
        r1 = residual(x1)
        if r0 == 0 or r0 * r1 < 0:
            t = x0 if r0 == 0 else bisect(residual, x0, x1)
            try:
                return state(t, w_at(t, na, va, p), p)
            except ValueError:
                pass  # a root outside the moist-air region; keep scanning
        x0, r0 = x1, r1
    raise ValueError('no moist-air state matches these two values')
