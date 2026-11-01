"""Draws the logic diagram (inverters + AND gates + OR gate) with matplotlib."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, PathPatch
from matplotlib.path import Path

from logic import VARS


def _and_gate(ax, x, yc, w, h, n_in):
    """AND gate whose output is at (x+w, yc). Returns (output, [inputs])."""
    r = h / 2
    pts = [(x, yc - r), (x + w - r, yc - r)]
    import math
    arc = [(x + w - r + r * math.sin(t), yc + r * math.cos(t))
           for t in [i * math.pi / 20 - math.pi / 2 + math.pi / 2 for i in range(21)]]
    arc = [(x + w - r + r * math.cos(a), yc + r * math.sin(a))
           for a in [-math.pi / 2 + i * math.pi / 20 for i in range(21)]]
    poly = pts[:1] + [pts[1]] + arc + [(x, yc + r)]
    ax.add_patch(Polygon(poly, closed=True, fill=False, lw=1.4, ec="black"))
    gap = h * 0.7 / max(n_in - 1, 1)
    ys = [yc + (n_in - 1) * gap / 2 - i * gap for i in range(n_in)] if n_in > 1 else [yc]
    return (x + w, yc), [(x, y) for y in ys]


def _or_gate(ax, x, yc, w, h, n_in):
    t, b = yc + h / 2, yc - h / 2
    verts = [(x, t), (x + w * 0.55, t), (x + w, yc),          # top curve
             (x + w * 0.55, b), (x, b),                        # bottom curve
             (x + w * 0.3, yc), (x, t)]                        # concave back
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3,
             Path.CURVE3, Path.CURVE3]
    ax.add_patch(PathPatch(Path(verts, codes), fill=False, lw=1.4, ec="black"))
    gap = h * 0.7 / max(n_in - 1, 1)
    ys = [yc + (n_in - 1) * gap / 2 - i * gap for i in range(n_in)] if n_in > 1 else [yc]
    return (x + w, yc), [(x + w * 0.16, y) for y in ys]


def _dot(ax, x, y):
    ax.add_patch(Circle((x, y), 0.07, color="black", zorder=5))


def draw_schema(cover, path, names=VARS, n=4):
    """cover = list of implicants (strings like '000-'). Saves the image to `path`."""
    terms = [[(i, c) for i, c in enumerate(p) if c != "-"] for p in cover]
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_aspect("equal"); ax.axis("off")

    xt = {i: i * 2.6 for i in range(n)}           # rail of the direct variable
    xn = {i: i * 2.6 + 1.8 for i in range(n)}     # rail of the negated variable
    yin = {i: -i * 1.4 for i in range(n)}
    k = len(terms)
    pitch = 2.6
    y0 = yin[n - 1] - 2.6
    ybot = y0 - (k - 1) * pitch - 1.0
    for i in range(n):
        y = yin[i]
        ax.plot([-1.3, xt[i]], [y, y], "k", lw=1.4)
        ax.text(-1.45, y, names[i], ha="right", va="center", fontsize=13)
        _dot(ax, xt[i], y)
        gx = xt[i] + 0.5                          # inverter
        ax.add_patch(Polygon([(gx, y - 0.32), (gx, y + 0.32), (gx + 0.62, y)],
                             closed=True, fill=False, lw=1.4))
        ax.add_patch(Circle((gx + 0.69, y), 0.07, fill=False, lw=1.2))
        ax.plot([xt[i], gx], [y, y], "k", lw=1.4)
        ax.plot([gx + 0.76, xn[i]], [y, y], "k", lw=1.4)
        _dot(ax, xn[i], y)
        ax.plot([xt[i]] * 2, [y, ybot], "k", lw=1.4)
        ax.plot([xn[i]] * 2, [y, ybot], "k", lw=1.4)
        ax.text(xt[i] + 0.1, y + 0.12, names[i], fontsize=10)
        ax.text(xn[i] + 0.1, y + 0.12, names[i] + "'", fontsize=10)

    gx0 = xn[n - 1] + 3.0
    outs = []
    for j, lits in enumerate(terms):
        yc = y0 - j * pitch
        if len(lits) == 1:                         # single literal: plain wire
            i, c = lits[0]
            x = xt[i] if c == "1" else xn[i]
            ax.plot([x, gx0 + 1.4], [yc, yc], "k", lw=1.4); _dot(ax, x, yc)
            outs.append((gx0 + 1.4, yc)); continue
        out, ins = _and_gate(ax, gx0, yc, 1.4, 1.5, len(lits))
        for (i, c), (px, py) in zip(lits, ins):
            x = xt[i] if c == "1" else xn[i]
            ax.plot([x, px], [py, py], "k", lw=1.2); _dot(ax, x, py)
        ax.text(out[0] + 0.1, out[1] + 0.12, f"T{j + 1}", fontsize=10)
        outs.append(out)

    ycen = sum(o[1] for o in outs) / len(outs)
    ox = gx0 + 5.0
    if len(outs) == 1:
        fx, fy = outs[0]
        ax.plot([fx, fx + 1.5], [fy, fy], "k", lw=1.4); end = (fx + 1.5, fy)
    else:
        out, ins = _or_gate(ax, ox, ycen, 2.0, max(2.4, 0.55 * len(outs) + 0.6), len(outs))
        for j, ((sx, sy), (ix, iy)) in enumerate(zip(outs, ins)):
            off = 0.5 + 0.35 * abs(j - (len(outs) - 1) / 2) * 2
            xm = sx + off
            ax.plot([sx, xm, xm, ix], [sy, sy, iy, iy], "k", lw=1.2)
        ax.plot([out[0], out[0] + 1.2], [out[1], out[1]], "k", lw=1.4)
        end = (out[0] + 1.2, out[1])
    ax.add_patch(Circle(end, 0.1, fc="white", ec="black", lw=1.4, zorder=6))
    ax.text(end[0] + 0.25, end[1], "f", fontsize=14, va="center")
    ax.autoscale_view()
    ax.set_xlim(-2.6, end[0] + 1.2); ax.set_ylim(ybot - 0.4, 1.0)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
