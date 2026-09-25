"""ConePro concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The rod axis is the Z axis, ground at Z = 0, and the instrument is shown
set up at the start of a test: cone tip on the ground, reference plate flat on the ground and
the 8 kg hammer resting on the anvil. Mechanical geometry follows ASTM D6951 (16 mm rod,
20 mm 60 degree cone, 8 kg hammer, 575 mm drop).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot, Solid, Plane, Vector, Align
from concept import Part, render_all

ROD_R = 8.0                  # 16 mm drive rod
CONE_R = 10.0                # 20 mm cone base
CONE_H = CONE_R / 0.57735    # 60 degree apex angle: h = r / tan(30 deg), about 17.3 mm
LOWER_ROD = 1000.0
ANVIL_R, ANVIL_H = 32.0, 60.0
HAMMER_OD, HAMMER_ID, HAMMER_L = 100.0, 22.0, 136.0   # about 8.0 kg of steel
DROP = 575.0
PLATE, PLATE_T = 300.0, 8.0

BASE = (Align.CENTER, Align.CENTER, Align.MIN)   # base of the solid at its placement z


def cyl(r, h, z, x=0.0, y=0.0):
    """Vertical cylinder of radius r and height h with its base at z."""
    return Pos(x, y, z) * Cylinder(r, h, align=BASE)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


# 1 Cone: 60 degree point, 20 mm base, short shoulder
z_cone_top = CONE_H + 5.0
cone = Cone(0.4, CONE_R, CONE_H, align=BASE) + cyl(CONE_R, 5.0, CONE_H)

# 2 Lower drive rod, 1,000 mm, engraved every 10 mm as a manual backup scale
z_rod = z_cone_top
lower_rod = cyl(ROD_R, LOWER_ROD, z_rod)

# 3 Anvil and coupler
z_anvil = z_rod + LOWER_ROD
anvil = cyl(ANVIL_R, ANVIL_H, z_anvil)

# 5 Upper rod (hammer guide): hammer length plus 575 mm drop plus a stop allowance
z_upper = z_anvil + ANVIL_H
UPPER = HAMMER_L + DROP + 40.0
upper_rod = cyl(ROD_R, UPPER, z_upper)

# 4 Hammer, 8 kg, resting on the anvil
hammer = cyl(HAMMER_OD / 2, HAMMER_L, z_upper) - cyl(HAMMER_ID / 2, HAMMER_L + 2, z_upper - 1)

# 6 Handle and top stop
z_top = z_upper + UPPER
handle = cyl(22.0, 18.0, z_top) + Pos(0, 0, z_top + 34) * Rot(90, 0, 0) * Cylinder(13.0, 260.0)
handle = handle + cyl(ROD_R, 34.0, z_top + 10)

# 7 Reference plate with a slot so it lifts off around the rod
plate = Box(PLATE, PLATE, PLATE_T, align=BASE)
plate = plate - cyl(30.0, PLATE_T + 2, -1) - Pos(0, -PLATE / 4, -1) * Box(60.0, PLATE / 2 + 2, PLATE_T + 2,
                                                                          align=BASE)

# 8 Draw-wire depth sensor on the plate, wire up to the anvil clamp arm
DW_X = 105.0
dw_box = Pos(DW_X, 40.0, PLATE_T) * Box(60.0, 56.0, 60.0, align=BASE)
wire_top = z_anvil - 30.0
wire = tube3((DW_X, 40.0, PLATE_T + 60.0), (DW_X, 40.0, wire_top), 1.2)
drawwire = dw_box + wire

# 9 Anvil clamp collar and wire arm
clamp = cyl(20.0, 22.0, wire_top - 6) + Pos(DW_X / 2 + 6, 20.0, wire_top + 5) * Rot(0, 0, 21) * Box(DW_X + 14, 16.0, 12.0)

# 10 Hall-effect blow sensor, potted, in a pad on the anvil (magnet ring in the hammer face)
hall = Pos(ANVIL_R + 11.0, 0, z_anvil + ANVIL_H / 2) * Box(22.0, 30.0, 40.0)

# 11 BLE logger box on the plate (electronics kept off the anvil to limit shock)
logger = Pos(-95.0, 55.0, PLATE_T) * Box(100.0, 70.0, 42.0, align=BASE)

# 12 Coiled sensor cable from the anvil sensor to the logger
cable = (tube3((ANVIL_R + 18.0, -10.0, z_anvil + 10), (ANVIL_R + 30.0, -60.0, z_anvil - 200), 3.0)
         + tube3((ANVIL_R + 30.0, -60.0, z_anvil - 200), (-60.0, 75.0, PLATE_T + 42.0), 3.0))

parts = [
    Part("Hardened cone, 20 mm, 60 degree", cone, "#B45309", 1, (0, 0, -110)),
    Part("Lower drive rod, 16 mm x 1,000 mm", lower_rod, "#6B7280", 2, (0, 0, -30)),
    Part("Anvil and coupler", anvil, "#374151", 3, (0, 0, 60)),
    Part("Drop hammer, 8 kg", hammer, "#0F766E", 4, (-330, -330, 420)),
    Part("Upper rod (hammer guide)", upper_rod, "#9CA3AF", 5, (0, 0, 150)),
    Part("Handle and top stop", handle, "#111827", 6, (0, 0, 260)),
    Part("Reference plate, slotted", plate, "#94A3B8", 7, (0, 0, -260)),
    Part("Draw-wire depth sensor", drawwire, "#2563EB", 8, (330, 330, -150)),
    Part("Anvil clamp and wire arm", clamp, "#D4A017", 9, (330, 330, 60)),
    Part("Hall-effect blow sensor", hall, "#7C3AED", 10, (330, -330, 60)),
    Part("BLE logger, 3 x AA", logger, "#16A34A", 11, (-330, 330, -150)),
    Part("Coiled sensor cable", cable, "#1F2937", 12, (-450, 250, 0)),
]

# Callout offsets for the exploded view, in screen pixels (dx right, dy down) from each part.
# The kit places callouts on the part itself, which hides the small sensor parts on a 1.9 m tall
# assembly, so the view is redrawn below with leader lines.
CALLOUT = {1: (70, 0), 2: (60, 40), 3: (60, 0), 4: (-60, -40), 5: (60, 0), 6: (60, 10),
           7: (-90, 10), 8: (60, 30), 9: (60, -30), 10: (60, -10), 11: (-70, 0), 12: (-60, 0)}


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
                     "Draw-wire depth: 1 mm resolution target",
                     "About 850 mm per rod; about 15 kg (estimate)",
                     "About $300 in parts (indicative)"],
        cut=False,
        flow={"title": "energy per blow, J (estimates)", "unit": "J",
              "stages": [("Hammer at 575 mm", 45.1), ("At impact", 43.8), ("Into rod", 35.0),
                         ("At cone", 33.3), ("Work on soil", 33.3)],
              "losses": [(0, "Guide friction (3 %)", 1.3), (1, "Rebound, anvil (20 %)", 8.8),
                         (2, "Rod wave, side friction (5 %)", 1.7)]},
    )
    exploded_with_leaders(parts, Path("media") / "exploded.png")
    import shutil
    for tmp in ("_views", "_views_fig"):
        shutil.rmtree(Path("media") / tmp, ignore_errors=True)
