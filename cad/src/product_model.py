"""ConePro product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: machined and filleted steel parts, a painted drop
hammer with bare strike faces, grip grooves and its magnet ring, rod graduations, a T-handle with
ribbed rubber grips and a bubble level, an anodized reference plate with markings, a draw-wire
reel housing with a clear window onto the drum, a split clamp collar and wire arm with its eye, a
potted sensor pad on its band clamp, a logger box with a clear window onto its AA cells, a lit
status LED, a scan button and a cable gland, a coiled sensor cable, a patch of ground and a phone
showing a penetration curve for context.
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
from model import PARAMS, derived, build_parts

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
             "reference plate below; spare cone and cover"},
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


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
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
        marks.append(_ring(rr + 0.15, rr - 0.5, 1.4 if major else 0.6, z - 0.3))
    add("Rod graduations (10 mm)", Compound(children=marks), C_MARK, "painted", 2, "shell", ex("lower_rod"))

    # ---- 3 anvil and coupler: filleted, with the coupler seam
    za, ha, ra = D["z_anvil"], P["anvil_h"], P["anvil_d"] / 2
    anvil = _cyl(ra, ha, za)
    anvil = _fillet_try(anvil, _top_edges(anvil), [2.0, 1.2, 0.6])
    anvil = _fillet_try(anvil, _bottom_edges(anvil), [2.0, 1.2, 0.6])
    anvil = _grooves(anvil, ra, 0.6, 0.8, [za + 20.0])
    add("Anvil and coupler", anvil, C_STEEL_DK, "metal", 3, "shell", ex("anvil"))

    # ---- 4 drop hammer: painted body, bare strike faces, grip grooves, magnet ring, label
    hz, hL = D["z_anvil_top"], D["hammer_L"]
    ro, ri = P["hammer_od"] / 2, P["hammer_id"] / 2
    face_h = 5.0
    body = _ring(ro, ri, hL - 2 * face_h, hz + face_h)
    body = _grooves(body, ro, 1.2, 2.2, [hz + 38.0 + 7.0 * i for i in range(6)])
    add("Drop hammer body (painted)", body, C_ACCENT, "painted", 4, "shell", ex("hammer"))
    low = _ring(ro, ri, face_h, hz)
    low = _fillet_try(low, [e for e in _bottom_edges(low) if e.radius > ro - 1], [2.5, 1.5, 0.8])
    upp = _ring(ro, ri, face_h, hz + hL - face_h)
    upp = _fillet_try(upp, [e for e in _top_edges(upp) if e.radius > ro - 1], [2.5, 1.5, 0.8])
    mag_r = (ro + ra) / 2 + 3.0
    for k in range(16):
        a = math.radians(360.0 * k / 16)
        low -= _cyl(4.0, 4.0, hz - 0.5, mag_r * math.cos(a), mag_r * math.sin(a))
    add("Hammer strike faces", low + upp, C_STEEL, "metal", 4, "shell", ex("hammer"))
    mags = [_cyl(4.0, 3.5, hz + 0.1, mag_r * math.cos(math.radians(22.5 * k)), mag_r * math.sin(math.radians(22.5 * k)))
            for k in range(16)]
    add("Hammer magnet ring (16 x N42)", Compound(children=mags), C_STAINLESS, "metal", 4, "internal", ex("hammer"))
    lab_z = hz + 88.0
    label = _ring(ro + 0.3, ro - 0.2, 26.0, lab_z) & (Rot(0, 0, -50) * Pos(ro, 0, lab_z + 13.0) * Box(30, 44, 30))
    add("Hammer label (8.0 kg)", label, C_LABEL, "paper", 4, "shell", ex("hammer"))

    # ---- 5 upper rod (hammer guide), bright steel
    add("Upper rod (hammer guide)", m["upper_rod"][1], C_CHROME, "metal", 5, "shell", ex("upper_rod"))

    # ---- 6 handle: stop collar, stem, tee, powder-coated bar, ribbed rubber grips, bubble level
    zs, sh = D["z_stop"], P["stop_h"]
    stop = _cyl(P["stop_d"] / 2, sh, zs)
    stop = _fillet_try(stop, _top_edges(stop), [2.0, 1.0])
    stop = _fillet_try(stop, _bottom_edges(stop), [2.0, 1.0])
    stop = _grooves(stop, P["stop_d"] / 2, 0.6, 0.8, [zs + sh / 2])
    screw = Pos(0, -P["stop_d"] / 2 - 1.5, zs + sh / 2) * Rot(90, 0, 0) * Cylinder(4.0, 4.0)
    add("Top stop collar", stop + screw, C_STEEL_DK, "metal", 6, "shell", ex("handle"))
    zh = D["z_handle"]
    od, t = P["handle_tube"]
    stem = _cyl(rr, P["handle_stem"] + 4.0, zs + sh)
    tee = Pos(0, 0, zh) * Rot(90, 0, 0) * Cylinder(od / 2 + 2.5, 44.0)
    tee = _fillet_try(tee, tee.edges(), [2.0, 1.0])
    tee += _cyl(rr + 3.0, 16.0, zh - od / 2 - 14.0)
    bar = Pos(0, 0, zh) * Rot(90, 0, 0) * (Cylinder(od / 2, P["handle_w"] - 6.0) - Cylinder(od / 2 - t, P["handle_w"]))
    add("T-handle frame (powder coat)", stem + tee + bar, C_BLACK, "painted", 6, "shell", ex("handle"))
    grips = None
    gl = 84.0
    for s in (-1, 1):
        yc = s * (P["handle_w"] / 2 - gl / 2)
        g = Pos(0, yc, zh) * Rot(90, 0, 0) * Cylinder(od / 2 + 3.5, gl)
        g = _fillet_try(g, g.edges(), [3.0, 2.0, 1.0])
        g -= Pos(0, yc, zh) * Rot(90, 0, 0) * Cylinder(od / 2 - t, gl + 2)
        for k in range(-4, 5):
            g -= Pos(0, yc + 8.0 * k, zh) * Rot(90, 0, 0) * (Cylinder(od / 2 + 5, 2.0) - Cylinder(od / 2 + 2.6, 3.0))
        grips = g if grips is None else grips + g
    add("Handle grips (ribbed rubber)", grips, C_RUBBER, "rubber", 6, "shell", ex("handle"))
    lz = zh + od / 2
    level = Pos(0, 0, lz) * Box(16, 30, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    level = _fillet_try(level, level.edges().filter_by(Axis.Z), [2.5, 1.5])
    level = _fillet_try(level, _top_edges(level), [1.2, 0.8])
    level -= Pos(0, 0, lz + 8.0) * Box(8.0, 22.0, 5.0)
    add("Bubble level housing", level, C_RUBBER, "plastic", 6, "shell", ex("handle"))
    vial = Pos(0, 0, lz + 5.2) * Rot(90, 0, 0) * Cylinder(3.0, 20.0)
    add("Bubble level vial", vial, "#D9F99D", "clear", 6, "shell", ex("handle"))

    # ---- 7 reference plate: anodized, rounded corners, markings
    plate = m["plate"][1]
    corners = [e for e in plate.edges().filter_by(Axis.Z)
               if abs(e.center().X) > P["plate"] / 2 - 1 and abs(e.center().Y) > P["plate"] / 2 - 1]
    plate = _fillet_try(plate, corners, [14.0, 10.0, 6.0])
    plate = _fillet_try(plate, _top_edges(plate), [1.2, 0.8, 0.5])
    add("Reference plate (anodized)", plate, C_ALU, "metal", 7, "shell", ex("plate"))
    mk = []
    hr = P["plate_hole"] / 2
    for a in (0, 90, 180):   # zero-depth ticks round the hole (the slot is on -Y)
        mk.append(Rot(0, 0, a) * Pos(hr + 9.0, 0, T) * Box(12.0, 2.0, 0.3, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    mk.append(_prism(70.0, 16.0, 3.0, T, 0.3, x=-95.0, y=-95.0))
    add("Plate markings", Compound(children=mk), C_MARK, "painted", 7, "shell", ex("plate"))
    add("Plate nameplate", _prism(62.0, 10.0, 2.0, T + 0.3, 0.2, x=-95.0, y=-95.0), C_LABEL, "paper", 7, "shell",
        ex("plate"))

    # ---- 8 draw-wire depth sensor: housing, lid, window, drum, eyelet, wire
    rx, ry = P["reel_xy"]
    bx, by, bz = P["reel_box"]
    split = T + bz - 10.0
    hous = _prism(bx, by, 6.0, T, bz, x=rx, y=ry)
    hous = _fillet_try(hous, _top_edges(hous), [3.0, 2.0, 1.0])
    hous -= _prism(bx - 2 * REEL_WALL, by - 2 * REEL_WALL, 4.0, T + REEL_WALL, bz - 2 * REEL_WALL, x=rx, y=ry)
    hous -= _prism(bx + 2, by + 2, 7.0, split - 0.3, 0.6, x=rx, y=ry) - _prism(bx - 1.2, by - 1.2, 5.4, split - 1, 2, x=rx, y=ry)
    dr = P["drum_d"] / 2               # full 60 mm drum; the housing is sized round it (CNP-DDR-003)
    wz = T + REEL_WALL + 1.5 + dr      # drum axis height, drum clear of the housing floor
    win_cut = Pos(rx, ry - by / 2, wz) * Rot(90, 0, 0) * Cylinder(dr - 8.0, 10.0)
    lid = hous & Pos(rx, ry, split) * Box(bx + 4, by + 4, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
    base = hous & Pos(rx, ry, split) * Box(bx + 4, by + 4, 80, align=(Align.CENTER, Align.CENTER, Align.MAX))
    base -= win_cut
    base -= Pos(rx, ry - by / 2, wz) * Rot(90, 0, 0) * (Cylinder(dr - 5.0, 1.2) - Cylinder(dr - 8.0, 2))
    base += Pos(rx, ry - by / 2 + 0.2, wz) * Rot(90, 0, 0) * (Cylinder(dr - 3.5, 1.6) - Cylinder(dr - 6.5, 2))
    lid -= _cyl(1.8, 10, T + bz - 5, rx, ry)
    add("Draw-wire housing (IP65)", base, C_SHELL, "plastic", 8, "shell", ex("reel"))
    add("Draw-wire housing lid", lid, C_SHELL2, "plastic", 8, "shell", ex("reel", dz=60))
    heads = [_fillet_try(_cyl(2.6, 1.2, T + bz, rx + sx * (bx / 2 - 7), ry + sy * (by / 2 - 7)),
                         [], [0.3]) for sx in (-1, 1) for sy in (-1, 1)]
    add("Housing lid screws", Compound(children=heads), C_STAINLESS, "metal", 14, "shell", ex("reel", dz=60))
    win = Pos(rx, ry - by / 2 + 1.25, wz) * Rot(90, 0, 0) * Cylinder(dr - 6.5, 1.5)
    add("Draw-wire drum window", win, C_WINDOW, "clear", 8, "shell", ex("reel", dy=-60))
    drum = Pos(rx, ry, wz) * Rot(90, 0, 0) * Cylinder(dr - 2.0, 30.0)
    for s in (-1, 1):
        drum += Pos(rx, ry + s * 14.0, wz) * Rot(90, 0, 0) * Cylinder(dr, 2.0)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        drum -= Pos(rx + 12 * math.cos(a), ry, wz + 12 * math.sin(a)) * Rot(90, 0, 0) * Cylinder(4.5, 40)
    drum -= Pos(rx, ry, wz) * Rot(90, 0, 0) * Cylinder(3.0, 40)
    for k in range(-5, 6):
        drum -= Pos(rx, ry + 2.4 * k, wz) * Rot(90, 0, 0) * (Cylinder(dr, 0.8) - Cylinder(dr - 2.6, 1.0))
    add("Grooved aluminum drum", drum, C_CHROME, "metal", 8, "internal", ex("reel", dy=-130))
    eye = _ring(4.5, 1.6, 4.0, T + bz)
    eye = Pos(rx, ry, 0) * eye
    add("Wire exit eyelet", eye, C_STAINLESS, "metal", 8, "shell", ex("reel", dz=60))
    add("Draw wire (coated steel)", _rod((rx, ry, D["reel_top"]), (rx, ry, D["arm_under"] - 6.0), 1.2),
        "#9CA3AF", "metal", 8, "shell", ex("reel"))

    # ---- 9 clamp collar and wire arm: anodized, split with a clamp screw, eye and eye spring
    aw, ah = P["arm_section"]
    ang = math.degrees(math.atan2(ry, rx))
    ct = D["collar_top"]
    collar = _cyl(P["collar_d"] / 2, P["collar_h"], ct - P["collar_h"])
    collar = _fillet_try(collar, _top_edges(collar), [1.5, 1.0])
    collar = _fillet_try(collar, _bottom_edges(collar), [1.5, 1.0])
    collar -= _cyl(rr, P["collar_h"] + 2, ct - P["collar_h"] - 1)
    collar -= Rot(0, 0, ang + 180) * Pos(P["collar_d"] / 2, 0, ct - P["collar_h"] / 2) * Box(P["collar_d"], 1.6, P["collar_h"] + 2)
    collar += Rot(0, 0, ang + 180) * Pos(P["collar_d"] / 2 + 3.0, 0, ct - 11.0) * Box(10.0, 16.0, 14.0)
    collar -= Rot(0, 0, ang + 180) * Pos(P["collar_d"] / 2 + 3.0, 0, ct - 11.0) * Box(22.0, 1.6, 16.0)
    arm = (Pos(0, 0, D["arm_under"]) * Rot(0, 0, ang)
           * Pos(D["arm_len"] / 2 + 4, 0, 0) * Box(D["arm_len"] + 8, aw, ah, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    arm = _fillet_try(arm, arm.edges().filter_by(Axis.Z, reverse=True), [2.5, 1.5, 0.8])
    arm -= _cyl(rr + 0.5, 40, D["arm_under"] - 10)
    add("Clamp collar and wire arm (anodized)", collar + arm, C_ANOD, "metal", 9, "shell", ex("clamp"))
    cs = Rot(0, 0, ang + 180) * Pos(P["collar_d"] / 2 + 3.0, 0, ct - 11.0) * Rot(90, 0, 0) * Cylinder(3.2, 22.0)
    cs += Rot(0, 0, ang + 180) * Pos(P["collar_d"] / 2 + 3.0, 11.0 + 2.0, ct - 11.0) * Rot(90, 0, 0) * Cylinder(4.8, 4.0)
    add("Clamp screw", cs, C_BLACK, "metal", 14, "shell", ex("clamp"))
    wye = Pos(rx, ry, D["arm_under"] - 4.0) * Rot(90, 0, ang) * (Cylinder(5.0, 3.0) - Cylinder(2.2, 4.0))
    spring = [_ring(3.0, 2.0, 0.9, D["arm_under"] - 22.0 + 1.6 * k, rx, ry) for k in range(9)]
    add("Wire eye and preload spring", Compound(children=[wye] + spring), C_STAINLESS, "metal", 9, "shell", ex("clamp"))

    # ---- 10 sensor pad: isolator, potted body, stainless band clamp with worm housing
    pr, pt, ph = P["pad"]
    pad_top = D["z_anvil_top"] - P["pad_gap"]
    x_in = -ra
    iso = Pos(x_in - 2.0, 0, pad_top - ph) * Box(4.0, pt, ph, align=(Align.CENTER, Align.CENTER, Align.MIN))
    iso = _fillet_try(iso, iso.edges().filter_by(Axis.X), [1.5, 1.0])
    add("Pad elastomer isolator", iso, C_RUBBER, "rubber", 10, "shell", ex("pad"))
    pb = Pos(x_in - 4.0 - (pr - 4.0) / 2, 0, pad_top - ph) * Box(pr - 4.0, pt, ph, align=(Align.CENTER, Align.CENTER, Align.MIN))
    pb = _fillet_try(pb, pb.edges(), [3.0, 2.0, 1.0])
    add("Potted sensor pad", pb, "#3A3F47", "plastic", 10, "shell", ex("pad", dx=-50))
    stripe = Pos(x_in - pr - 0.05, 0, pad_top - 8.0) * Box(0.4, pt - 8.0, 3.0)
    add("Pad accent stripe", stripe, C_ACCENT, "painted", 10, "shell", ex("pad", dx=-50))
    bz0 = pad_top - ph + 4
    band = _ring(ra + P["band_t"], ra, P["band_h"], bz0)
    band += Pos(0, ra + 5.0, bz0 + P["band_h"] / 2) * Box(12.0, 8.0, P["band_h"] + 2)
    band += Pos(0, ra + 5.0, bz0 + P["band_h"] / 2) * Rot(0, 90, 0) * Cylinder(3.0, 18.0)
    add("Stainless band clamp", band, C_STAINLESS, "metal", 10, "shell", ex("pad"))

    # ---- 11 logger: IP65 box, lid with window over the cells, button, LED, gland, label
    lx, ly = P["logger_xy"]
    Lb, Wb, Hb = P["logger_box"]
    lsplit = T + Hb - 10.0
    box = _prism(Lb, Wb, 7.0, T, Hb, x=lx, y=ly)
    box = _fillet_try(box, _top_edges(box), [3.0, 2.0, 1.0])
    box -= _prism(Lb - 2 * LOG_WALL, Wb - 2 * LOG_WALL, 5.0, T + LOG_WALL, Hb - 2 * LOG_WALL, x=lx, y=ly)
    box -= _prism(Lb + 2, Wb + 2, 8.0, lsplit - 0.3, 0.6, x=lx, y=ly) - _prism(Lb - 1.2, Wb - 1.2, 6.4, lsplit - 1, 2, x=lx, y=ly)
    llid = box & Pos(lx, ly, lsplit) * Box(Lb + 4, Wb + 4, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lbase = box & Pos(lx, ly, lsplit) * Box(Lb + 4, Wb + 4, 80, align=(Align.CENTER, Align.CENTER, Align.MAX))
    wx, wy = lx - 20.0, ly
    llid -= _prism(46.0, 40.0, 3.0, T + Hb - 4.0, 6.0, x=wx, y=wy)
    llid -= _prism(52.0, 46.0, 4.0, T + Hb - 0.8, 2.0, x=wx, y=wy)
    gx, gy = lx + 20.0, ly            # cable entry, as model.py
    bxn, byn = lx + 36.0, ly - 20.0   # button
    ledx, ledy = lx + 36.0, ly + 20.0
    llid -= _cyl(6.2, 10, T + Hb - 5, bxn, byn)
    llid -= _cyl(2.0, 10, T + Hb - 5, ledx, ledy)
    llid -= _cyl(3.5, 10, T + Hb - 5, gx, gy)
    add("Logger box (IP65)", lbase, C_SHELL, "plastic", 11, "shell", ex("logger"))
    add("Logger lid", llid, C_SHELL2, "plastic", 11, "shell", ex("logger", dz=90))
    lheads = [_cyl(2.6, 1.2, T + Hb, lx + sx * (Lb / 2 - 7), ly + sy * (Wb / 2 - 7)) for sx in (-1, 1) for sy in (-1, 1)]
    add("Logger lid screws", Compound(children=lheads), C_STAINLESS, "metal", 11, "shell", ex("logger", dz=90))
    add("Logger cell window", _prism(51.0, 45.0, 3.5, T + Hb - 0.8, 0.8, x=wx, y=wy), C_WINDOW, "clear", 11,
        "shell", ex("logger", dz=120))
    btn = _cyl(5.6, 3.5, T + Hb - 2.0, bxn, byn)
    btn = _fillet_try(btn, _top_edges(btn), [1.5, 1.0, 0.5])
    btn += _ring(8.0, 6.2, 1.0, T + Hb, bxn, byn)
    add("Logger button", btn, C_ACCENT, "rubber", 11, "shell", ex("logger", dz=90))
    led = _cyl(1.9, 2.0, T + Hb - 1.4, ledx, ledy)
    led = _fillet_try(led, _top_edges(led), [0.8, 0.5])
    add("Status LED (lit)", led, C_LED, "emissive", 11, "shell", ex("logger", dz=90))
    gland = _cyl(7.0, 4.0, T + Hb, gx, gy)
    gland = _fillet_try(gland, _top_edges(gland), [1.0, 0.5])
    gland += _cyl(5.5, 6.0, T + Hb + 4.0, gx, gy)
    gland = _fillet_try(gland, _top_edges(gland), [1.5, 1.0, 0.5])
    add("Cable gland", gland, C_BLACK, "plastic", 12, "shell", ex("logger", dz=90))
    lab = Pos(lx, ly - Wb / 2 - 0.1, T + 18.0) * Box(58.0, 0.3, 14.0)
    add("Logger label", lab, C_LABEL, "paper", 11, "shell", ex("logger"))
    cells = []
    caps = []
    for k in (-1, 0, 1):
        cx = wx + 14.5 * k
        c = Pos(cx, wy, T + LOG_WALL + 8.0) * Rot(90, 0, 0) * Cylinder(7.25, 47.0)
        cells.append(_fillet_try(c, c.edges(), [0.8, 0.5]))
        caps.append(Pos(cx, wy - 24.2, T + LOG_WALL + 8.0) * Rot(90, 0, 0) * Cylinder(2.6, 1.6))
    add("AA cells (3)", Compound(children=cells), C_CELL, "painted", 11, "internal", ex("logger", dz=45))
    add("AA cell terminals", Compound(children=caps), C_STAINLESS, "metal", 11, "internal", ex("logger", dz=45))
    tray = _prism(46.0, 52.0, 3.0, T + LOG_WALL, 4.0, x=wx, y=wy)
    add("Cell holder", tray, C_BLACK, "plastic", 11, "internal", ex("logger", dz=45))

    # ---- 12 coiled cable: tight coil from the pad, stretched coil down to the logger gland
    c = P["cable_d"] / 2
    a = (x_in - pr / 2, 0, pad_top - ph)
    a2 = (a[0], a[1], a[2] - 16.0)
    mpt = (-(ra + 30), -40, D["z_anvil"] - 250)
    b = (gx, gy, T + Hb + 10.0)
    b2 = (b[0], b[1], b[2] + 20.0)
    boot = _rod(a, a2, c + 1.5)
    boot = _fillet_try(boot, boot.edges(), [1.0, 0.5])
    cable = [_coil(a2, mpt, 8.0, c, 9.0), _coil(mpt, b2, 6.0, c, 45.0), _rod(b2, b, c)]
    add("Coiled sensor cable", Compound(children=cable), C_BLACK, "rubber", 12, "shell", ex("cable"))
    add("Cable strain relief", boot, C_RUBBER, "rubber", 12, "shell", ex("pad", dx=-50))

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
