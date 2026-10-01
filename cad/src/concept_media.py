"""ConePro concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the parts from cad/src/model.py (PARAMS), colored and numbered to match bom/bom.csv, and
renders the media set with .kit/concept.py. Figures on the sheet and in the flow diagram come
from docs/04-calcs/sizing.py (CNP-CAL-001). Not for fabrication.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

m = build_parts()
EXPLODE = {"cone": (0, 0, -110), "lower_rod": (0, 0, -30), "anvil": (0, 0, 60), "hammer": (-330, -330, 420),
           "upper_rod": (0, 0, 150), "handle": (0, 0, 260), "plate": (0, 0, -260), "drawwire": (330, 330, -150),
           "clamp": (330, 330, 60), "pad": (-330, 330, 60), "logger": (-330, 330, -150), "cable": (-450, 250, 0),
           "reel_cable": (0, 420, -150)}
parts = [Part(name, shape, color, bom, EXPLODE[k]) for k, (name, shape, bom, color) in m.items()]

# Callout offsets for the exploded view, in screen pixels (dx right, dy down) from each part.
# The kit places callouts on the part itself, which hides the small sensor parts on a 1.9 m tall
# assembly, so the view is redrawn below with leader lines.
CALLOUT = {1: (70, 0), 2: (60, 40), 3: (60, 0), 4: (-60, -40), 5: (60, 0), 6: (60, 10),
           7: (-90, 10), 8: (60, 30), 9: (60, -30), 10: (60, -10), 11: (-70, 0), 12: (-60, 0),
           17: (60, 20)}


def exploded_with_leaders(parts, out, elev=24, azim=-58, size=(8, 6), dpi=160, ss=2, pad=0.06):
    """Redraw media/exploded.png with callouts set off the parts on leader lines."""
    import numpy as np
    import matplotlib.pyplot as plt
    import concept
    concept._render(parts, out, elev=elev, azim=azim, offsets=True, labels=False, size=size, dpi=dpi,
                    title="ConePro: exploded view", ss=ss)
    W, H = int(size[0] * dpi) * ss, int(size[1] * dpi) * ss
    e, a = np.radians(elev), np.radians(azim)
    d = -np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    right = np.cross(d, [0, 0, 1.0]); right /= np.linalg.norm(right)
    up = np.cross(right, d)
    P = np.stack([right, up, -d])
    items, allq = [], []
    for p in parts:
        v, t = concept._tris(p.shape)
        v = v + np.array(p.explode)
        allq.append((v[t] @ P.T)[..., :2].reshape(-1, 2)); items.append((p, v))
    q = np.vstack(allq); lo, hi = q.min(0), q.max(0)
    span = (hi - lo).max() * (1 + 2 * pad); c = (lo + hi) / 2; scale = min(W, H) / span

    def px(pt):
        xy = np.asarray(pt) @ P.T
        return np.array([(xy[0] - c[0]) * scale + W / 2, H / 2 - (xy[1] - c[1]) * scale]) / ss

    img = plt.imread(str(out))
    fig = plt.figure(figsize=size, dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(img); ax.set_axis_off()
    for p, v in items:
        if p.bom is None:
            continue
        x, y = px(v.mean(0))
        dx, dy = CALLOUT.get(p.bom, (60, 0))
        ax.plot([x, x + dx], [y, y + dy], color=concept.INK, lw=0.7)
        ax.plot([x], [y], marker="o", ms=2.5, color=concept.INK)
        ax.text(x + dx, y + dy, f"{p.bom}", fontsize=8, fontweight="bold", color="white", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.3", fc=concept.ACCENT, ec="white", lw=0.8))
    handles = [plt.Line2D([], [], marker="o", ls="", mfc=p.color, mec=concept.INK, ms=7, label=f"{p.bom}  {p.name}")
               for p in parts if p.bom is not None]
    ax.legend(handles=handles, loc="upper left", frameon=False, fontsize=7.5, bbox_to_anchor=(0.0, 0.9))
    fig.savefig(out, facecolor="white"); plt.close(fig)


if __name__ == "__main__":
    render_all(
        parts, project="ConePro", title="Digital dynamic cone penetrometer concept", dwg_no="CNP-DWG-010",
        key_figures=["ASTM D6951 geometry: 8 kg hammer, 575 mm drop",
                     "About 45 J per blow; 16 mm rod, 20 mm 60 deg cone",
                     "About 28 J at the cone (estimate, CNP-CAL-001)",
                     "Draw-wire depth: 0.05 mm resolution; 850 mm per rod",
                     "About 15.7 kg with bag; about $335 in parts"],
        cut=False,
        flow={"title": "energy per blow, J (estimates)", "unit": "J",
              "stages": [("Hammer at 575 mm", 45.1), ("At impact", 43.8), ("Into rod", 29.5),
                         ("At cone", 28.0), ("Work on soil", 28.0)],
              "losses": [(0, "Guide friction (3 %)", 1.4), (1, "Impact, e = 0.4 (33 %)", 14.3),
                         (2, "Rod wave, side friction (5 %)", 1.5)]},
    )
    # The kit now places numbered callouts on visible pixels with leaders, so its exploded view is kept
    # (the earlier leader redraw no longer matched the kit's cropped layout).
    import shutil
    for tmp in ("_views", "_views_fig"):
        shutil.rmtree(ROOT / "media" / tmp, ignore_errors=True)
