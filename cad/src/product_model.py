"""ConePro product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders, built on the constructable parts of model.py
(updated 2026-10-02 to the design for construction and Amish's decisions of that day): a painted
drop hammer with bare strike faces, three grip grooves, its magnet ring and the "fit the end cap"
label; spanner flats on the cone, lower rod and anvil; rod graduations; the pinned stop collar, the
welded T-handle tube with 33 mm ribbed rubber grips and the level on its seat; an anodized
reference plate; the draw-wire reel at its constructable position with a clear window onto the
drum; the one-piece clamp and wire arm; the curved sensor pad under its band clamp; the flanged
logger box with its glands and a clear window onto its AA cells; a lit status LED and a button;
the coiled sensor cable and reel cable; the end cap lying beside the plate; a patch of ground and
a phone showing a penetration curve for context. The windows are render-only (decided by Amish on
2026-10-02); the parts themselves are opaque.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and derived() in model.py.
Axes as model.py: the rod axis is Z, the ground at z = 0 with the cone point touching it, the
draw-wire reel on +X and the logger on -X; front is -Y.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Align, Axis, Box, Compound, Cone, Cylinder, Helix, Plane, Pos,
                       RectangleRounded, Rot, Solid, Sphere, Vector, extrude, fillet, scale)
from model import PARAMS, derived, build_components, build_parts, end_cap

TITLE = "ConePro: digital dynamic cone penetrometer that logs soil strength to a phone"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation); the instrument "
             "stands upright on a patch of ground with the teal drop hammer resting on the anvil, the "
             "draw-wire reel at right, the logger at left and a phone showing the penetration curve"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): T-handle and top "
             "stop, upper rod, drop hammer, anvil, lower rod and cone on the axis; sensor pad and "
             "band clamp, logger and cable at left; clamp arm, draw-wire reel and drum at right; "
             "reference plate below; spare cone, cover and the end cap for the upper rod"},
    {"name": "detail", "groups": ["shell", "internal", "context"], "explode": False, "el": 58, "az": -35,
     "note": "Detail from the front right and high above (about 58 deg elevation), looking down the rod "
             "onto the reference plate: draw-wire reel with the drum behind its window, logger with "
             "its cells behind the lid window and the status light lit, and the phone"},
]

# Colors (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_STEEL = "#8C939C"
C_STEEL_DK = "#4B5058"
C_CHROME = "#C7CCD3"
C_HARD = "#3E4248"
C_ALU = "#A9B1BB"
C_ANOD = "#B58A34"
C_BLACK = "#1F2328"
C_RUBBER = "#2B2F36"
C_SHELL = "#E4E7EB"
C_SHELL2 = "#C3CAD2"
C_WINDOW = "#DCEBF5"
C_MARK = "#1F2937"
C_LABEL = "#F4F4F2"
C_LED = "#22C55E"
C_CELL = "#334155"
C_STAINLESS = "#D1D5DB"
C_SOIL = "#8B7560"
C_PEBBLE = "#9A948A"
C_PHONE = "#23272E"
C_SCREEN = "#E7F4F1"

# Appearance-only detail sizes (mm)
GROUND = 560.0          # side of the context ground patch
GROUND_D = 70.0         # its visible depth
REEL_WALL = 2.5
LOG_WALL = 2.5


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _cyl(r, h, z, x=0.0, y=0.0):
    """Vertical cylinder from z up by h."""
    return Pos(x, y, z) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def _ring(ro, ri, h, z, x=0.0, y=0.0):
    return _cyl(ro, h, z, x, y) - _cyl(ri, h + 2, z - 1, x, y)


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    v = b - a
    return Solid.make_cylinder(r, v.length, Plane(origin=a, z_dir=v.normalized()))


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _coil(a, b, coil_r, wire_r, pitch, seg_per_turn=8):
    """Coiled cable from a to b as a chain of short straight tubes (light to tessellate)."""
    a, b = Vector(*a), Vector(*b)
    L = (b - a).length
    turns = max(1, round(L / pitch))
    h = Helix(L / turns, L, coil_r)
    n = turns * seg_per_turn
    pts = [h.position_at(i / n) for i in range(n + 1)]
    segs = []
    for p, q in zip(pts, pts[1:]):
        v = q - p
        d = v.normalized()
        segs.append(Solid.make_cylinder(wire_r, v.length + 2 * wire_r * 0.4, Plane(origin=p - d * wire_r * 0.4, z_dir=d)))
    loc = Plane(origin=a, z_dir=(b - a).normalized()).location
    return Compound(children=[loc * s for s in segs])


def _grooves(shape, r_out, depth, width, zs, x=0.0, y=0.0):
    """Cut circumferential grooves round a vertical cylinder of radius r_out at heights zs."""
    for z in zs:
        shape -= _ring(r_out + 2, r_out - depth, width, z - width / 2, x, y)
    return shape


def _fuse_list(shapes):
    shapes = [x for x in shapes if x is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS):
    D = derived(P)
    C = build_components(P)
    m = build_parts(P, comps=C)
    rr = P["rod_d"] / 2
    T = P["plate_t"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # explode offsets per component, based on cad/src/concept_media.py (vertical spread trimmed)
    E = {"cone": (0, 0, -90), "lower_rod": (0, 0, -30), "anvil": (0, 0, 60), "hammer": (-330, -330, 420),
         "upper_rod": (0, 0, 150), "handle": (0, 0, 230), "plate": (0, 0, -200), "reel": (330, 330, -150),
         "clamp": (330, 330, 60), "pad": (-330, 330, 60), "logger": (-330, 330, -150), "cable": (-450, 250, 0)}

    def ex(key, dx=0.0, dy=0.0, dz=0.0):
        x, y, z = E[key]
        return (x + dx, y + dy, z + dz)

    # ---- 1 cone: hardened, darker steel; filleted shoulder
    cone = m["cone"][1]
    cone = _fillet_try(cone, _top_edges(cone), [1.0, 0.6, 0.3])
    add("Hardened cone", cone, C_HARD, "metal", 1, "shell", ex("cone"))

    # ---- 2 lower drive rod with engraved graduations every 10 mm (heavier every 100 mm)
    add("Lower drive rod", m["lower_rod"][1], C_STEEL, "metal", 2, "shell", ex("lower_rod"))
    marks = []
    for k in range(1, 98):
        z = D["z_rod"] + 10.0 * k
        if z > D["collar_top"] - P["collar_h"] - 4:
            break
        major = k % 10 == 0
        if D["z_rod"] + P["flats_rod_z"] - 2 < z < D["z_rod"] + P["flats_rod_z"] + P["flats_rod"][1] + 2:
            continue                     # no ring across the spanner flats
        marks.append(_ring(rr + 0.15, rr - 0.5, 1.4 if major else 0.6, z - 0.3))
    add("Rod graduations (10 mm)", Compound(children=marks), C_MARK, "painted", 2, "shell", ex("lower_rod"))

    # ---- 3 anvil and coupler: the constructable anvil from model.py (tapped both ends, spanner flats)
    za, ha, ra = D["z_anvil"], P["anvil_h"], P["anvil_d"] / 2
    anvil = C["anvil"].shape
    anvil = _fillet_try(anvil, [e for e in _top_edges(anvil) if e.radius > ra - 1], [1.0, 0.6])
    add("Anvil and coupler", anvil, C_STEEL_DK, "metal", 3, "shell", ex("anvil"))

    # ---- 4 drop hammer: model hammer (grip grooves, magnet pockets), painted body, bare strike faces, label
    hz, hL = D["z_anvil_top"], D["hammer_L"]
    face_h = 5.0
    ham = C["hammer"].shape
    win_body = Pos(0, 0, hz + face_h) * Box(300, 300, hL - 2 * face_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    add("Drop hammer body (painted)", ham & win_body, C_ACCENT, "painted", 4, "shell", ex("hammer"))
    add("Hammer strike faces", ham - win_body, C_STEEL, "metal", 4, "shell", ex("hammer"))
    add("Hammer magnet ring (16 x N42)", C["magnets"].shape, C_STAINLESS, "metal", 4, "internal", ex("hammer"))
    add("Hammer label (fit the end cap)", C["label"].shape, C_LABEL, "paper", 4, "shell", ex("hammer"))

    # ---- 5 upper rod (hammer guide), bright steel
    add("Upper rod (hammer guide)", m["upper_rod"][1], C_CHROME, "metal", 5, "shell", ex("upper_rod"))

    # ---- 6 handle: pinned stop collar, welded tube, rubber grips, level seat and bubble level (model.py)
    add("Top stop collar and roll pin", _fuse_list([C["stop"].shape, C["pin"].shape]), C_STEEL_DK, "metal", 6, "shell", ex("handle"))
    add("T-handle tube (powder coat)", C["tube"].shape, C_BLACK, "painted", 6, "shell", ex("handle"))
    zh = D["z_handle"]
    gd = P["grip"][0]
    grips = C["grips"].shape
    for sgn in (-1, 1):                  # appearance ribs on the grips
        for k in range(8):
            yk = sgn * (P["handle_w"] / 2 - 12.0 - 10.0 * k)
            grips -= Pos(0, yk, zh) * Rot(90, 0, 0) * (Cylinder(gd / 2 + 2, 2.0) - Cylinder(gd / 2 - 1.0, 3.0))
    add("Handle grips (ribbed rubber)", grips, C_RUBBER, "rubber", 6, "shell", ex("handle"))
    add("Level seat disc", C["seat"].shape, C_STEEL_DK, "metal", 6, "shell", ex("handle"))
    add("Bubble level", C["level"].shape, "#D9F99D", "clear", 6, "shell", ex("handle"))

    # ---- 7 reference plate: anodized, rounded corners, markings
    plate = m["plate"][1]
    corners = [e for e in plate.edges().filter_by(Axis.Z)
               if abs(e.center().X) > P["plate"] / 2 - 1 and abs(e.center().Y) > P["plate"] / 2 - 1]
    plate = _fillet_try(plate, corners, [14.0, 10.0, 6.0])
    add("Reference plate (anodized)", plate, C_ALU, "metal", 7, "shell", ex("plate"))
    mk = []
    hr = P["plate_hole"] / 2
    for a in (0, 90, 180):   # zero-depth ticks round the hole (the slot is on -Y)
        mk.append(Rot(0, 0, a) * Pos(hr + 9.0, 0, T) * Box(12.0, 2.0, 0.3, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    mk.append(_prism(70.0, 16.0, 3.0, T, 0.3, x=-95.0, y=-95.0))
    add("Plate markings", Compound(children=mk), C_MARK, "painted", 7, "shell", ex("plate"))
    add("Plate nameplate", _prism(62.0, 10.0, 2.0, T + 0.3, 0.2, x=-95.0, y=-95.0), C_LABEL, "paper", 7, "shell",
        ex("plate"))

    # ---- 8 draw-wire depth sensor: model housing, lid, drum and internals; the window is render-only
    rx, ry = P["reel_xy"]
    cx, bz_c = D["drum_cx"], D["drum_cz"]
    by = P["reel_box"][1]
    hy0 = ry - by / 2
    dr = P["drum_d"] / 2
    window = Pos(cx, hy0 - 1, bz_c) * Rot(-90, 0, 0) * Cylinder(dr - 6.0, P["reel_wall"] + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    add("Draw-wire housing (IP65)", C["reel_body"].shape, C_SHELL, "plastic", 8, "shell", ex("reel"))
    add("Draw-wire housing lid", C["reel_lid"].shape - window, C_SHELL2, "plastic", 8, "shell", ex("reel", dy=-60))
    add("Draw-wire drum window (render only)", C["reel_lid"].shape & window, C_WINDOW, "clear", 8, "shell", ex("reel", dy=-60))
    add("Housing screws", _fuse_list([C["lid_screws"].shape, C["reel_screws"].shape]), C_STAINLESS, "metal", 14, "shell", ex("reel"))
    add("Grooved aluminum drum and shaft", _fuse_list([C["drum"].shape, C["shaft"].shape, C["magnet"].shape]), C_CHROME, "metal", 8,
        "internal", ex("reel", dy=-130))
    add("Spring motor", C["motor"].shape, "#B45309", "metal", 8, "internal", ex("reel", dy=-100))
    add("Angle sensor board", C["board"].shape, "#16A34A", "plastic", 8, "internal", ex("reel", dy=-80))
    add("Wire exit eyelet", C["eyelet"].shape, C_STAINLESS, "metal", 8, "shell", ex("reel"))
    add("Draw wire (coated steel)", _rod((rx, ry, D["reel_top"]), (rx, ry, D["collar_top"] + 20.0), 1.0),
        "#9CA3AF", "metal", 8, "shell", ex("reel"))

    # ---- 9 one-piece clamp collar and wire arm (model.py), anodized, with its screw, eye spring and wire stop
    add("Clamp collar and wire arm (anodized)", C["clamp"].shape, C_ANOD, "metal", 9, "shell", ex("clamp"))
    add("Clamp screw", C["clamp_screw"].shape, C_BLACK, "metal", 14, "shell", ex("clamp"))
    add("Eye spring and wire stop", _fuse_list([C["eye_spring"].shape, C["crimp"].shape]), C_STAINLESS, "metal", 8, "shell", ex("clamp"))

    # ---- 10 sensor pad: curved pad on a curved isolator, band over the pad (model.py)
    pr, pt, ph = P["pad"]
    pad_top = D["pad_top"]
    x_in = -ra
    add("Pad elastomer isolator", C["isolator"].shape, C_RUBBER, "rubber", 10, "shell", ex("pad"))
    add("Potted sensor pad", C["pad"].shape, "#3A3F47", "plastic", 10, "shell", ex("pad", dx=-50))
    stripe = Pos(x_in - pr - 0.2, 0, pad_top - 5.0) * Box(0.4, pt - 8.0, 3.0)
    add("Pad accent stripe", stripe, C_ACCENT, "painted", 10, "shell", ex("pad", dx=-50))
    add("Stainless band clamp", C["band"].shape, C_STAINLESS, "metal", 10, "shell", ex("pad"))

    # ---- 11 logger: model flanged box, glands and screws; lid with a render-only window over the cells
    lx, ly = P["logger_xy"]
    Lb, Wb, Hb = P["logger_box"]
    lx0, ly0 = lx - Lb / 2, ly - Wb / 2
    wl = P["logger_wall"]
    wx, wy = lx0 + 35.0, ly0 + 32.5
    lwin = _prism(56.0, 44.0, 3.0, T + Hb - 6.0, 8.0, x=wx, y=wy)
    llid = C["logger_lid"].shape - lwin
    bxn, byn = lx + 34.0, ly + 18.0
    ledx, ledy = lx + 34.0, ly - 14.0
    llid -= _cyl(6.2, 10, T + Hb - 5, bxn, byn)
    llid -= _cyl(2.0, 10, T + Hb - 5, ledx, ledy)
    add("Logger box (IP65, flanged)", C["logger"].shape, C_SHELL, "plastic", 11, "shell", ex("logger"))
    add("Logger lid", llid, C_SHELL2, "plastic", 11, "shell", ex("logger", dz=90))
    add("Logger cell window (render only)", C["logger_lid"].shape & lwin, C_WINDOW, "clear", 11, "shell", ex("logger", dz=90))
    add("Logger flange screws", C["flange_screws"].shape, C_STAINLESS, "metal", 14, "shell", ex("logger"))
    btn = _cyl(5.6, 4.5, T + Hb - 3.0, bxn, byn)
    btn = _fillet_try(btn, _top_edges(btn), [1.5, 1.0, 0.5])
    add("Logger button", btn, C_ACCENT, "rubber", 11, "shell", ex("logger", dz=90))
    led = _cyl(1.9, 3.0, T + Hb - 2.4, ledx, ledy)
    led = _fillet_try(led, _top_edges(led), [0.8, 0.5])
    add("Status LED (lit)", led, C_LED, "emissive", 11, "shell", ex("logger", dz=90))
    add("Cable glands (3)", C["glands"].shape, C_BLACK, "plastic", 11, "shell", ex("logger"))
    lab = Pos(lx, ly0 - 0.1, T + 20.0) * Box(58.0, 0.3, 14.0)
    add("Logger label", lab, C_LABEL, "paper", 11, "shell", ex("logger"))
    cells = []
    for k in (-1, 0, 1):
        c_ = Pos(wx + 15.0 * k, wy, T + wl + 8.0) * Rot(90, 0, 0) * Cylinder(7.25, 44.0)
        cells.append(_fillet_try(c_, c_.edges(), [0.8, 0.5]))
    add("AA cells (3)", Compound(children=cells), C_CELL, "painted", 11, "internal", ex("logger", dz=45))
    add("Cell holder and logger board", _fuse_list([C["module"].shape]), C_BLACK, "plastic", 11, "internal", ex("logger", dz=45))

    # ---- 12 coiled cable from the pad to its logger gland; 17 reel cable in its P-clips (model.py)
    c = P["cable_d"] / 2
    a = (-ra - P["isolator_t"] - (pr - P["isolator_t"]) / 2, 0, D["pad_bot"])
    a2 = (a[0], 0, a[2] - 14.0)
    mpt = (-(ra + 38), -40, D["z_anvil"] - 250)
    lx1 = lx + Lb / 2
    b = (lx1 + 16, P["gland_y"][0], T + 21.0)
    e_ = (lx1 + 6, P["gland_y"][0], T + 21.0)
    cable = [_rod(a, a2, c), _coil(a2, mpt, 8.0, c, 9.0), _coil(mpt, b, 6.0, c, 45.0), _rod(b, e_, c)]
    add("Coiled sensor cable", Compound(children=cable), C_BLACK, "rubber", 12, "shell", ex("cable"))
    add("Reel-to-logger cable and P-clips", _fuse_list([C["reel_cable"].shape, C["pclips"].shape]), C_BLACK, "rubber", 17,
        "shell", ex("logger", dx=200))

    # ---- accessory: the end cap for the upper rod's stud, lying beside the plate (BOM 14)
    cap = end_cap(P)
    cap = Pos(200.0, 60.0, P["end_cap"][0] / 2) * Rot(0, 90, 0) * Pos(0, 0, -(D["z_anvil_top"] - P["end_cap"][1] / 2)) * cap
    add("End cap for the upper rod (aluminum)", cap, C_ALU, "metal", 14, "accessory", (0, -80, -200))

    # ---- accessory: spare cone with its cover (BOM 1 and 14), lying beside the plate
    sp = Pos(180.0, -150.0, P["cone_d"] / 2) * Rot(0, 0, 25) * Rot(0, -90, 0) * Pos(0, 0, -D["z_rod"] / 2) * m["cone"][1]
    add("Spare cone", sp, C_HARD, "metal", 1, "accessory", (0, -80, -200))
    cover = Pos(0, 0, -2.0) * (Cone(P["cone_d"] / 2 + 3.0, 4.0, m["cone"][1].bounding_box().size.Z - P["cone_shoulder"] + 4.0,
                                   align=(Align.CENTER, Align.CENTER, Align.MIN))
                               - Cone(P["cone_d"] / 2 + 0.5, 0.5, D["cone_h"] + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cover = Pos(250.0, -110.0, P["cone_d"] / 2 + 3.0) * Rot(0, 0, 25) * Rot(0, -90, 0) * Pos(0, 0, -D["z_rod"] / 2) * cover
    add("Cone cover (rubber)", cover, C_RUBBER, "rubber", 14, "accessory", (0, -80, -200))

    # ---- context: patch of ground, pebbles and the user's phone showing the curve
    ground = Pos(0, 0, -GROUND_D) * Box(GROUND, GROUND, GROUND_D, align=(Align.CENTER, Align.CENTER, Align.MIN))
    ground = _fillet_try(ground, _top_edges(ground), [18.0, 10.0, 5.0])
    ground = _fillet_try(ground, ground.edges().filter_by(Axis.Z), [18.0, 10.0])
    ground -= _cyl(2.0, 6.0, -5.0)          # tiny seat under the cone point
    add("Ground patch (soil)", ground, C_SOIL, "clay", None, "context", (0, 0, 0))
    pebbles = []
    for (x, y, r, sz) in [(215, -200, 14, 0.55), (-225, -235, 10, 0.5), (200, 215, 12, 0.5), (-230, 175, 16, 0.45),
                          (60, -235, 8, 0.6), (-40, 235, 11, 0.5), (240, 40, 9, 0.55), (-245, -30, 7, 0.6)]:
        pebbles.append(Pos(x, y, 0) * scale(Sphere(r), (1.0, 0.8, sz)))
    add("Pebbles", Compound(children=pebbles), C_PEBBLE, "clay", None, "context", (0, 0, 0))
    ph_l, ph_w, ph_t = 150.0, 72.0, 8.0
    phone = _prism(ph_l, ph_w, 9.0, 0.0, ph_t)
    phone = _fillet_try(phone, _top_edges(phone), [2.5, 1.5])
    phone = _fillet_try(phone, _bottom_edges(phone), [2.0, 1.0])
    screen = _prism(ph_l - 8, ph_w - 6, 6.0, ph_t, 0.2)
    curve_pts = [(-55, 22), (-45, 18), (-35, 15), (-25, 6), (-15, -2), (-5, -8), (5, -12), (15, -15), (25, -17),
                 (35, -22), (45, -27), (55, -29)]
    curve = [Pos((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, ph_t + 0.2) *
             Rot(0, 0, math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))) *
             Box(math.hypot(q[0] - p[0], q[1] - p[1]) + 1.2, 1.2, 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
             for p, q in zip(curve_pts, curve_pts[1:])]
    axes_ = [Pos(-60, 0, ph_t + 0.2) * Box(0.6, 56, 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN)),
             Pos(0, 27, ph_t + 0.2) * Box(124, 0.6, 0.2, align=(Align.CENTER, Align.CENTER, Align.MIN))]
    place = Pos(-205.0, -170.0, 0.0) * Rot(0, 0, 28)
    add("Phone (user's own)", place * phone, C_PHONE, "plastic", None, "context", (0, 0, 0))
    add("Phone screen (lit)", place * screen, C_SCREEN, "emissive", None, "context", (0, 0, 0))
    add("Penetration curve on screen", place * Compound(children=curve), C_ACCENT, "painted", None, "context", (0, 0, 0))
    add("Screen axes", place * Compound(children=axes_), "#6B7280", "painted", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:38s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
