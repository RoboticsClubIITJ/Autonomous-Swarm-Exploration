"""
Insights strip for the inference-results slide (sits under the two Gazebo graphs), in the design
language of rl_design_choices_7.

  python3 docs/architecture/make_results_insights.py   # writes presentation/results_insights.svg

Numbers: 8 paired Gazebo runs in results/archive/2_ghost_fix_theta_star (same data as the graphs);
PPO better in 8/8 pairs on both, exact paired permutation p = 0.008.
Rate windows: (A(b) - A(a)) / (b - a) per run, then averaged.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'presentation', 'results_insights.svg')
W, H = 1100, 104
INK, GREY, HAIR = '#1C1C1C', '#6E6E6E', '#D3D3D3'
PPO = '#1f77b4'                 # same blue as the PPO lines in the graphs
SANS = "'Open Sans', sans-serif"

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{SANS}" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="white"/>']


def text(x, y, s, size=13, anchor='middle', bold=False, fill=INK):
    b = ' font-weight="bold"' if bold else ''
    p.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{b}>{s}</text>')


insights = [   # (centre x, big number, what, values)
    (W / 4, '+38 %', 'exploration rate, 30–150 s', '0.16 vs 0.12 m²/s'),      # under the rate graph
    (3 * W / 4, '−21 %', 'time to map 30 m²', '127 s vs 160 s'),              # under the area graph
]
for cx, big, what, vals in insights:
    text(cx, 56, big, size=42, fill=PPO)
    text(cx, 84, what, size=14)
p.append(f'<line x1="{W/2}" y1="14" x2="{W/2}" y2="{H-14}" stroke="{HAIR}" stroke-width="1"/>')

with open(OUT, 'w') as fh:
    fh.write('\n'.join(p + ['</svg>']))
print('Wrote', os.path.normpath(OUT))
