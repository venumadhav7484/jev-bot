"""Check the solver against published reference values and round-trip every usable pair of properties."""
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import psychro as ps


class Reference(unittest.TestCase):
    def test_saturation_pressure_matches_ashrae_table(self):
        # ASHRAE Handbook Fundamentals (2017), chapter 1, table 3 (kPa)
        for t, kpa in ((-10, 0.25991), (0.01, 0.6117), (20, 2.3392), (30, 4.2467), (40, 7.3844), (100, 101.42)):
            self.assertAlmostEqual(ps.pws(t) / 1000 / kpa, 1, delta=1e-3, msg=t)

    def test_textbook_state_25c_50pct(self):
        s = ps.solve(('tdb', 25), ('rh', 0.5))
        self.assertAlmostEqual(s['w'], 0.00988, delta=5e-5)
        self.assertAlmostEqual(s['h'], 50.3, delta=0.1)
        self.assertAlmostEqual(s['tdp'], 13.9, delta=0.1)
        self.assertAlmostEqual(s['twb'], 17.9, delta=0.15)
        self.assertAlmostEqual(s['v'], 0.858, delta=0.002)

    def test_dependent_pair_is_refused(self):
        with self.assertRaises(ValueError):
            ps.solve(('tdp', 10), ('w', 0.0076))

    def test_supersaturated_input_is_refused(self):
        with self.assertRaises(ValueError):
            ps.solve(('tdb', 20), ('rh', 1.2))


class RoundTrip(unittest.TestCase):
    def test_every_usable_pair_recovers_the_state(self):
        pairs = [set(c) for c in combinations(ps.PROPS, 2) if set(c) not in ps.DEPENDENT]
        checked = 0
        for p in (ps.P_SEA, ps.pressure_at(1500)):
            for t in (-10, 0.5, 10, 20, 30, 40):
                for rh in (0.1, 0.3, 0.6, 0.9):
                    truth = ps.state(t, ps.w_at(t, 'rh', rh, p), p)
                    for a, b in (sorted(pair) for pair in pairs):
                        got = ps.solve((a, truth[a]), (b, truth[b]), p)
                        tol_t = 0.05 if {a, b} in ps.ILL_CONDITIONED else 1e-4
                        self.assertAlmostEqual(got['tdb'], t, delta=tol_t, msg=(a, b, t, rh, p))
                        self.assertAlmostEqual(got['w'], truth['w'], delta=1e-6, msg=(a, b, t, rh, p))
                        checked += 1
        self.assertEqual(checked, 2 * 6 * 4 * 20)


if __name__ == '__main__':
    unittest.main()
