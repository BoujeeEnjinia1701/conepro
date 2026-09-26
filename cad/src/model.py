"""ConePro parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    conepro-assembly.step / .stl   whole instrument set up at the start of a test
    hammer-assembly.step / .stl    upper rod, 8 kg hammer, stop collar and T-handle (heaviest piece)
    drive-train.step / .stl        cone, lower drive rod and anvil
    sensor-set.step / .stl         reference plate, draw-wire reel, clamp and arm, sensor pad, logger, cable

Axes: the rod axis is Z, with the ground at z = 0 and the cone point touching the ground.
The draw-wire reel sits on the plate on +X, the logger on -X. Main dimensions and
interfaces only: ASTM D6951 geometry (16 mm rod, 20 mm 60 degree cone, 8 kg hammer,
575 mm drop), rod threads, plate hole and slot, clamp and wire eye, sensor pad gap under
the hammer. Not fabrication detail; not for fabrication. The same PARAMS feed
docs/04-calcs/sizing.py (CNP-CAL-001) and the drawing CNP-DWG-001 (cad/src/sheets.py).
"""
import math
from pathlib import Path

STEEL, ALU = 7850e-9, 2700e-9   # kg/mm^3

# Top-level parameters (mm unless stated). Edit these, not the geometry below.
PARAMS = {
    # ASTM D6951 mechanical geometry
    "rod_d": 16.0, "cone_d": 20.0, "cone_angle": 60.0, "cone_shoulder": 5.0,
    "lower_rod_L": 1000.0,
    "anvil_d": 64.0, "anvil_h": 60.0,
    "hammer_mass": 8.0,              # kg; hammer length is derived from it
    "hammer_od": 100.0, "hammer_id": 22.0,
    "drop": 575.0,                   # free drop, anvil top to hammer lower face at the stop
    "stop_d": 44.0, "stop_h": 18.0,  # top stop collar under the handle
    "handle_w": 260.0, "handle_tube": (26.0, 2.5), "handle_stem": 34.0,
    # sensor set (decisions D1, D3, D4, D6, D7 in CNP-DDR-001; plate and clamp lightened per CNP-DDR-002)
    "plate": 300.0, "plate_t": 6.0, "plate_hole": 60.0, "slot_w": 60.0,   # 6 mm plate (DDR-002, R10)
    "reel_xy": (105.0, 40.0),        # wire exit point on the plate
    "reel_box": (60.0, 56.0, 60.0),  # housing x, y, z
    "drum_d": 60.0,                  # grooved aluminum drum, single layer
    "collar_d": 40.0, "collar_h": 22.0, "collar_gap": 4.0,   # aluminum clamp collar below the anvil (DDR-002)
    "arm_section": (16.0, 12.0),
    "pad": (22.0, 30.0, 30.0),       # sensor pad radial, tangential, height
    "pad_gap": 8.0,                  # pad top below the anvil top (hammer overhang clearance)
    "band_h": 12.0, "band_t": 2.0,   # band clamp that holds the pad to any 50 to 80 mm anvil
    "logger_xy": (-95.0, 55.0), "logger_box": (100.0, 70.0, 42.0),
    "cable_d": 6.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    d = {}
    d["cone_h"] = (p["cone_d"] / 2) / math.tan(math.radians(p["cone_angle"] / 2))
    d["z_rod"] = d["cone_h"] + p["cone_shoulder"]
    d["z_anvil"] = d["z_rod"] + p["lower_rod_L"]
    d["z_anvil_top"] = d["z_anvil"] + p["anvil_h"]
    ring = math.pi / 4 * (p["hammer_od"] ** 2 - p["hammer_id"] ** 2)
    d["hammer_L"] = p["hammer_mass"] / (STEEL * ring)
    d["upper_free"] = d["hammer_L"] + p["drop"]          # anvil top to stop underside
    d["z_stop"] = d["z_anvil_top"] + d["upper_free"]
    d["upper_L"] = d["upper_free"] + p["stop_h"]           # rod runs through the stop collar
    d["z_handle"] = d["z_stop"] + p["stop_h"] + p["handle_stem"]
    d["height"] = d["z_handle"] + p["handle_tube"][0] / 2 + 8.0   # top of the bubble level
    d["drop_check"] = d["z_stop"] - d["z_anvil_top"] - d["hammer_L"]
    d["collar_top"] = d["z_anvil"] - p["collar_gap"]
    d["arm_under"] = d["collar_top"] - p["arm_section"][1]
    d["reel_top"] = p["plate_t"] + p["reel_box"][2]
    # travel limits: the first contact as the rod goes down sets the penetration range
    d["limits"] = {
        "wire arm on reel housing": d["arm_under"] - d["reel_top"],
        "clamp collar on plate": d["collar_top"] - p["collar_h"] - p["plate_t"],
        "anvil on plate": d["z_anvil"] - p["plate_t"],
        "sensor pad on plate": d["z_anvil_top"] - p["pad_gap"] - p["pad"][2] - p["plate_t"],
    }
    d["travel"] = min(d["limits"].values())
    d["travel_by"] = min(d["limits"], key=d["limits"].get)
    d["arm_len"] = math.hypot(*p["reel_xy"])
    d["wire_start"] = d["arm_under"] - d["reel_top"]      # free wire length at zero depth
    return d


def build_parts(p=PARAMS):
    """Return {key: (name, shape, bom_no, color)} for the instrument set up at zero depth."""
    from build123d import Align, Box, Cone, Cylinder, Plane, Pos, Rot, Solid, Vector

    D = derived(p)
    BASE = (Align.CENTER, Align.CENTER, Align.MIN)
    rr = p["rod_d"] / 2

    def cyl(r, h, z, x=0.0, y=0.0):
        return Pos(x, y, z) * Cylinder(r, h, align=BASE)

    def tube3(a, b, r):
        a, b = Vector(*a), Vector(*b)
        v = b - a
        return Solid.make_cylinder(r, v.length, Plane(origin=a, z_dir=v.normalized()))

    parts = {}
    # 1 cone: 60 degree point, 20 mm base, short shoulder
    cone = Cone(0.4, p["cone_d"] / 2, D["cone_h"], align=BASE) + cyl(p["cone_d"] / 2, p["cone_shoulder"], D["cone_h"])
    parts["cone"] = ("Hardened cone, 20 mm, 60 degree", cone, 1, "#B45309")
    # 2 lower drive rod
    parts["lower_rod"] = ("Lower drive rod, 16 mm x 1,000 mm", cyl(rr, p["lower_rod_L"], D["z_rod"]), 2, "#6B7280")
    # 3 anvil and coupler
    parts["anvil"] = ("Anvil and coupler", cyl(p["anvil_d"] / 2, p["anvil_h"], D["z_anvil"]), 3, "#374151")
    # 4 hammer, resting on the anvil
    hz = D["z_anvil_top"]
    hammer = cyl(p["hammer_od"] / 2, D["hammer_L"], hz) - cyl(p["hammer_id"] / 2, D["hammer_L"] + 2, hz - 1)
    parts["hammer"] = ("Drop hammer, 8 kg", hammer, 4, "#0F766E")
    # 5 upper rod (hammer guide), through the stop collar
    parts["upper_rod"] = ("Upper rod (hammer guide)", cyl(rr, D["upper_L"], hz), 5, "#9CA3AF")
    # 6 stop collar, stem and tubular T-handle with bubble level (D1 backup)
    od, t = p["handle_tube"]
    bar = Pos(0, 0, D["z_handle"]) * Rot(90, 0, 0) * (Cylinder(od / 2, p["handle_w"]) - Cylinder(od / 2 - t, p["handle_w"] + 2))
    handle = (cyl(p["stop_d"] / 2, p["stop_h"], D["z_stop"]) + cyl(rr, p["handle_stem"], D["z_stop"] + p["stop_h"]) + bar
              + Pos(0, 0, D["z_handle"] + od / 2) * Box(16, 30, 8, align=BASE))
    parts["handle"] = ("Handle, top stop, bubble level", handle, 6, "#111827")
    # 7 reference plate with a center hole and a slot so it lifts off around the rod
    P, T = p["plate"], p["plate_t"]
    plate = (Box(P, P, T, align=BASE) - cyl(p["plate_hole"] / 2, T + 2, -1)
             - Pos(0, -P / 4, -1) * Box(p["slot_w"], P / 2 + 2, T + 2, align=BASE))
    parts["plate"] = ("Reference plate, slotted", plate, 7, "#94A3B8")
    # 8 draw-wire reel on the plate and its wire up to the arm eye
    rx, ry = p["reel_xy"]
    bx, by, bz = p["reel_box"]
    reel = Pos(rx, ry, T) * Box(bx, by, bz, align=BASE)
    wire = tube3((rx, ry, D["reel_top"]), (rx, ry, D["arm_under"]), 1.2)
    parts["drawwire"] = ("Draw-wire depth sensor", reel + wire, 8, "#2563EB")
    # 9 clamp collar on the lower rod with the wire arm
    aw, ah = p["arm_section"]
    ang = math.degrees(math.atan2(ry, rx))
    arm = (Pos(0, 0, D["arm_under"]) * Rot(0, 0, ang)
           * Pos(D["arm_len"] / 2 + 4, 0, 0) * Box(D["arm_len"] + 8, aw, ah, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    collar = cyl(p["collar_d"] / 2, p["collar_h"], D["collar_top"] - p["collar_h"]) - cyl(rr, p["collar_h"] + 2, D["collar_top"] - p["collar_h"] - 1)
    parts["clamp"] = ("Anvil clamp and wire arm, aluminum", collar + arm, 9, "#D4A017")
    # 10 blow and tilt sensor pad (Hall switch plus accelerometer) on a band clamp round the anvil
    pr, pt, ph = p["pad"]
    ra = p["anvil_d"] / 2
    pad_top = D["z_anvil_top"] - p["pad_gap"]
    pad = Pos(-(ra + pr / 2), 0, pad_top - ph) * Box(pr, pt, ph, align=BASE)
    band = cyl(ra + p["band_t"], p["band_h"], pad_top - ph + 4) - cyl(ra, p["band_h"] + 2, pad_top - ph + 3)
    parts["pad"] = ("Blow and tilt sensor pad", pad + band, 10, "#7C3AED")
    # 11 logger box on the plate
    lx, ly = p["logger_xy"]
    parts["logger"] = ("BLE logger, 3 x AA", Pos(lx, ly, T) * Box(*p["logger_box"], align=BASE), 11, "#16A34A")
    # 12 coiled cable from the pad down to the logger
    c = p["cable_d"] / 2
    a = (-(ra + pr / 2), 0, pad_top - ph)
    m = (-(ra + 30), -40, D["z_anvil"] - 250)
    b = (lx + 20, ly, T + p["logger_box"][2])
    parts["cable"] = ("Coiled sensor cable", tube3(a, m, c) + tube3(m, b, c), 12, "#1F2937")
    return parts


GROUPS = {
    "conepro-assembly": None,
    "hammer-assembly": ["hammer", "upper_rod", "handle"],
    "drive-train": ["cone", "lower_rod", "anvil"],
    "sensor-set": ["plate", "drawwire", "clamp", "pad", "logger", "cable"],
}


def export(parts=None):
    from build123d import Compound, export_step, export_stl
    parts = parts or build_parts()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    for name, keys in GROUPS.items():
        shapes = [parts[k][1] for k in (keys or parts)]
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.2)
    return list(GROUPS)


if __name__ == "__main__":
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
