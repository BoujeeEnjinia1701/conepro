"""ConePro parametric model (build123d), TRL 3, constructable level of detail.

Run from the repo root:  python cad/src/model.py            exports STEP and STL and prints the checks
                         python cad/src/model.py --check    prints the constructability checks only
Exports STEP and STL into cad/step and cad/stl:
    conepro-assembly.step / .stl   whole instrument set up at the start of a test
    hammer-assembly.step / .stl    upper rod, 8 kg hammer, stop collar, T-handle and end cap, packed (heaviest piece)
    drive-train.step / .stl        cone, lower drive rod and anvil
    sensor-set.step / .stl         reference plate, draw-wire reel, clamp and arm, sensor pad, logger, cables

Axes: the rod axis is Z, with the ground at z = 0 and the cone point touching the ground.
The draw-wire reel sits on the plate on +X, the logger on -X, the plate slot opens toward -Y.
ASTM D6951 geometry (16 mm rod, 20 mm 60 degree cone, 8 kg hammer, 575 mm drop).

Revised 2026-09-30 under Amish's instruction to make the design physically buildable
(CNP-DDR-004, "Design for construction"). Every component is now a shape that can be turned,
drilled, sawn, printed or bought, and every joint has a fixing:
    M12 studs turned on the rod ends, screwed into tapped holes in the cone and anvil;
    cone shoulder 12 mm long so the tapped hole has wall round it;
    upper rod runs through the stop collar (6 mm roll pin) and the T-handle tube (welded);
    bubble level on a seat disc welded to the rod top;
    magnets in pockets outside the anvil strike area, 0.5 mm below the hammer face;
    clamp and wire arm cut in one piece from 12 mm aluminium plate, butting the anvil underside;
    sensor pad with a curved face on a curved isolator, held by the band round the anvil and pad;
    reel housing with walls, lid, posts, drum, shaft, spring motor and angle sensor; drum placed so
    the wire leaves it vertically under the exit eyelet; housing screwed to the plate from below;
    logger box with mounting flanges, two cable glands and a reel-to-logger cable in P-clips.
Revised 2026-10-02 to carry Amish's decisions of that day (CNP-DEC-001): spanner flats on the lower
rod, anvil and cone (no thread locker); a screw-on end cap for the upper rod's stud (end_cap());
grip grooves on the hammer, its length set to keep 8.00 kg; a "fit the end cap" label on the hammer;
33 mm rubber grips on the T-handle. The upper rod is turned by its T-handle, so it needs no flats.
The same PARAMS feed docs/04-calcs/sizing.py (CNP-CAL-001), the drawing CNP-DWG-001
(cad/src/sheets.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from collections import namedtuple
from pathlib import Path

STEEL, ALU = 7850e-9, 2700e-9   # kg/mm^3

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # ASTM D6951 mechanical geometry
    "rod_d": 16.0, "cone_d": 20.0, "cone_angle": 60.0,
    "cone_shoulder": 12.0,           # parallel part above the point; holds the tapped hole (DDR-004, P1)
    "stud_d": 12.0, "stud_cone": 12.0, "stud_anvil": 20.0,   # M12 studs turned on the rod ends
    "tap_cone": 14.0, "tap_anvil": 24.0,                       # tapped hole depths
    "lower_rod_L": 1000.0,
    "anvil_d": 64.0, "anvil_h": 60.0,
    "hammer_mass": 8.0,              # kg; hammer length is derived from it
    "hammer_od": 100.0, "hammer_id": 22.0,
    "groove_n": 3, "groove_w": 6.0, "groove_d": 2.0, "groove_pitch": 14.0,   # hammer grip grooves (decided 2026-10-02)
    "label": (25.0, 50.0, 0.2),      # hammer label: height, arc length, thickness ("fit the end cap", decided 2026-10-02)
    "n_mag": 16, "mag_d": 8.0, "mag_t": 4.0, "mag_r": 41.0, "mag_recess": 0.5,
    "drop": 575.0,                   # free drop, anvil top to hammer lower face at the stop
    "stop_d": 44.0, "stop_h": 18.0, "pin_d": 6.0,
    "handle_w": 260.0, "handle_tube": (26.0, 2.5), "handle_stem": 34.0,
    "grip": (33.0, 100.0, 3.0),      # rubber grips: OD, length over the closed end, end thickness (decided 2026-10-02)
    "end_cap": (32.0, 24.0, 21.0),   # upper rod stud end cap: OD, length, tapped depth (CNP-DDR-004, A1)
    # spanner flats (no thread locker, decided 2026-10-02): across flats, length
    "flats_rod": (13.0, 20.0), "flats_rod_z": 8.0,     # lower rod, 8 mm above its bottom shoulder
    "flats_anvil": (55.0, 17.0), "flats_anvil_z": 3.0,  # anvil, 3 mm above its bottom face
    "flats_cone": (17.0, 10.0),                         # cone shoulder, top 10 mm
    "seat": (30.0, 5.0), "level": (20.0, 6.0), "level_recess": 3.0,
    # sensor set (decisions D1, D3, D4, D6, D7 in CNP-DDR-001; plate and clamp lightened per CNP-DDR-002)
    "plate": 300.0, "plate_t": 6.0, "plate_hole": 60.0, "slot_w": 60.0,
    "reel_xy": (105.0, 40.0),        # wire exit point on the plate
    "reel_box": (72.0, 60.0, 72.0),  # housing x, y, z; sized round the 60 mm drum (CNP-DDR-003)
    "reel_wall": 3.0,
    "drum_d": 60.0, "drum_w": 20.0, "shaft_d": 6.0,
    "collar_d": 40.0, "collar_h": 12.0, "collar_gap": 0.0,   # one-piece clamp from 12 mm plate, against the anvil
    "arm_section": (16.0, 12.0),
    "pad": (22.0, 30.0, 30.0),       # isolator plus pad radial, tangential, height
    "isolator_t": 4.0,
    "pad_gap": 8.0,                  # pad top below the anvil top (hammer overhang clearance)
    "band_h": 12.0, "band_t": 2.0,   # band clamp round the anvil and over the pad (50 to 80 mm anvils)
    "logger_xy": (-95.0, 55.0), "logger_box": (100.0, 70.0, 42.0), "logger_wall": 2.5,
    "gland_y": (32.0, 58.0),         # logger glands on its +X wall: pad cable, reel cable
    "cable_d": 6.0, "reel_cable_d": 5.0, "wire_r": 0.6,   # wire drawn 1.2 mm so it shows
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    d = {}
    d["cone_h"] = (p["cone_d"] / 2) / math.tan(math.radians(p["cone_angle"] / 2))
    d["z_rod"] = d["cone_h"] + p["cone_shoulder"]
    d["z_anvil"] = d["z_rod"] + p["lower_rod_L"]
    d["z_anvil_top"] = d["z_anvil"] + p["anvil_h"]
    ring = math.pi / 4 * (p["hammer_od"] ** 2 - p["hammer_id"] ** 2)
    # magnet pockets remove steel; the magnets are counted at steel density, so add back the glue gaps
    rm = p["mag_d"] / 2
    void = p["n_mag"] * math.pi * ((rm + 0.1) ** 2 * (p["mag_t"] + p["mag_recess"] + 0.5) - rm ** 2 * p["mag_t"])
    ro = p["hammer_od"] / 2
    void += p["groove_n"] * math.pi * (ro ** 2 - (ro - p["groove_d"]) ** 2) * p["groove_w"]   # grip grooves
    d["hammer_L"] = (p["hammer_mass"] / STEEL + void) / ring
    d["upper_free"] = d["hammer_L"] + p["drop"]          # anvil top to stop underside
    d["z_stop"] = d["z_anvil_top"] + d["upper_free"]
    d["z_handle"] = d["z_stop"] + p["stop_h"] + p["handle_stem"]
    od = p["handle_tube"][0]
    d["z_rod_top"] = d["z_handle"] + od / 2             # upper rod ends flush with the top of the tube
    d["upper_L"] = d["z_rod_top"] - d["z_anvil_top"]    # rod length above the anvil (stud extra)
    d["height"] = d["z_rod_top"] + p["seat"][1] - p["level_recess"] + p["level"][1]
    d["drop_check"] = d["z_stop"] - d["z_anvil_top"] - d["hammer_L"]
    d["groove_z"] = [d["hammer_L"] / 2 + (k - (p["groove_n"] - 1) / 2) * p["groove_pitch"] for k in range(p["groove_n"])]
    d["label_z"] = d["hammer_L"] - 8.0 - p["label"][0] / 2   # label centre above the hammer's lower face
    d["collar_top"] = d["z_anvil"] - p["collar_gap"]
    d["arm_under"] = d["collar_top"] - p["arm_section"][1]
    d["reel_top"] = p["plate_t"] + p["reel_box"][2]
    d["drum_cx"] = p["reel_xy"][0] - p["drum_d"] / 2 - p["wire_r"] - 0.1   # wire leaves the drum vertically under the exit
    d["drum_cz"] = p["plate_t"] + p["reel_box"][2] / 2
    d["pad_top"] = d["z_anvil_top"] - p["pad_gap"]
    d["pad_bot"] = d["pad_top"] - p["pad"][2]
    # travel limits: the first contact as the rod goes down sets the penetration range
    d["limits"] = {
        "wire arm on reel housing": d["arm_under"] - d["reel_top"],
        "clamp collar on plate": d["collar_top"] - p["collar_h"] - p["plate_t"],
        "anvil on plate": d["z_anvil"] - p["plate_t"],
        "sensor pad on plate": d["pad_bot"] - p["plate_t"],
    }
    d["travel"] = min(d["limits"].values())
    d["travel_by"] = min(d["limits"], key=d["limits"].get)
    d["arm_len"] = math.hypot(*p["reel_xy"])
    d["arm_ang"] = math.degrees(math.atan2(p["reel_xy"][1], p["reel_xy"][0]))
    d["wire_start"] = d["arm_under"] - d["reel_top"]      # free wire length at zero depth
    return d


Comp = namedtuple("Comp", "name shape bom color")


def build_components(p=PARAMS):
    """Every made, bought and fixing part as a separate solid, set up at zero depth.
    Returns {key: Comp(name, shape, bom_no, color)}."""
    from build123d import (Align, Box, Cone, Cylinder, Face, Plane, Pos, Rot, Solid, Sphere, Vector,
                           Wire, extrude)

    D = derived(p)
    BASE = (Align.CENTER, Align.CENTER, Align.MIN)
    rr = p["rod_d"] / 2
    rs = p["stud_d"] / 2
    T = p["plate_t"]
    C = {}

    def cyl(r, h, z, x=0.0, y=0.0):
        return Pos(x, y, z) * Cylinder(r, h, align=BASE)

    def ycyl(r, L, x, y0, z):
        """Cylinder along +Y from y0, length L."""
        return Pos(x, y0, z) * Rot(-90, 0, 0) * Cylinder(r, L, align=BASE)

    def xcyl(r, L, x0, y, z):
        """Cylinder along +X from x0, length L."""
        return Pos(x0, y, z) * Rot(0, 90, 0) * Cylinder(r, L, align=BASE)

    def box(x0, x1, y0, y1, z0, z1):
        return Pos((x0 + x1) / 2, (y0 + y1) / 2, z0) * Box(x1 - x0, y1 - y0, z1 - z0, align=BASE)

    def tube3(a, b, r):
        a, b = Vector(*a), Vector(*b)
        v = b - a
        return Solid.make_cylinder(r, v.length, Plane(origin=a, z_dir=v.normalized()))

    def path(pts, r):
        s = None
        for a, b in zip(pts, pts[1:]):
            s = tube3(a, b, r) if s is None else s + tube3(a, b, r)
        for q in pts[1:-1]:
            s = s + Pos(*q) * Sphere(r)
        return s

    def add(key, name, shape, bom, color):
        C[key] = Comp(name, shape, bom, color)

    def flats(af, z0, L, r):
        """Two parallel spanner flats, af across, facing +X and -X, from z0 for L."""
        big = 2 * r + 4
        return (Pos(af / 2 + big / 2, 0, z0) * Box(big, big, L, align=BASE)
                + Pos(-af / 2 - big / 2, 0, z0) * Box(big, big, L, align=BASE))

    # ------------------------------------------------------------ drive train
    zr, za, zt = D["z_rod"], D["z_anvil"], D["z_anvil_top"]
    cone = Cone(0.4, p["cone_d"] / 2, D["cone_h"], align=BASE) + cyl(p["cone_d"] / 2, p["cone_shoulder"], D["cone_h"])
    cone -= cyl(rs, p["tap_cone"] + 1, zr - p["tap_cone"])
    fc, lc = p["flats_cone"]
    cone -= flats(fc, zr - lc, lc + 1, p["cone_d"] / 2)
    add("cone", "Hardened cone, 20 mm, 60 degree", cone, 1, "#B45309")
    rod = cyl(rr, p["lower_rod_L"], zr) + cyl(rs, p["stud_cone"], zr - p["stud_cone"]) + cyl(rs, p["stud_anvil"], za)
    rod -= flats(p["flats_rod"][0], zr + p["flats_rod_z"], p["flats_rod"][1], rr)
    add("lower_rod", "Lower drive rod, 16 mm x 1,000 mm", rod, 2, "#6B7280")
    anvil = cyl(p["anvil_d"] / 2, p["anvil_h"], za) - cyl(rs, p["tap_anvil"] + 1, za - 1) - cyl(rs, p["tap_anvil"] + 1, zt - p["tap_anvil"])
    anvil -= flats(p["flats_anvil"][0], za + p["flats_anvil_z"], p["flats_anvil"][1], p["anvil_d"] / 2)
    add("anvil", "Anvil and coupler", anvil, 3, "#374151")

    # ------------------------------------------------------------ hammer with its magnets
    hL = D["hammer_L"]
    hammer = cyl(p["hammer_od"] / 2, hL, zt) - cyl(p["hammer_id"] / 2, hL + 2, zt - 1)
    mags = None
    for k in range(p["n_mag"]):
        a = 2 * math.pi * k / p["n_mag"]
        x, y = p["mag_r"] * math.cos(a), p["mag_r"] * math.sin(a)
        hammer -= cyl(p["mag_d"] / 2 + 0.1, p["mag_t"] + p["mag_recess"] + 0.5, zt - 1 + 1, x, y)
        m = cyl(p["mag_d"] / 2, p["mag_t"], zt + p["mag_recess"], x, y)
        mags = m if mags is None else mags + m
    ro = p["hammer_od"] / 2
    for gz_ in D["groove_z"]:            # grip grooves, square, turned
        hammer -= cyl(ro + 1, p["groove_w"], zt + gz_ - p["groove_w"] / 2) - cyl(ro - p["groove_d"], p["groove_w"] + 2, zt + gz_ - p["groove_w"] / 2 - 1)
    add("hammer", "Drop hammer, 8 kg", hammer, 4, "#0F766E")
    lh, la, lt = p["label"]
    half = math.degrees(la / 2 / ro)
    sector = Pos(0, 0, zt + D["label_z"] - lh / 2) * Box(ro + 10, 2 * (ro + 10) * math.sin(math.radians(half)), lh,
                                                      align=(Align.MIN, Align.CENTER, Align.MIN))
    label = (cyl(ro + lt, lh, zt + D["label_z"] - lh / 2) - cyl(ro, lh + 2, zt + D["label_z"] - lh / 2 - 1)) & (Rot(0, 0, -90) * sector)
    add("label", "Hammer label, fit the end cap", label, 14, "#F4F4F2")
    add("magnets", "Magnets (16), bonded in pockets", mags, 4, "#B91C1C")

    # ------------------------------------------------------------ upper rod, stop collar, T-handle, level
    zs, zh, ztop = D["z_stop"], D["z_handle"], D["z_rod_top"]
    od, t = p["handle_tube"]
    pin_z = zs + p["stop_h"] / 2
    pin_hole = ycyl(p["pin_d"] / 2, p["stop_d"] + 4, 0, -p["stop_d"] / 2 - 2, pin_z)
    upper = cyl(rr, ztop - zt, zt) + cyl(rs, p["stud_anvil"], zt - p["stud_anvil"])
    upper -= pin_hole
    add("upper_rod", "Upper rod (hammer guide)", upper, 5, "#9CA3AF")
    stop = cyl(p["stop_d"] / 2, p["stop_h"], zs) - cyl(rr, p["stop_h"] + 2, zs - 1) - pin_hole
    add("stop", "Top stop collar", stop, 6, "#1F2937")
    pin_L = p["stop_d"] - 4
    add("pin", "Roll pin, 6 mm", ycyl(p["pin_d"] / 2, pin_L, 0, -pin_L / 2, pin_z), 14, "#111827")
    tube = Pos(0, 0, zh) * Rot(90, 0, 0) * (Cylinder(od / 2, p["handle_w"]) - Cylinder(od / 2 - t, p["handle_w"] + 2))
    tube -= cyl(rr, od + 4, zh - od / 2 - 2)
    add("tube", "T-handle tube", tube, 6, "#111827")
    gd, gL, ge = p["grip"]
    grips = None
    for sgn in (-1, 1):                 # closed-end rubber grips pushed over the tube ends
        y0 = p["handle_w"] / 2 + ge - gL
        g = ycyl(gd / 2, gL, 0, y0, zh) - ycyl(od / 2, gL - ge + 1, 0, y0 - 1, zh)
        grips_s = g if sgn > 0 else Rot(0, 0, 180) * g
        grips = grips_s if grips is None else grips + grips_s
    add("grips", "Rubber grips (2), 33 mm", grips, 6, "#2B2F36")
    sd, sh = p["seat"]
    seat = cyl(sd / 2, sh, ztop) - cyl(p["level"][0] / 2, p["level_recess"] + 1, ztop + sh - p["level_recess"])
    add("seat", "Level seat disc", seat, 6, "#374151")
    add("level", "Bullseye bubble level", cyl(p["level"][0] / 2, p["level"][1], ztop + sh - p["level_recess"]), 6, "#22C55E")

    # ------------------------------------------------------------ reference plate
    P_, rx, ry = p["plate"], *p["reel_xy"]
    bx, by, bz = p["reel_box"]
    w = p["reel_wall"]
    cx = D["drum_cx"]
    hx0, hx1, hy0, hy1 = cx - bx / 2, cx + bx / 2, ry - by / 2, ry + by / 2
    post = 8.0
    reel_screws = [(hx0 + w + post / 2, hy0 + 20), (hx0 + w + post / 2, hy1 - 10),
                   (hx1 - w - post / 2, hy0 + 20), (hx1 - w - post / 2, hy1 - 10)]
    lx, ly = p["logger_xy"]
    Lb, Wb, Hb = p["logger_box"]
    flange_screws = [(lx + s * 18, ly + q * (Wb / 2 + 6)) for s in (-1, 1) for q in (-1, 1)]
    yc = p["gland_y"][1]
    clip_xy = [(4.0, yc + 8.0), (-14.0, yc + 8.0)]
    plate = (Box(P_, P_, T, align=BASE) - cyl(p["plate_hole"] / 2, T + 2, -1)
             - Pos(0, -P_ / 4, -1) * Box(p["slot_w"], P_ / 2 + 2, T + 2, align=BASE))
    for (x, y) in reel_screws:      # countersunk from below
        plate -= cyl(2.0, T + 2, -1, x, y) + Pos(x, y, 0) * Cone(4.0, 2.0, 2.0, align=BASE)
    for (x, y) in flange_screws + clip_xy:   # tapped M4 (drawn at the screw size)
        plate -= cyl(2.0, T + 2, -1, x, y)
    add("plate", "Reference plate, slotted", plate, 7, "#94A3B8")

    # ------------------------------------------------------------ draw-wire reel
    body = box(hx0, hx1, hy0 + w, hy1, T, T + bz) - box(hx0 + w, hx1 - w, hy0 - 1, hy1 - w, T + w, T + bz - w)
    zlo, zhi = T + w, T + bz - w
    for xa in (hx0 + w, hx1 - w - post):
        body += box(xa, xa + post, hy0 + w, hy1 - w, zlo, zlo + post)               # bottom posts, full depth
        body += box(xa, xa + post, hy0 + w, hy0 + w + 10, zhi - post, zhi)          # top posts at the lid
    bz_c = D["drum_cz"]
    body += ycyl(9.0, 15.0, cx, hy1 - w - 15.0, bz_c)                                # bearing boss on the back wall
    body -= ycyl(p["shaft_d"] / 2, 15.5, cx, hy1 - w - 15.0 - 0.5, bz_c)
    body -= cyl(2.6, w + 2, T + bz - w - 1, rx, ry)                                   # eyelet hole
    gz = T + 22.0
    body -= xcyl(6.0, w + 2, hx0 - 1, yc, gz)                                         # gland hole, -X wall
    for (x, y) in reel_screws:
        body -= cyl(2.0, 9.0, T - 0.1, x, y)                                           # heat-set inserts from below
    add("reel_body", "Reel housing body, printed", body, 8, "#2563EB")
    lid = box(hx0, hx1, hy0, hy0 + w, T, T + bz)   # the -Y face of the housing
    lid += ycyl(8.0, 1.0, cx, hy0 + w, bz_c + 18.0)                                  # stand-off pad for the sensor board
    lid_xz = [(xa + post / 2, za_) for xa in (hx0 + w, hx1 - w - post) for za_ in (zlo + post / 2, zhi - post / 2)]
    ls = None
    for (x, z) in lid_xz:
        lid -= ycyl(1.6, w + 2, x, hy0 - 1, z)
        body -= ycyl(1.6, 8.0, x, hy0 + w - 0.01, z)                                  # M3 inserts in the post ends
        s_ = ycyl(1.6, w + 8.0, x, hy0, z) + ycyl(2.75, 2.0, x, hy0 - 2.0, z)
        ls = s_ if ls is None else ls + s_
    add("reel_lid", "Reel housing lid, printed", lid, 8, "#60A5FA")
    add("lid_screws", "M3 lid screws (4)", ls, 14, "#111827")
    add("reel_body", "Reel housing body, printed", body, 8, "#2563EB")
    dr = p["drum_d"] / 2
    y_d0 = ry - p["drum_w"] / 2
    drum = ycyl(dr, p["drum_w"], cx, y_d0, bz_c) - ycyl(p["shaft_d"] / 2, p["drum_w"] + 2, cx, y_d0 - 1, bz_c)
    for k in range(6):   # wire grooves, 1 mm pitch, single layer
        drum -= Pos(cx, ry - 3 + k, bz_c) * Rot(-90, 0, 0) * (Cylinder(dr + 1, 0.6) - Cylinder(dr - 0.5, 0.8))
    add("drum", "Grooved drum, aluminium", drum, 8, "#CBD5E1")
    sy0 = hy0 + w + 6.0
    shaft = ycyl(p["shaft_d"] / 2, hy1 - w - sy0, cx, sy0, bz_c)
    add("shaft", "Drum shaft, 6 mm", shaft, 8, "#6B7280")
    motor = ycyl(20.0, 8.0, cx, y_d0 - 10.0, bz_c) - ycyl(p["shaft_d"] / 2, 10.0, cx, y_d0 - 11.0, bz_c)
    add("motor", "Constant-force spring motor", motor, 8, "#F59E0B")
    add("magnet", "Shaft magnet", ycyl(3.0, 2.0, cx, sy0 - 2.0, bz_c), 8, "#B91C1C")
    board = box(cx - 15, cx + 15, hy0 + w + 1.0, hy0 + w + 2.6, bz_c - 15, bz_c + 15)
    add("board", "Angle sensor board", board, 8, "#16A34A")
    eyelet = cyl(4.0, 1.0, T + bz, rx, ry) + cyl(2.5, w, T + bz - w, rx, ry)
    eyelet -= cyl(1.6, w + 3, T + bz - w - 1, rx, ry)
    add("eyelet", "Wire exit eyelet", eyelet, 8, "#D4A017")
    for i, (x, y) in enumerate(reel_screws):
        s = Pos(x, y, 0) * Cone(4.0, 2.0, 2.0, align=BASE) + cyl(2.0, T + 8.0 - 2.0, 2.0, x, y)
        C.setdefault("reel_screws", Comp("M4 countersunk screws (4)", None, 14, "#111827"))
        C["reel_screws"] = C["reel_screws"]._replace(shape=s if C["reel_screws"].shape is None else C["reel_screws"].shape + s)

    # ------------------------------------------------------------ clamp collar and wire arm, one piece
    aw, ah = p["arm_section"]
    ang = D["arm_ang"]
    ct = D["collar_top"]
    zb = ct - p["collar_h"]
    L_arm = D["arm_len"] + 10.0
    clamp = cyl(p["collar_d"] / 2, p["collar_h"], zb) + Pos(0, 0, zb) * Rot(0, 0, ang) * Pos(L_arm / 2, 0, 0) * Box(L_arm, aw, ah, align=BASE)
    clamp -= cyl(rr, p["collar_h"] + 2, zb - 1)
    back = Rot(0, 0, ang + 180)
    clamp -= back * Pos(rr + 7, 0, zb - 1) * Box(16.0, 1.5, p["collar_h"] + 2, align=BASE)     # saw slit
    clamp -= back * Pos(14.0, -15, zb + p["collar_h"] / 2) * Rot(-90, 0, 0) * Cylinder(2.75, 30, align=BASE)   # M5 cross hole
    clamp -= cyl(1.6, ah + 2, zb - 1, rx, ry)                                                   # wire eye hole
    clamp -= back * Pos(14.0, -20.0, zb + p["collar_h"] / 2) * Rot(-90, 0, 0) * Cylinder(4.5, 7.0, align=BASE)   # spot face for the head
    add("clamp", "Clamp collar and wire arm, aluminium", clamp, 9, "#D4A017")
    scr = back * Pos(14.0, -13.0, zb + p["collar_h"] / 2) * Rot(-90, 0, 0) * Cylinder(2.5, 24.0, align=BASE)
    scr += back * Pos(14.0, -18.0, zb + p["collar_h"] / 2) * Rot(-90, 0, 0) * Cylinder(4.25, 5.0, align=BASE)
    add("clamp_screw", "M5 clamp screw", scr, 14, "#111827")
    spring = cyl(4.0, 15.0, ct, rx, ry) - cyl(1.8, 17.0, ct - 1, rx, ry)
    add("eye_spring", "Preload eye spring", spring, 8, "#F59E0B")
    add("crimp", "Wire end stop", cyl(2.5, 5.0, ct + 15.0, rx, ry) - cyl(p["wire_r"], 7.0, ct + 14.0, rx, ry), 8, "#D4A017")
    wire = cyl(p["wire_r"], ct + 15.0 + 5.0 - bz_c, bz_c, rx, ry)
    add("wire", "Draw wire, 0.45 mm coated steel", wire, 8, "#1D4ED8")

    # ------------------------------------------------------------ sensor pad, isolator and band
    ra = p["anvil_d"] / 2
    pr, pt, ph = p["pad"]
    ti = p["isolator_t"]
    pb, ptop = D["pad_bot"], D["pad_top"]
    sector = box(-ra - pr - 5, 0, -pt / 2, pt / 2, pb, ptop)
    iso = (cyl(ra + ti, ph, pb) - cyl(ra, ph + 2, pb - 1)) & box(-ra - ti - 1, -10, -pt / 2, pt / 2, pb, ptop)
    add("isolator", "Elastomer isolator, 4 mm", iso, 10, "#111827")
    pad = box(-ra - pr, -ra + 2, -pt / 2, pt / 2, pb, ptop) - cyl(ra + ti, ph + 2, pb - 1)
    pad = pad & sector
    pad += cyl(4.0, 8.0, pb - 8.0, -ra - ti - (pr - ti) / 2, 0)                       # strain relief at the cable exit
    pad -= cyl(p["cable_d"] / 2, 9.0, pb - 8.5, -ra - ti - (pr - ti) / 2, 0)
    add("pad", "Blow and tilt sensor pad", pad, 10, "#7C3AED")

    def hull(pts):
        pts = sorted(set(pts))
        lo, up = [], []
        cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])  # noqa: E731
        for q in pts:
            while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
                lo.pop()
            lo.append(q)
        for q in reversed(pts):
            while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0:
                up.pop()
            up.append(q)
        return lo[:-1] + up[:-1]

    def prism(r, ex, h, z):
        r = r / math.cos(math.pi / 96)          # polygon round the circle, not inside it
        ptsc = [(round(r * math.cos(2 * math.pi * k / 96), 4), round(r * math.sin(2 * math.pi * k / 96), 4)) for k in range(96)]
        ptsc += [(-ra - pr - ex, pt / 2 + ex), (-ra - pr - ex, -pt / 2 - ex)]
        hp = hull(ptsc)
        f = Face(Wire.make_polygon([Vector(x, y, z) for x, y in hp], close=True))
        return extrude(f, amount=h)
    bzb = pb + (ph - p["band_h"]) / 2
    band = prism(ra + p["band_t"], p["band_t"], p["band_h"], bzb) - prism(ra, 0.0, p["band_h"] + 2, bzb - 1)
    band += box(-6, 6, ra + p["band_t"], ra + p["band_t"] + 8, bzb - 1, bzb + p["band_h"] + 1)     # worm housing
    add("band", "Stainless band clamp", band, 10, "#9CA3AF")

    # ------------------------------------------------------------ logger with flanges, glands and internals
    wl = p["logger_wall"]
    lx0, lx1, ly0, ly1 = lx - Lb / 2, lx + Lb / 2, ly - Wb / 2, ly + Wb / 2
    lbody = box(lx0, lx1, ly0, ly1, T, T + Hb - 4) - box(lx0 + wl, lx1 - wl, ly0 + wl, ly1 - wl, T + wl, T + Hb)
    for q in (-1, 1):
        y0 = ly1 if q > 0 else ly0 - 12
        lbody += box(lx - 30, lx + 30, y0, y0 + 12, T, T + 4)
    for (x, y) in flange_screws:
        lbody -= cyl(2.2, 6, T - 1, x, y)
    for y in p["gland_y"]:
        lbody -= xcyl(6.0, wl + 2, lx1 - wl - 1, y, T + 21.0)
    add("logger", "Logger box, IP65, flanged", lbody, 11, "#16A34A")
    add("logger_lid", "Logger lid", box(lx0, lx1, ly0, ly1, T + Hb - 4, T + Hb), 11, "#4ADE80")
    add("cells", "Cell holder, 3 x AA", box(lx0 + 5, lx0 + 65, ly0 + 10, ly0 + 55, T + wl, T + wl + 16), 11, "#C2410C")
    add("module", "BLE logger board", box(lx1 - 31, lx1 - 9, ly0 + 18, ly0 + 52, T + wl, T + wl + 8), 11, "#0F766E")
    fs = None
    for (x, y) in flange_screws:
        s = cyl(2.0, 4.0 + T - 1.0, 1.0, x, y) + cyl(3.8, 2.6, T + 4, x, y)
        fs = s if fs is None else fs + s
    add("flange_screws", "M4 pan-head screws (4)", fs, 14, "#111827")
    gl = None
    for y, rb in zip(p["gland_y"], (p["cable_d"] / 2, p["reel_cable_d"] / 2)):
        g = xcyl(7.5, 12.0, lx1, y, T + 21.0) + xcyl(6.0, wl, lx1 - wl, y, T + 21.0) + xcyl(9.0, 3.0, lx1 - wl - 3.0, y, T + 21.0)
        g -= xcyl(rb, 30.0, lx1 - 10, y, T + 21.0)
        gl = g if gl is None else gl + g
    g = xcyl(7.5, 10.0, hx0 - 10.0, yc, gz) + xcyl(6.0, w, hx0, yc, gz) + xcyl(9.0, 3.0, hx0 + w, yc, gz)
    g -= xcyl(p["reel_cable_d"] / 2, 30.0, hx0 - 15, yc, gz)
    gl = gl + g
    add("glands", "Cable glands, M12 (3)", gl, 11, "#1F2937")

    # ------------------------------------------------------------ cables
    rc = p["reel_cable_d"] / 2
    zc = T + rc
    reel_cable = path([(hx0 + 2, yc, gz), (hx0 - 16, yc, gz), (hx0 - 22, yc, zc), (lx1 + 22, yc, zc),
                       (lx1 + 16, yc, T + 21.0), (lx1 - 6, yc, T + 21.0)], rc)
    add("reel_cable", "Reel-to-logger cable", reel_cable, 17, "#334155")
    pc = None
    for (x, y) in clip_xy:
        c_ = (xcyl(rc + 1.2, 8, x - 4, yc, zc) - xcyl(rc, 10, x - 5, yc, zc)) & box(x - 5, x + 5, yc - 10, yc + 10, T, zc + 10)
        c_ += box(x - 4, x + 4, yc + rc, yc + 12, T, T + 1.2)
        c_ -= cyl(2.1, 4, T - 1, x, y)
        pc = c_ if pc is None else pc + c_
    add("pclips", "P-clips (2) and M4 screws", pc, 14, "#475569")
    c = p["cable_d"] / 2
    a0 = (-ra - ti - (pr - ti) / 2, 0, pb)
    a = (a0[0], 0, pb - 14.0)
    m = (-(ra + 38), -40, D["z_anvil"] - 250)
    b_ = (lx1 + 16, p["gland_y"][0], T + 21.0)
    e_ = (lx1 - 6, p["gland_y"][0], T + 21.0)
    add("cable", "Coiled sensor cable", path([a0, a, m, b_, e_], c), 12, "#1F2937")
    return C


# Which components make up each numbered part of the concept (BOM numbering); sizing.py,
# concept_media.py and sheets.py use these fused parts.
PART_GROUPS = {
    "cone": ("Hardened cone, 20 mm, 60 degree", ["cone"], 1, "#B45309"),
    "lower_rod": ("Lower drive rod, 16 mm x 1,000 mm", ["lower_rod"], 2, "#6B7280"),
    "anvil": ("Anvil and coupler", ["anvil"], 3, "#374151"),
    "hammer": ("Drop hammer, 8 kg", ["hammer", "magnets", "label"], 4, "#0F766E"),
    "upper_rod": ("Upper rod (hammer guide)", ["upper_rod"], 5, "#9CA3AF"),
    "handle": ("Handle, top stop, grips, bubble level", ["stop", "pin", "tube", "grips", "seat", "level"], 6, "#111827"),
    "plate": ("Reference plate, slotted", ["plate"], 7, "#94A3B8"),
    "drawwire": ("Draw-wire depth sensor", ["reel_body", "reel_lid", "drum", "shaft", "motor", "magnet", "board",
                                             "eyelet", "wire", "eye_spring", "crimp", "reel_screws", "lid_screws"], 8, "#2563EB"),
    "clamp": ("Anvil clamp and wire arm, aluminum", ["clamp", "clamp_screw"], 9, "#D4A017"),
    "pad": ("Blow and tilt sensor pad", ["pad", "isolator", "band"], 10, "#7C3AED"),
    "logger": ("BLE logger, 3 x AA", ["logger", "logger_lid", "cells", "module", "glands", "flange_screws"], 11, "#16A34A"),
    "cable": ("Coiled sensor cable", ["cable"], 12, "#1F2937"),
    "reel_cable": ("Reel-to-logger cable", ["reel_cable", "pclips"], 17, "#334155"),
}


def end_cap(p=PARAMS):
    """Screw-on end cap on the upper rod's M12 stud, fitted whenever the rod is off the anvil (CNP-DDR-004, A1).
    Drawn in place on the stud: its top face seats on the rod shoulder, where the anvil top would be, so the
    hammer rests on it exactly as it rests on the anvil."""
    from build123d import Align, Cylinder, Pos
    D = derived(p)
    BASE = (Align.CENTER, Align.CENTER, Align.MIN)
    cd, cL, ch = p["end_cap"]
    zt = D["z_anvil_top"]
    cap = Pos(0, 0, zt - cL) * Cylinder(cd / 2, cL, align=BASE) - Pos(0, 0, zt - ch) * Cylinder(p["stud_d"] / 2, ch + 1, align=BASE)
    for k in range(24):                  # knurl-like flutes for a finger grip
        import math as _m
        a = 2 * _m.pi * k / 24
        cap -= Pos(cd / 2 * _m.cos(a), cd / 2 * _m.sin(a), zt - cL + 3) * Cylinder(0.8, cL - 6, align=BASE)
    return cap


def _fuse(shapes):
    from build123d import Compound
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def build_parts(p=PARAMS, comps=None):
    """Return {key: (name, shape, bom_no, color)} for the instrument set up at zero depth."""
    C = comps or build_components(p)
    return {k: (n, _fuse([C[c].shape for c in keys]), b, col) for k, (n, keys, b, col) in PART_GROUPS.items()}


# ---------------------------------------------------------------- constructability checks
def _overlap(a, b):
    try:
        bb1, bb2 = a.bounding_box(), b.bounding_box()
        if (bb1.min.X > bb2.max.X or bb2.min.X > bb1.max.X or bb1.min.Y > bb2.max.Y or bb2.min.Y > bb1.max.Y
                or bb1.min.Z > bb2.max.Z or bb2.min.Z > bb1.max.Z):
            return 0.0
        r = a & b
        return 0.0 if r is None else r.volume
    except Exception:
        try:
            return sum((x & y).volume for x in a.solids() for y in b.solids())
        except Exception:
            return float("nan")


def checks(p=PARAMS, C=None):
    """(description, overlap mm3, gap mm, expectation, ok) for every joint and clearance that matters."""
    C = C or build_components(p)
    D = derived(p)
    rows = []

    def chk(desc, ka, kb, expect):
        a, b = C[ka].shape, C[kb].shape
        v = _overlap(a, b)
        g = a.distance_to(b)
        if expect == "touch":
            ok = v < 1.0 and g < 0.05
        elif isinstance(expect, tuple):
            ok = v < 1.0 and expect[0] - 1e-6 <= g <= expect[1] + 1e-6
        else:
            ok = v < 1.0 and g >= expect - 1e-6
        rows.append((desc, v, g, expect, ok))

    T = [("cone on the lower rod stud", "cone", "lower_rod"),
         ("lower rod stud in the anvil", "lower_rod", "anvil"),
         ("upper rod stud in the anvil", "upper_rod", "anvil"),
         ("hammer resting on the anvil", "hammer", "anvil"),
         ("stop collar on the upper rod", "stop", "upper_rod"),
         ("roll pin in the stop collar", "pin", "stop"),
         ("roll pin through the upper rod", "pin", "upper_rod"),
         ("T-handle tube on the upper rod (weld)", "tube", "upper_rod"),
         ("level seat on the rod top (weld)", "seat", "upper_rod"),
         ("level in its seat", "level", "seat"),
         ("clamp collar on the lower rod", "clamp", "lower_rod"),
         ("clamp collar against the anvil underside", "clamp", "anvil"),
         ("clamp screw in the clamp", "clamp_screw", "clamp"),
         ("isolator on the anvil", "isolator", "anvil"),
         ("sensor pad on the isolator", "pad", "isolator"),
         ("band over the pad", "band", "pad"),
         ("band round the anvil", "band", "anvil"),
         ("reel housing on the plate", "reel_body", "plate"),
         ("reel lid on the housing", "reel_lid", "reel_body"),
         ("lid screws in the lid", "lid_screws", "reel_lid"),
         ("lid screws in the post inserts", "lid_screws", "reel_body"),
         ("drum shaft in the bearing boss", "shaft", "reel_body"),
         ("drum on the shaft", "drum", "shaft"),
         ("spring motor on the shaft", "motor", "shaft"),
         ("shaft magnet on the shaft end", "magnet", "shaft"),
         ("eyelet in the housing top", "eyelet", "reel_body"),
         ("reel screws in the plate", "reel_screws", "plate"),
         ("reel screws in the housing inserts", "reel_screws", "reel_body"),
         ("eye spring on the arm", "eye_spring", "clamp"),
         ("wire end stop on the spring", "crimp", "eye_spring"),
         ("logger on the plate", "logger", "plate"),
         ("logger lid on the box", "logger_lid", "logger"),
         ("logger flange screws in the plate", "flange_screws", "plate"),
         ("glands in the logger and reel walls", "glands", "logger"),
         ("reel cable lying on the plate", "reel_cable", "plate"),
         ("P-clips on the plate", "pclips", "plate"),
         ("P-clips over the reel cable", "pclips", "reel_cable"),
         ("cell holder on the logger floor", "cells", "logger"),
         ("logger board on the logger floor", "module", "logger"),
         ("sensor board on the lid stand-off", "board", "reel_lid")]
    for d, a, b in T:
        chk(d, a, b, "touch")
    chk("magnets in the hammer pockets (glue gap)", "magnets", "hammer", (0.0, 0.6))
    chk("wire tangent to the drum groove", "wire", "drum", (0.0, 0.5))
    chk("hammer bore clear of the upper rod", "hammer", "upper_rod", 2.5)
    chk("hammer clear of the stop collar (free drop)", "hammer", "stop", p["drop"] - 1)
    chk("sensor pad below the hammer face", "pad", "hammer", p["pad_gap"] - 0.1)
    chk("magnets above the sensor pad at impact", "magnets", "pad", p["pad_gap"])
    chk("drum clear of the housing", "drum", "reel_body", 2.0)
    chk("drum clear of the lid", "drum", "reel_lid", 2.0)
    chk("spring motor clear of the drum", "motor", "drum", 1.0)
    chk("spring motor clear of the housing", "motor", "reel_body", 1.0)
    chk("sensor board clear of the shaft magnet", "board", "magnet", (0.5, 3.0))
    chk("wire clear of the eyelet bore", "wire", "eyelet", 0.2)
    chk("wire clear of the housing wall", "wire", "reel_body", 0.2)
    chk("wire clear of the arm eye hole", "wire", "clamp", 0.2)
    chk("wire arm above the reel at zero depth (stroke)", "clamp", "reel_body", D["travel"] - 1)
    chk("sensor cable clear of the lower rod", "cable", "lower_rod", 10.0)
    chk("sensor cable clear of the plate", "cable", "plate", 5.0)
    chk("sensor cable in its logger gland", "cable", "glands", (0.0, 0.05))
    chk("reel cable clear of the plate hole edge (rod)", "reel_cable", "lower_rod", 20.0)
    chk("band clear of the hammer", "band", "hammer", 5.0)
    chk("clamp clear of the sensor pad", "clamp", "pad", 5.0)
    chk("logger clear of the plate hole and rod", "logger", "lower_rod", 20.0)
    chk("reel housing clear of the rod", "reel_body", "lower_rod", 20.0)
    # every pair not meant to touch must not overlap
    allowed = {frozenset((a, b)) for _, a, b in T}
    allowed |= {frozenset(x) for x in [("wire", "eyelet"), ("cable", "glands"), ("reel_cable", "glands"),
                                       ("pin", "upper_rod"), ("flange_screws", "logger"), ("pclips", "reel_cable")]}
    keys = list(C)
    bad = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            v = _overlap(C[a].shape, C[b].shape)
            if v > 1.0:
                bad.append((a, b, v))
    rows.append(("no two parts overlap (all pairs)", sum(x[2] for x in bad), 0.0, "none",
                 not bad))
    # spanner flats: wall left at the flats, and the flats clear of the parts round them
    fc = p["flats_cone"][0] / 2 - 10.2 / 2           # cone: flat to the M12 tapping drill
    rows.append(("cone wall at the spanner flats, mm", 0.0, fc, ">= 3", fc >= 3.0))
    fa = D["pad_bot"] - (D["z_anvil"] + p["flats_anvil_z"] + p["flats_anvil"][1])
    rows.append(("anvil flats below the pad and band, mm", 0.0, fa, ">= 1", fa >= 1.0))
    fr = (D["z_anvil"] - p["collar_h"]) - (D["z_rod"] + p["flats_rod_z"] + p["flats_rod"][1])
    rows.append(("lower rod flats below the clamp collar, mm", 0.0, fr, ">= 100", fr >= 100.0))
    chk("rubber grips on the tube ends", "grips", "tube", "touch")
    chk("rubber grips clear of the stop collar", "grips", "stop", 10.0)
    chk("hammer label on the hammer", "label", "hammer", "touch")
    # end cap, packed state (upper rod off the anvil)
    cap = end_cap(p)
    for desc, k, exp in (("end cap on the upper rod stud (packed)", "upper_rod", "touch"),
                         ("hammer resting on the end cap (packed)", "hammer", "touch")):
        v, g = _overlap(cap, C[k].shape), cap.distance_to(C[k].shape)
        rows.append((desc, v, g, exp, v < 1.0 and g < 0.05))
    ret = p["end_cap"][0] - p["hammer_id"]
    rows.append(("end cap wider than the hammer bore, mm", 0.0, ret, ">= 8", ret >= 8.0))
    return rows, bad


def print_checks():
    rows, bad = checks()
    nfail = 0
    for d, v, g, e, ok in rows:
        nfail += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {d:<52} overlap {v:8.2f} mm3  gap {g:7.2f} mm  expect {e}")
    for a, b, v in bad:
        print(f"       overlap {a} / {b}: {v:.1f} mm3")
    print(f"{len(rows)} checks, {nfail} failed")
    return nfail


GROUPS = {
    "conepro-assembly": None,
    "hammer-assembly": ["hammer", "upper_rod", "handle", "end_cap"],
    "drive-train": ["cone", "lower_rod", "anvil"],
    "sensor-set": ["plate", "drawwire", "clamp", "pad", "logger", "cable", "reel_cable"],
}


def export(parts=None):
    from build123d import Compound, export_step, export_stl
    parts = dict(parts or build_parts())
    parts["end_cap"] = ("End cap (packed state)", end_cap(), 14, "#475569")
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    for name, keys in GROUPS.items():
        shapes = [parts[k][1] for k in (keys or [k for k in parts if k != "end_cap"])]
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.2)
    return list(GROUPS)


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound
    parts = build_parts()
    names = export(parts)
    D = derived()
    bb = Compound(children=[v[1] for v in parts.values()]).bounding_box()
    print(f"assembly bounding box: X {bb.min.X:.0f} to {bb.max.X:.0f}, Y {bb.min.Y:.0f} to {bb.max.Y:.0f}, "
          f"Z {bb.min.Z:.0f} to {bb.max.Z:.0f} mm")
    print(f"height {D['height']:.0f} mm; hammer length {D['hammer_L']:.1f} mm; drop check {D['drop_check']:.1f} mm")
    print(f"penetration range {D['travel']:.0f} mm, limited by {D['travel_by']}")
    for k, (n, s, b, _) in parts.items():
        print(f"  {b:>2} {n:<36} volume {s.volume / 1000:9.1f} cm3")
    print("exported:", ", ".join(names))
    print_checks()
