"""
Horizontal strip (v2, decluttered) for "The 2D training simulator" slide: one headline number + tools,
in the same design language as rl_design_choices_7.

  python3 docs/architecture/make_sim_strip_2.py   # writes presentation/rl_simulator_strip_2.svg

Throughput numbers: see make_rl_design_2.py.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'presentation', 'rl_simulator_strip_2.svg')
W, H = 1100, 124
INK, GREY, HAIR = '#1C1C1C', '#6E6E6E', '#D3D3D3'
ACT, CRI = '#2B5C8A', '#B5562B'
SANS = "'Open Sans', sans-serif"

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{SANS}" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="white"/>']


def text(x, y, s, size=13, anchor='start', bold=False, fill=INK, extra=''):
    b = ' font-weight="bold"' if bold else ''
    p.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{b}{extra}>{s}</text>')


DIV = 440                                   # headline on the left, tools take the wider right side

# ── left: one headline number ──────────────────────────────────────────
text(30, 34, 'Train in a fast 2D simulator', size=18)
text(30, 100, '≈ 300×', size=46, fill=ACT)
text(200, 78, 'faster than Gazebo', size=17)
text(200, 102, '190 vs 0.7 decisions / s', size=14, fill=GREY)
p.append(f'<line x1="{DIV}" y1="20" x2="{DIV}" y2="{H-20}" stroke="{HAIR}" stroke-width="1"/>')

# ── right: tools, as two columns (label | tools), no heading ────────────
LX, TX = DIV + 40, DIV + 180
for y, label, tools in ((58, 'RL training', 'SB3 · MaskablePPO · PyTorch · Gymnasium · TensorBoard'),
                        (92, '2D simulator', 'NumPy · OpenCV')):
    text(LX, y, label, size=16, bold=True)
    text(TX, y, tools, size=16)

with open(OUT, 'w') as fh:
    fh.write('\n'.join(p + ['</svg>']))
print('Wrote', os.path.normpath(OUT))
