"""
Exploration rate (m² newly mapped per second) over time, PPO vs heuristic, from paired Gazebo runs.
Same style as graphs/04_gazebo_coverage_over_time.svg.

  python3 rl_sim/exploration_rate_graph.py --dir results/archive/2_ghost_fix_theta_star

rate(t) = (A(t + WINDOW/2) - A(t - WINDOW/2)) / WINDOW, a centred average (the window is clipped to
[0, HORIZON] at the ends, so the curve covers the whole run), because the raw per-second area is a
step function. Also prints the mean rate over 0-180 s per
policy with an exact paired permutation test (same test as analyze_gazebo_tests.py).
"""
import argparse
import glob
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import numpy as np  # noqa: E402

from rl_sim.analyze_gazebo_tests import area_at, load, perm_test  # noqa: E402

WINDOW = 30.0      # s
HORIZON = 240.0    # s
PPO_C, HEUR_C = '#1f77b4', '#d62728'


def rates(run, grid):
    lo = np.clip(grid - WINDOW / 2, 0, HORIZON)
    hi = np.clip(grid + WINDOW / 2, 0, HORIZON)
    return (np.interp(hi, run['t'], run['a']) - np.interp(lo, run['t'], run['a'])) / (hi - lo)


def svg(ppo, heur, path):
    W, H, L, B, T, R = 640, 420, 60, 50, 30, 20
    grid = np.arange(0, HORIZON + 1, 2.0)
    cp, ch = np.array([rates(r, grid) for r in ppo]), np.array([rates(r, grid) for r in heur])
    ymax = max(cp.max(), ch.max()) * 1.25

    def xs(t):
        return L + (W - L - R) * t / HORIZON

    def ys(v):
        return H - B - (H - B - T) * v / ymax

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="12">',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<text x="{W/2}" y="16" text-anchor="middle" font-size="15" font-weight="bold">'
           'Exploration rate over time</text>']
    v = 0.0
    while v <= ymax + 1e-9:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{ys(v):.1f}" y2="{ys(v):.1f}" stroke="#ddd"/>'
                   f'<text x="{L-8}" y="{ys(v)+4:.1f}" text-anchor="end">{v:.1f}</text>')
        v += 0.1
    for t in range(0, int(HORIZON) + 1, 60):
        out.append(f'<text x="{xs(t):.1f}" y="{H-B+18}" text-anchor="middle">{t}</text>')
    out.append(f'<text x="{(L+W-R)/2}" y="{H-12}" text-anchor="middle">simulated time (s)</text>'
               f'<text x="16" y="{(H-B)/2}" transform="rotate(-90 16 {(H-B)/2})" text-anchor="middle">'
               'newly mapped area (m² / s)</text>')
    for c, color, label, ly in ((cp, PPO_C, 'PPO policy', 46), (ch, HEUR_C, 'Heuristic', 64)):
        lo, hi, mean = c.min(0), c.max(0), c.mean(0)
        band = ' '.join(f'{xs(t):.1f},{ys(v):.1f}' for t, v in zip(grid, hi)) + ' ' + \
               ' '.join(f'{xs(t):.1f},{ys(v):.1f}' for t, v in zip(grid[::-1], lo[::-1]))
        out.append(f'<polygon points="{band}" fill="{color}" fill-opacity="0.15"/>')
        line = ' '.join(f'{xs(t):.1f},{ys(v):.1f}' for t, v in zip(grid, mean))
        out.append(f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        out.append(f'<line x1="{L+15}" x2="{L+40}" y1="{ly}" y2="{ly}" stroke="{color}" stroke-width="2.5"/>'
                   f'<text x="{L+46}" y="{ly+4}">{label}</text>')
    out.append('</svg>')
    with open(path, 'w') as fh:
        fh.write('\n'.join(out))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--dir', default=os.path.join(REPO, 'results', 'gazebo_runs'))
    p.add_argument('--svg', default=os.path.join(REPO, 'graphs', '21_gazebo_exploration_rate.svg'))
    args = p.parse_args()
    ppo = [load(f) for f in sorted(glob.glob(os.path.join(args.dir, 'ppo_*.csv')))]
    heur = [load(f) for f in sorted(glob.glob(os.path.join(args.dir, 'heuristic_*.csv')))]
    n = min(len(ppo), len(heur))
    ppo, heur = ppo[:n], heur[:n]
    svg(ppo, heur, args.svg)

    mean_rate = {k: np.array([(area_at(r, 180) - r['a'][0]) / 180 for r in runs])
                 for k, runs in (('ppo', ppo), ('heuristic', heur))}
    d = mean_rate['ppo'] - mean_rate['heuristic']
    grid = np.arange(0, HORIZON + 1, 2.0)
    peak = {k: np.array([rates(r, grid).max() for r in runs]) for k, runs in (('ppo', ppo), ('heuristic', heur))}
    print(f'{n} paired runs from {args.dir}')
    for k in ('ppo', 'heuristic'):
        print(f'  {k:9s} mean rate 0-180 s: {mean_rate[k].mean():.3f} ± {mean_rate[k].std(ddof=1):.3f} m²/s'
              f' | peak {WINDOW:.0f} s rate: {peak[k].mean():.3f} m²/s')
    print(f'  paired diff {d.mean():+.3f} m²/s ({100 * d.mean() / mean_rate["heuristic"].mean():+.0f} %), '
          f'PPO higher in {int((d > 0).sum())}/{n}, exact permutation p = {perm_test(d):.3f}')
    print('Wrote', args.svg)


if __name__ == '__main__':
    main()
