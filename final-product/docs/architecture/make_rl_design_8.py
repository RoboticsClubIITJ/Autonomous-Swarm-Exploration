"""
Slide graphic (v8): the network at full height on the left; reward, PPO loop and objective on the right.

  python3 docs/architecture/make_rl_design_8.py   # writes presentation/rl_design_choices_8.svg

The bar chart under the actor uses the shipped policy's real output for the first decision
of an episode on the benchmark arena (8 valid slots; see docs/ultimate_rl_explanation.md §5.4).
Objective: J = J_CLIP - 0.5 * E_VF + 0.01 * H (vf_coef, ent_coef from rl_sim/train.py).
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'presentation', 'rl_design_choices_8.svg')
W, H = 1100, 560
INK, GREY, HAIR = '#1C1C1C', '#6E6E6E', '#D3D3D3'
ACT, ACT_L = '#2B5C8A', '#DCE7F2'        # actor
CRI, CRI_L = '#B5562B', '#F5E3D8'        # critic
ENT = '#5E7D3A'                          # entropy
SANS = "'Open Sans', sans-serif"
SERIF = SANS                             # sans everywhere, including math
MATH = f' font-family="{SERIF}"'                # upright, no italics anywhere

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{SANS}" font-size="13">',
     '<defs><marker id="arr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">'
     f'<path d="M0,0 L9,3.5 L0,7 z" fill="{INK}"/></marker></defs>',
     f'<rect width="{W}" height="{H}" fill="white"/>']


def text(x, y, s, size=13, anchor='start', bold=False, fill=INK, extra=''):
    b = ' font-weight="bold"' if bold else ''
    p.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{b}{extra}>{s}</text>')


def heading(x, y, s, size=18):
    text(x, y, s, size=size, extra=f' font-family="{SERIF}"')


def hline(x1, x2, y):
    p.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{HAIR}" stroke-width="1"/>')


def vline(x, y1, y2):
    p.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{HAIR}" stroke-width="1"/>')


def m(t, size=14, fill=INK):
    return f'<tspan font-family="{SERIF}" font-size="{size}" fill="{fill}">{t}</tspan>'


def sub(t):
    return f'<tspan dy="5" font-size="12">{t}</tspan><tspan dy="-5"> </tspan>'


# ── the network (left, full height) ──────────────────────────────────────
vline(620, 20, 540)

IN_Y, H1_Y, H2_Y, OUT_Y = 60, 174, 286, 388
BASE = OUT_Y + 80                        # baseline of the π(slot | s) chart
# critic rows: same first layer as the actor, stretched evenly down to the π row
C_H1, C_H2, C_OUT = H1_Y, (H1_Y + BASE - 4) // 2, BASE - 4
ax, cx = 125, 510
mid = (ax + cx) / 2
R_IN, R_H, R_OUT, GAP_IN, GAP_H, GAP_OUT = 6.5, 7.5, 6, 23, 23, 16


def row(cxn, y, n, gap, r, fill, stroke, ellipsis=True):
    """n node x-positions centred on cxn, with an ellipsis in the middle."""
    half = n // 2
    xs = [cxn + (k - half - (0 if k < half else -1)) * gap if ellipsis else cxn + (k - (n - 1) / 2) * gap
          for k in range(n)]
    return xs


def nodes(xs, y, r, fill, stroke, dashed=False):
    for x in xs:
        d = ' stroke-dasharray="2 2"' if dashed else ''
        p.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"{d}/>')


def wires(xs1, y1, xs2, y2, r1, r2, color, opacity):
    for a in xs1:
        for b in xs2:
            p.append(f'<line x1="{a:.1f}" y1="{y1 + r1}" x2="{b:.1f}" y2="{y2 - r2}" stroke="{color}" '
                     f'stroke-opacity="{opacity}" stroke-width="0.7"/>')


xin = row(mid, IN_Y, 12, GAP_IN, R_IN, 'white', INK)
branches = []
for c, col, light, y1, y2 in ((ax, ACT, ACT_L, H1_Y, H2_Y), (cx, CRI, CRI_L, C_H1, C_H2)):
    h1 = row(c, y1, 6, GAP_H, R_H, light, col)
    h2 = row(c, y2, 6, GAP_H, R_H, light, col)
    wires(xin, IN_Y, h1, y1, R_IN, R_H, col, 0.16)
    wires(h1, y1, h2, y2, R_H, R_H, col, 0.2)
    branches.append((h1, h2, col, light, y1, y2))

# actor output: 12 slot scores, last 4 masked
outs = [ax + (k - 5.5) * GAP_OUT for k in range(12)]
wires(branches[0][1], H2_Y, outs, OUT_Y, R_H, R_OUT, ACT, 0.12)
nodes(outs[:8], OUT_Y, R_OUT, ACT, ACT)
nodes(outs[8:], OUT_Y, R_OUT, 'white', '#AAAAAA', dashed=True)
# critic output: one value
wires(branches[1][1], C_H2, [cx], C_OUT, R_H, 9, CRI, 0.25)
nodes([cx], C_OUT, 9, CRI, CRI)

nodes(xin, IN_Y, R_IN, 'white', INK)
for h1, h2, col, light, y1, y2 in branches:
    nodes(h1, y1, R_H, light, col)
    nodes(h2, y2, R_H, light, col)
for x0, y in ((mid, IN_Y), (ax, H1_Y), (ax, H2_Y), (cx, C_H1), (cx, C_H2)):
    text(x0, y + 5, '…', size=17, anchor='middle', fill=GREY)

LBL = ''
text(mid, IN_Y - 20, 'Observation (153 numbers)', size=16, anchor='middle', fill=GREY, extra=LBL)
# one label for all four hidden layers, in the gap between the two branches
HALO = LBL + ' paint-order="stroke" stroke="white" stroke-width="6"'
text(mid, (H1_Y + H2_Y) / 2 + 2, 'Hidden layers', size=15.5, anchor='middle', fill=GREY, extra=HALO)
text(mid, (H1_Y + H2_Y) / 2 + 22, '128 neurons each', size=15.5, anchor='middle', fill=GREY, extra=HALO)
text(outs[-1] + 16, OUT_Y + 5, '12 slot scores', size=15.5, fill=GREY, extra=LBL)

# π(slot | s): real output for the first decision of an episode (8 valid slots)
probs = [0.0029, 0.8626, 0.0070, 0.0017, 0.0036, 0.1192, 0.0013, 0.0016]
base = BASE
p.append(f'<line x1="{outs[0]-7}" y1="{base}" x2="{outs[-1]+7}" y2="{base}" stroke="{INK}" stroke-width="0.8"/>')
for k, x in enumerate(outs):
    if k < 8:
        hgt = max(probs[k] * 58, 1.4)
        p.append(f'<rect x="{x-4.5:.1f}" y="{base-hgt:.1f}" width="9" height="{hgt:.1f}" fill="{ACT}"/>')
    else:
        text(x, base - 2, '×', size=11, anchor='middle', fill='#AAAAAA')
text(outs[1] + 10, base - 42, '0.86', size=14, fill=ACT)
text(outs[5] + 10, base - 10, '0.12', size=14, fill=ACT)
text(outs[-1] + 16, base - 4, 'Mask + softmax', size=15.5, fill=GREY, extra=LBL)
text((outs[0] + outs[-1]) / 2, base + 25, 'π(slot | s)', size=22, anchor='middle', extra=MATH)

text(cx + 20, C_OUT + 8, 'V(s)', size=22, extra=MATH)

for x0, name, col, q in ((ax, 'Actor', ACT, 'Which frontier?'), (cx, 'Critic', CRI, 'How good is this state?')):
    text(x0, 529, name, size=18, bold=True, fill=col, anchor='middle')
    text(x0, 551, q, size=15.5, fill=GREY, anchor='middle')

# ── reward (right, top) ─────────────────────────────────────────────────
heading(644, 44, 'Reward', size=21)
text(644, 90, 'r = 0.1 · ΔA − 0.01 · Δt', size=26, extra=MATH)
hline(644, 1060, 120)

# ── training loop (right) ───────────────────────────────────────────────
heading(644, 154, 'Training loop (PPO)', size=21)
steps = ['Run the policy, record actions and rewards', 'Score each action (advantage)',
         'Make good actions more likely (clipped)', 'Improve the critic’s predictions']
SY = [196, 244, 292, 340]
for i, (name, y) in enumerate(zip(steps, SY)):
    text(650, y + 9, str(i + 1), size=26, fill=ACT, extra=f' font-family="{SERIF}"')
    text(684, y + 5, name, size=15, bold=True)
# return arrow, step 4 back to step 1: a straight bracket with rounded corners
p.append(f'<path d="M1040,{SY[3]} H1048 Q1060,{SY[3]} 1060,{SY[3]-12} V{SY[0]+12} Q1060,{SY[0]} 1048,{SY[0]} H1032" '
         f'fill="none" stroke="{GREY}" stroke-width="1.3" marker-end="url(#arr)"/>')
text(1078, (SY[0] + SY[3]) / 2, 'repeat', size=13, anchor='middle', fill=GREY,
     extra=f' transform="rotate(-90 1078 {(SY[0] + SY[3]) / 2})"')

# ── objective ───────────────────────────────────────────────────────────
hline(644, 1060, 380)
heading(644, 412, 'Objective', size=21)
ey = 460
text(650, ey, 'J(θ) =', size=20, extra=MATH)
terms = [(762, 'J' + sub('CLIP'), ACT, 726, 798, 'improve the actor'),
         (880, '0.5 · E' + sub('VF'), CRI, 838, 922, 'fix the critic’s error'),
         (1004, '0.01 · H(π)', ENT, 958, 1052, 'keep exploring')]
for tx, t, col, x1, x2, lab in terms:
    text(tx, ey, t, size=20, fill=col, anchor='middle', extra=MATH)
    yb, mx = ey + 10, (x1 + x2) / 2
    p.append(f'<path d="M{x1},{yb} q0,7 7,7 L{mx-7},{yb+7} q7,0 7,7 q0,-7 7,-7 L{x2-7},{yb+7} q7,0 7,-7" '
             f'fill="none" stroke="{col}" stroke-width="1.2"/>')
    text(mx, yb + 32, lab, size=12.5, fill=col, anchor='middle')
text(814, ey, '−', size=20, anchor='middle')
text(940, ey, '+', size=20, anchor='middle')

with open(OUT, 'w') as fh:
    fh.write('\n'.join(p + ['</svg>']))
print('Wrote', os.path.normpath(OUT))
