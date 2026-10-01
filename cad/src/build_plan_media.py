"""ConePro prototype build plan pictures (CNP-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component laid out, numbered in build order
    cad/drawings/CNP-DWG-101 to 113        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/plate-holes.png     hole positions on the reference plate (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
C = build_components(P)
ZA, ZT = D["z_anvil"], D["z_anvil_top"]
RX, RY = P["reel_xy"]

COL = {"cone": "#B45309", "rod": "#6B7280", "clamp": "#D4A017", "anvil": "#374151", "hammer": "#0F766E",
       "mag": "#B91C1C", "upper": "#9CA3AF", "stop": "#1F2937", "tube": "#111827", "seat": "#475569",
       "level": "#22C55E", "pad": "#7C3AED", "iso": "#111827", "band": "#9CA3AF", "plate": "#94A3B8",
       "body": "#2563EB", "lid": "#60A5FA", "drum": "#CBD5E1", "motor": "#F59E0B", "board": "#16A34A",
       "wire": "#1D4ED8", "logger": "#16A34A", "llid": "#4ADE80", "cells": "#C2410C", "module": "#0F766E",
       "gland": "#1F2937", "cable": "#334155", "bolt": "#111827", "ground": "#D6C7B0"}


def _fuse(shapes):
    from build123d import Compound
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def S(*keys):
    return _fuse([C[k].shape for k in keys])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return shape & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))


def zwin(shape, z0, z1):
    return win(shape, -400, 400, -400, 400, z0, z1)


def thick_wire(z0, z1, r=2.0):
    """The 0.45 mm wire drawn thicker so it shows in pictures of the whole instrument."""
    from build123d import Cylinder, Pos, Align
    return Pos(RX, RY, z0) * Cylinder(r, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "cone": part("Cone", C["cone"].shape, COL["cone"]),
        "rod": part("Lower drive rod", C["lower_rod"].shape, COL["rod"]),
        "clamp": part("Clamp collar and wire arm", S("clamp", "clamp_screw"), COL["clamp"]),
        "anvil": part("Anvil", C["anvil"].shape, COL["anvil"]),
        "hammer": part("Drop hammer with its magnets", S("hammer", "magnets"), COL["hammer"]),
        "upper": part("Upper rod", C["upper_rod"].shape, COL["upper"]),
        "stop": part("Stop collar and roll pin", S("stop", "pin"), COL["stop"]),
        "tube": part("T-handle, level seat and level", S("tube", "seat", "level"), COL["tube"]),
        "pad": part("Sensor pad, isolator and band", S("pad", "isolator", "band"), COL["pad"]),
        "plate": part("Reference plate", C["plate"].shape, COL["plate"]),
        "housing": part("Reel housing and lid", S("reel_body", "reel_lid", "eyelet", "lid_screws"), COL["body"]),
        "reel": part("Drum, shaft, spring motor, sensor", S("drum", "shaft", "motor", "magnet", "board"), COL["drum"]),
        "wire": part("Wire, eye spring and end stop", S("wire", "eye_spring", "crimp"), COL["wire"]),
        "logger": part("Logger box, cells, board, glands", S("logger", "logger_lid", "cells", "module", "glands", "flange_screws"), COL["logger"]),
        "rcable": part("Reel cable and P-clips", S("reel_cable", "pclips"), COL["cable"]),
        "cable": part("Coiled sensor cable", C["cable"].shape, "#1F2937"),
    }


# ----------------------------------------------------------------- overview: laid out on a bench
def overview():
    """Every component laid out flat on a bench, numbered in build order. The rods lie along X."""
    from build123d import Pos, Rot, Cylinder, Align
    M = made()

    def flat(shape):
        return Rot(0, 90, 0) * shape

    def place(shape, x, y):
        """Move a shape so its left end is at x, its middle at y and it rests on the bench (z = 0)."""
        bb = shape.bounding_box()
        return Pos(x - bb.min.X, y - (bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * shape
    wire = _fuse([thick_wire(D["drum_cz"], D["collar_top"] + 15, 2.0), C["eye_spring"].shape, C["crimp"].shape])
    cable = Cylinder(3.5, 700, align=(Align.CENTER, Align.CENTER, Align.MIN))
    lay_out = {
        "cone": place(M["cone"].shape, 1000, 20),
        "rod": place(flat(M["rod"].shape), 0, 760),
        "clamp": place(M["clamp"].shape, 0, 420),
        "anvil": place(M["anvil"].shape, 250, 420),
        "hammer": place(M["hammer"].shape, 420, 420),
        "upper": place(flat(M["upper"].shape), 0, 600),
        "stop": place(M["stop"].shape, 880, 600),
        "tube": place(M["tube"].shape, 1010, 520),
        "pad": place(M["pad"].shape, 640, 420),
        "plate": place(M["plate"].shape, 0, 130),
        "housing": place(M["housing"].shape, 400, 180),
        "reel": place(M["reel"].shape, 560, 180),
        "wire": place(flat(wire), 0, -110),
        "logger": place(M["logger"].shape, 760, 160),
        "rcable": place(M["rcable"].shape, 950, 160),
        "cable": place(flat(cable), 0, -200),
    }
    order = ["cone", "rod", "clamp", "anvil", "hammer", "upper", "stop", "tube", "pad", "plate", "housing", "reel",
             "wire", "logger", "rcable", "cable"]
    parts = [part(M[k].name, lay_out[k], M[k].color) for k in order]
    parts[-1] = part("Coiled sensor cable (shown straight)", lay_out["cable"], "#1F2937")
    return bv.overview(parts, OUT / "overview.png", "ConePro prototype: every component, laid out",
                       subtitle="Numbered in build order, laid out on the bench before assembly. Seen from the front and above",
                       elev=62, azim=-90, size=(11, 8), dpi=150, key=True)

def broken(shape_flat, keep=110.0, gap=24.0):
    """A long part laid along X, drawn with its middle left out (a broken view)."""
    from build123d import Box, Pos, Compound
    bb = shape_flat.bounding_box()
    big = 400.0
    a = shape_flat & (Pos(bb.min.X + keep / 2, 0, 0) * Box(keep, big, big))
    b = shape_flat & (Pos(bb.max.X - keep / 2, 0, 0) * Box(keep, big, big))
    b = Pos(-(bb.size.X - 2 * keep - gap), 0, 0) * b
    return Compound(children=[a, b]), bb.size.X


def rod_sheet(part_, neighbours, flat_shape, dwg_no, title, material, notes, inset_view=(15, -58)):
    """component_sheet for a long rod: broken views at a readable scale, true length written on."""
    import shutil
    from drawing import Sheet, project_views, _t, INK
    view, L = broken(flat_shape)
    work = DWG / f"_{dwg_no}_views"
    views = project_views(view, work)
    inset = bv.where_it_goes(part_, neighbours, work / "where.png", elev=inset_view[0], azim=inset_view[1])
    s = Sheet(project="ConePro", title=title, dwg_no=dwg_no, rev="P1", author="Amish Chadha", date=DATE,
              concept="BUILD PLAN SKETCH, PLAN NOT YET BUILT", scale=None, material=material,
              revisions=[("P1", "Making sketch for the prototype build plan", DATE, "AC")])
    s.add_ortho(views, ["front", "top", "right"], dims=False)
    s._layers.append(_t(30, 60, f"Broken view: the middle of the rod is left out. True length {L:,.0f} mm overall.",
                        3.0, 600, INK, "start"))
    s.add_image(str(inset), 276, 30, 140, 70, label="Where it goes", sublabel="This part in colour, its neighbours in grey")
    s.add_notes("How to make it and how it fits", notes, x=276, y=112, width=140)
    s.save(DWG / dwg_no)
    shutil.rmtree(work, ignore_errors=True)
    return DWG / f"{dwg_no}.png"


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Pos, Rot
    M = made()
    base = dict(project="ConePro", date=DATE)
    out = []

    def flat(shape, z_lo):
        return Rot(0, 90, 0) * Pos(0, 0, -z_lo) * shape

    def nb(*keys, z0=None, z1=None):
        ps = [M[k] for k in keys]
        if z0 is not None:
            ps = [part(p.name, zwin(p.shape, z0, z1), p.color) for p in ps]
        return [p for p in ps if p.shape is not None and p.shape.volume > 1e-3]
    zr = D["z_rod"]
    lo, hi = ZA - 140, ZT + 160

    # 101 cone
    out.append(bv.component_sheet(
        part("Cone", C["cone"].shape, COL["cone"]), nb("rod", z0=0, z1=45),
        dwg_no="CNP-DWG-101", title="ConePro cone (make 2, one spare): making sketch",
        material="Tool steel or 4140 round bar 25 mm, hardened after machining",
        notes=["Make two. Turn from 25 mm bar: a 20.0 mm diameter body 12 mm long",
               "  with a 60 degree point below it (point 17.3 mm high), 29.3 mm overall.",
               "Keep the 20 mm diameter within 0.1 mm; a worn or undersize cone",
               "  biases the DCP index. Leave a sharp point, no flat.",
               "Top face: drill 10.2 mm 16 deep, tap M12 x 1.75 to 14 mm deep, and",
               "  face it square to the axis: the rod shoulder bears on this face.",
               "Harden after tapping (about 50 HRC); run a tap through after.",
               "Fit: screws onto the M12 stud on the bottom of the lower rod with",
               "  medium thread locker; the rod shoulder seats on the top face.",
               "Check: 20.0 mm across the body; 60 degrees with a gauge; the",
               "  rod shoulder sits flat on the top face with no gap."],
        inset_view=(15, -58), **base))

    # 102 lower drive rod, laid flat
    out.append(rod_sheet(
        part("Lower drive rod", C["lower_rod"].shape, COL["rod"]), [M["cone"], M["anvil"], M["clamp"]],
        flat_shape=flat(C["lower_rod"].shape, zr - P["stud_cone"]),
        dwg_no="CNP-DWG-102", title="ConePro lower drive rod: making sketch",
        material="16 mm 4140 class steel rod, ground or bright",
        notes=["Cut 1,032 mm of 16 mm rod; face both ends square.",
               "Bottom end: turn an M12 x 1.75 stud 12 mm long (12.0 mm diameter)",
               "  and cut the thread; leave a square, flat 16 mm shoulder.",
               "Top end: turn an M12 stud 20 mm long the same way.",
               "The shoulders are 1,000 mm apart. Both shoulders carry every",
               "  blow, so face them square and break the edge 0.5 mm.",
               "Engrave a ring every 10 mm, deeper every 100 mm, measured up from",
               "  the cone point with the cone fitted (the point is 29.3 mm",
               "  below the bottom shoulder). This is the backup depth scale.",
               "Fit: the cone screws on the bottom stud, the anvil on the top",
               "  stud; the clamp collar slides on from the top before the anvil.",
               "Check: straight within 1 mm over its length when rolled on a",
               "  flat bench; both studs take an M12 nut by hand."]))

    # 103 clamp and wire arm, flat in XY
    clamp = Rot(0, 0, -D["arm_ang"]) * Pos(0, 0, -(ZA - P["collar_h"])) * C["clamp"].shape
    out.append(bv.component_sheet(
        part("Clamp collar and wire arm", S("clamp", "clamp_screw"), COL["clamp"]),
        nb("rod", "anvil", "pad", z0=ZA - 150, z1=ZT + 20),
        dwg_no="CNP-DWG-103", title="ConePro clamp collar and wire arm: making sketch",
        material="Aluminium plate 12 mm, 6061 class", view_shape=clamp,
        notes=["One piece cut from 12 mm plate: a 40 mm round boss and an arm",
               "  16 mm wide reaching 122 mm from the boss centre.",
               "Bore the boss 16 mm (a sliding fit on the rod, ream if you can).",
               "Wire eye: a 3.2 mm hole on the arm centre line, 112.4 mm from",
               "  the bore centre; break both edges so the wire cannot chafe.",
               "Saw a 1.5 mm slit from the bore out through the boss on the side",
               "  opposite the arm.",
               "Clamp screw: at 14 mm from the bore centre, square across the slit,",
               "  drill 5.5 mm through the near jaw with a 9 mm spot face, and",
               "  drill 4.2 mm and tap M5 in the far jaw.",
               "Fit: slides on the lower rod from the top; its top face butts the",
               "  underside of the anvil, which carries it at every blow. Turn the",
               "  arm to point at the reel's wire exit, then tighten the M5 screw.",
               "Check: slides on the rod with the screw slack; locks by hand."],
        inset_view=(20, -40), **base))

    # 104 anvil
    out.append(bv.component_sheet(
        part("Anvil", C["anvil"].shape, COL["anvil"]), nb("rod", "upper", "clamp", "pad", z0=lo, z1=hi),
        dwg_no="CNP-DWG-104", title="ConePro anvil: making sketch", material="Steel round bar 70 mm, 1045 or 4140 class",
        view_shape=Pos(0, 0, -ZA) * C["anvil"].shape,
        notes=["Turn to 64 mm diameter x 60 mm long; face both ends square and",
               "  parallel within 0.1 mm. Chamfer the outer edges 1 mm.",
               "Both end faces: centre drill, drill 10.2 mm 27 mm deep and tap",
               "  M12 x 1.75 to 24 mm deep. The two holes do not meet.",
               "The top face takes every hammer blow: leave it flat and smooth.",
               "Fit: the lower rod's top stud screws into the bottom hole and the",
               "  upper rod's stud into the top hole, each to its shoulder, with",
               "  medium thread locker. The clamp collar butts the bottom face;",
               "  the sensor pad and band clamp onto its side.",
               "Check: both rods seat on their shoulders with no rock; the anvil",
               "  spins true on the rod within 0.2 mm."],
        inset_view=(15, -58), **base))

    # 105 hammer
    out.append(bv.component_sheet(
        part("Drop hammer", C["hammer"].shape, COL["hammer"]), nb("anvil", "upper", "pad", z0=lo, z1=ZT + 300),
        dwg_no="CNP-DWG-105", title="ConePro drop hammer: making sketch", material="Steel round bar 100 mm, 1018 to 1045 class",
        view_shape=Pos(0, 0, -ZT) * S("hammer", "magnets"),
        notes=["Saw 140 mm of 100 mm bar. Bore 22 mm through.",
               "Face both ends square; the lower face strikes the anvil.",
               "Lower face: 16 pockets 8.2 mm diameter, 5 mm deep, equally spaced",
               "  (22.5 degrees) on an 82 mm circle, all outside the 64 mm area",
               "  that strikes the anvil.",
               "Weigh, then face the top end down to 8.00 kg, within 10 g",
               "  (about 136.5 mm long).",
               "Bond a 8 x 4 mm N42 magnet in each pocket with epoxy, 0.5 mm",
               "  below the face, every one with the same pole facing down.",
               "Paint or oil the outside; keep the strike face bare.",
               "Fit: slides on the upper rod (3 mm clearance all round) and",
               "  falls 575 mm onto the anvil.",
               "Check: 8.00 kg; slides freely the length of a 16 mm rod; no",
               "  magnet stands proud of the face."],
        inset_view=(20, -58), **base))

    # 106 upper rod, laid flat
    out.append(rod_sheet(
        part("Upper rod", C["upper_rod"].shape, COL["upper"]), [M["hammer"], M["stop"], M["tube"], M["anvil"]],
        flat_shape=flat(C["upper_rod"].shape, ZT - P["stud_anvil"]),
        dwg_no="CNP-DWG-106", title="ConePro upper rod (hammer guide): making sketch",
        material="16 mm 4140 class steel rod, ground or bright",
        notes=["Cut 796 mm of 16 mm rod; face both ends square.",
               "Bottom end: turn an M12 x 1.75 stud 20 mm long with a square",
               "  shoulder. The shoulder is the anvil top: measure from it.",
               "The rod above the shoulder is 776.5 mm; its top end ends",
               "  flush with the top of the T-handle tube.",
               "Smooth the rod between the shoulder and 715 mm: the hammer",
               "  slides on it.",
               "The 6 mm roll pin hole, 720.5 mm above the shoulder, is drilled",
               "  through the rod and the stop collar together (DWG-107).",
               "Fit: the hammer goes on from the bottom end; then the stud",
               "  screws into the anvil with medium thread locker.",
               "Check: straight within 0.5 mm; the hammer slides its whole",
               "  length without sticking."]))

    # 107 stop collar
    out.append(bv.component_sheet(
        part("Stop collar", S("stop", "pin"), COL["stop"]), nb("upper", "tube", z0=D["z_stop"] - 200, z1=D["height"] + 5) + [part("Hammer at the stop", Pos_z(C["hammer"].shape, P["drop"]), COL["hammer"])],
        dwg_no="CNP-DWG-107", title="ConePro top stop collar: making sketch", material="Steel round bar 50 mm, 1018 class",
        view_shape=Pos(0, 0, -D["z_stop"]) * S("stop", "pin"),
        notes=["Turn to 44 mm diameter x 18 mm; bore 16 mm, a close slide fit.",
               "Face both ends square; the hammer's top face hits the underside.",
               "Slide it on the upper rod from the top so its underside is",
               "  711.5 mm above the rod shoulder. With the 136.5 mm hammer",
               "  this gives the 575 mm free drop. Set it with a rule and check",
               "  the drop with the hammer on a flat plate standing for the anvil.",
               "Clamp it there and drill 6 mm straight through collar and rod",
               "  together, at mid-height (720.5 mm above the shoulder).",
               "Drive in a 6 x 40 mm spring steel roll pin; its ends sit just",
               "  inside the collar's outside surface.",
               "Check: the free drop is 575 mm, within 2 mm; the collar does not",
               "  move when the hammer is jerked up against it."],
        inset_view=(15, -58), **base))

    # 108 T-handle and level seat
    tee = S("tube", "seat", "level")
    out.append(bv.component_sheet(
        part("T-handle and level seat", tee, COL["tube"]), nb("upper", "stop", z0=D["z_stop"] - 150, z1=D["height"] + 5),
        dwg_no="CNP-DWG-108", title="ConePro T-handle, level seat and level: making sketch",
        material="Steel tube 26 x 2.5 mm; steel disc 30 x 5 mm; bought bullseye level",
        view_shape=Rot(0, 0, 90) * Pos(0, 0, -D["z_handle"]) * tee,
        notes=["Tube: cut 260 mm of 26 x 2.5 mm steel tube; deburr; plug the",
               "  ends with push-in caps after painting.",
               "At mid-length drill 16 mm straight through both walls, square",
               "  to the tube, so the upper rod passes through.",
               "Seat disc: 30 mm diameter, 5 mm thick, with a 20 mm recess",
               "  3 mm deep in its top face.",
               "Fit: push the upper rod up through the tube until its top end is",
               "  flush with the top of the tube, the tube square to the rod.",
               "Weld the tube to the rod all round where the rod comes out, top",
               "  and bottom (or have a shop do it). Weld the disc centred on the",
               "  rod top. Paint, then bond the 20 mm bubble level in the recess.",
               "Check: the level reads centred when the rod hangs plumb; the",
               "  handle is square to the rod within 1 degree."],
        inset_view=(20, -58), **base))

    # 109 sensor pad
    padv = C["pad"].shape
    out.append(bv.component_sheet(
        part("Sensor pad", C["pad"].shape, COL["pad"]),
        nb("anvil", "rod", "clamp", z0=lo, z1=ZT + 10) + [part("Isolator and band", S("isolator", "band"), COL["band"])],
        dwg_no="CNP-DWG-109", title="ConePro blow and tilt sensor pad: making sketch",
        material="Printed PETG or ASA shell, potting epoxy; 4 mm elastomer sheet",
        view_shape=Pos(0, 0, -D["pad_bot"]) * padv,
        notes=["Shell: print 30 wide x 30 tall x 18 deep at the middle, open",
               "  at the back, 2 mm walls. The face toward the anvil is curved",
               "  to a 36 mm radius (anvil radius plus the 4 mm isolator).",
               "  For another anvil size use its radius plus 4 mm.",
               "Fit the sensor board (Hall switch and accelerometer) with the",
               "  Hall switch 1 mm under the top face; feed the cable through",
               "  the 6 mm hole in the boss under the pad.",
               "Fill with potting epoxy; let it cure fully before use.",
               "Isolator: cut 30 x 30 mm of 4 mm elastomer; it bends to the",
               "  anvil. Bond it to the pad's curved face.",
               "Fit: the pad sits on the anvil side, its top 8 mm below the",
               "  anvil top, under the hammer's overhang. The band clamp goes",
               "  round the anvil and over the pad's outer face.",
               "Check: the pad is fully potted; no wire shows at the top."],
        inset_view=(20, -150), **base))

    # 110 reference plate
    out.append(bv.component_sheet(
        part("Reference plate", C["plate"].shape, COL["plate"]), [M["housing"], M["logger"], M["rcable"]] + nb("rod", "cone", z0=0, z1=160),
        dwg_no="CNP-DWG-110", title="ConePro reference plate: making sketch", material="Aluminium plate 6 mm, 5083 or 6082 class",
        notes=["Cut a 300 x 300 mm blank; round the corners 10 mm; deburr.",
               "Positions from the plate centre: X toward the reel side, Y away",
               "  from the slot. The hole positions picture repeats them.",
               "Centre hole 60 mm; a 60 mm wide slot from the hole to the -Y",
               "  edge (chain drill, jigsaw, file straight).",
               "Reel: four 4.2 mm holes, countersunk from below for M4, at",
               "  X 45.3 and 103.3, Y 30 and 60.",
               "Logger flanges: four holes drilled 3.3 mm and tapped M4 at",
               "  X -113 and -77, Y 14 and 96.",
               "P-clips: two holes tapped M4 at (X 4, Y 66) and (X -14, Y 66).",
               "Check: lies flat on a bench within 1 mm; screw heads under",
               "  the plate sit flush or below the bottom face."],
        inset_view=(35, -60), **base))

    # 111 reel housing body and lid
    hb = S("reel_body", "reel_lid")
    out.append(bv.component_sheet(
        part("Reel housing and lid", hb, COL["body"]), [M["plate"], M["reel"], part("Wire", thick_wire(D["drum_cz"], 200, 0.8), COL["wire"])],
        dwg_no="CNP-DWG-111", title="ConePro draw-wire reel housing and lid: making sketch",
        material="Printed ASA or PETG, 100 % infill walls; brass heat-set inserts",
        view_shape=Pos(-RX + 30.7, -RY, -P["plate_t"]) * hb, inset_view=(25, -70),
        notes=["Body: 72 wide x 57 deep x 72 tall outside, 3 mm walls, open on",
               "  the front (-Y) face. Print standing on its base.",
               "Inside, four 8 x 8 mm posts at the corners: the lower two run",
               "  front to back, the upper two are 10 mm long at the front.",
               "Bearing boss on the back wall, 18 mm diameter x 15 mm, centred",
               "  36 mm from the left face and 36 mm up: press in two 6 x 13 x 5",
               "  mm bearings.",
               "Top: a 5.2 mm hole for the wire eyelet, 5.3 mm in from the right",
               "  face and on the front-to-back centre line.",
               "Left face: a 12 mm hole for the cable gland, 12 mm from the back",
               "  and 22 mm up.",
               "Inserts: M4 into the lower posts from below (two per post, 20 and",
               "  50 mm from the front); M3 into the four post ends at the front.",
               "Lid: 72 x 72 x 3 mm, four 3.4 mm holes over the post ends, and a",
               "  pad for the sensor board. Seal with a 1.5 mm cord in the joint."],
        **base))

    # 112 drum
    drum = Pos(-D["drum_cx"], 0, -D["drum_cz"]) * C["drum"].shape
    out.append(bv.component_sheet(
        part("Grooved drum", C["drum"].shape, COL["drum"]), [M["housing"], part("Shaft and spring motor", S("shaft", "motor", "magnet", "board"), COL["motor"])],
        dwg_no="CNP-DWG-112", title="ConePro draw-wire drum: making sketch", material="Aluminium round bar 65 mm, 6061 class",
        view_shape=drum, inset_view=(15, -100),
        notes=["Turn to 60.0 mm diameter x 20 mm; bore 6 mm (a close fit on the",
               "  shaft). The diameter sets the scale: 188.5 mm of wire per turn.",
               "Cut a helical groove 1 mm pitch and 0.5 mm deep over 7 mm of",
               "  the width, centred, with the lathe set to screw-cut 1 mm pitch.",
               "Drill a 1 mm anchor hole at the start of the groove for the",
               "  wire end, and an M3 set screw hole into the bore.",
               "Fit: on the 6 mm shaft beside the spring motor, set screw on",
               "  the shaft flat. The wire leaves the drum straight up under",
               "  the eyelet: the drum's right-hand edge is under the eyelet.",
               "Wind the 1,000 mm wire on in a single layer, in the groove.",
               "Check: runs true within 0.05 mm; the wire lies in the groove",
               "  in one layer with the arm at the full 939 mm stroke."],
        **base))

    # 113 logger box, drilled
    lg = S("logger", "logger_lid")
    lx, ly = P["logger_xy"]
    out.append(bv.component_sheet(
        part("Logger box", lg, COL["logger"]), [M["plate"], part("Glands and cables", S("glands", "reel_cable", "pclips"), COL["gland"])],
        dwg_no="CNP-DWG-113", title="ConePro logger box: drilling sketch", material="Bought IP65 ABS or polycarbonate box with flanges",
        view_shape=Pos(-lx, -ly, -P["plate_t"]) * lg, inset_view=(25, -40),
        notes=["Buy a flanged IP65 box about 100 x 70 x 42 mm with a gasketed",
               "  lid; its flange holes go 82 mm apart across the box and 36 mm",
               "  apart along it (or move the plate holes to suit your box).",
               "Drill two 12 mm holes in the end wall that faces the rod, both",
               "  21 mm above the box floor's underside: one 12 mm and one 38 mm",
               "  from the box side nearest the plate slot.",
               "The first takes the M12 gland for the coiled sensor cable, the",
               "  second the gland for the reel cable.",
               "Pilot drill 3 mm, open with a step drill at low speed, deburr.",
               "Inside: the three-AA holder on the floor at the far end, the",
               "  logger board near the glands, on double-sided foam tape or",
               "  the box's own bosses.",
               "Fit: flanges flat on the plate, four M4 pan-head screws into",
               "  the tapped plate holes.",
               "Check: the lid gasket seats all round; both glands tighten",
               "  on their cables."],
        **base))
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []
    M = made()

    def j(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    zr = D["z_rod"]
    # 1 cone on the rod
    j(1, [part("Cone", C["cone"].shape, COL["cone"]),
          part("Lower rod with its M12 stud", zwin(C["lower_rod"].shape, 0, zr + 60), COL["rod"])],
      "cone on the lower rod", "Cut open. The rod's M12 stud screws into the cone; the rod shoulder bears on the cone's top face",
      cut="+Y", elev=10, azim=-90)
    # 2 rod into anvil, clamp against the underside
    z0, z1 = ZA - 50, ZT + 10
    j(2, [part("Lower rod, top stud", zwin(C["lower_rod"].shape, z0, z1), COL["rod"]),
          part("Anvil", C["anvil"].shape, COL["anvil"]),
          part("Upper rod, bottom stud", zwin(C["upper_rod"].shape, z0, ZT + 50), COL["upper"]),
          part("Clamp collar, butting the anvil", win(C["clamp"].shape, -40, 40, -40, 40, z0, z1), COL["clamp"])],
      "rods into the anvil, clamp collar under it", "Cut open. Each M12 stud screws in to its shoulder; the collar's top face butts the anvil",
      cut="+Y", elev=10, azim=-90)
    # 3 hammer on the anvil, magnets above the pad
    z0 = ZT - 50
    w3 = lambda sh, za, zb: win(sh, -70, 22, -60, 60, za, zb)  # noqa: E731
    j(3, [part("Anvil", w3(C["anvil"].shape, z0, ZT), COL["anvil"]),
          part("Drop hammer, resting on the anvil", win(C["hammer"].shape, -70, -12, -60, 60, ZT, ZT + 45), COL["hammer"]),
          part("Magnet, 0.5 mm below the hammer face", win(C["magnets"].shape, -47, -35, -6, 6, ZT, ZT + 45), COL["mag"]),
          part("Sensor pad, 8 mm below the hammer face", C["pad"].shape, COL["pad"]),
          part("Isolator", C["isolator"].shape, COL["iso"]),
          part("Upper rod", w3(C["upper_rod"].shape, z0, ZT + 45), COL["upper"])],
      "hammer, magnets and sensor pad", "Cut open through the pad. The magnets pass 8.5 mm above the pad as the hammer lands",
      cut="+Y", elev=8, azim=-90, size=(10, 5.5))
    # 4 stop collar and pin
    zs = D["z_stop"]
    j(4, [part("Upper rod", zwin(C["upper_rod"].shape, zs - 40, zs + 40), COL["upper"]),
          part("Stop collar", C["stop"].shape, COL["stop"]),
          part("Roll pin, 6 mm", C["pin"].shape, COL["bolt"]),
          part("Hammer top, at the stop", zwin(Pos_z(C["hammer"].shape, P["drop"]), zs - 40, zs + 2), COL["hammer"])],
      "stop collar on the upper rod", "Cut open. A 6 mm roll pin through collar and rod sets the 575 mm drop",
      cut="-X", elev=10, azim=0)
    # 5 T-handle tee
    zh = D["z_handle"]
    j(5, [part("Upper rod", zwin(C["upper_rod"].shape, zh - 40, zh + 20), COL["upper"]),
          part("T-handle tube, welded to the rod", win(C["tube"].shape, -60, 60, -60, 60, zh - 20, zh + 20), COL["tube"]),
          part("Level seat, welded on the rod top", C["seat"].shape, COL["seat"]),
          part("Bubble level, bonded", C["level"].shape, COL["level"])],
      "T-handle, rod and level", "Cut open. The rod passes through the tube, its top flush; welds where the rod meets the tube",
      cut="+Y", elev=10, azim=-90)
    # 6 pad and band, seen from above, cut at the band
    zb = D["pad_bot"] + 15
    box_ = (-80, 60, -60, 60, zb - 4, zb + 4)
    j(6, [part("Anvil", win(C["anvil"].shape, *box_), COL["anvil"]),
          part("Isolator", win(C["isolator"].shape, *box_), COL["iso"]),
          part("Sensor pad", win(C["pad"].shape, *box_), COL["pad"]),
          part("Band clamp, round the anvil and over the pad", win(C["band"].shape, *box_), COL["band"])],
      "sensor pad and band clamp on the anvil", "Cut level with the band, seen from above. The band presses the pad and isolator onto the anvil",
      elev=88, azim=-90)
    # 7 inside the reel, lid off
    j(7, [part("Housing body (lid off)", C["reel_body"].shape, COL["body"]),
          part("Grooved drum", C["drum"].shape, COL["drum"]),
          part("Eyelet", C["eyelet"].shape, "#D4A017"),
          part("Wire, straight up from the drum edge", thick_wire(D["drum_cz"], D["reel_top"] + 30, 0.9), "#DC2626")],
      "inside the draw-wire reel", "Seen straight from the front, lid and spring motor off. The wire leaves the drum's edge straight up through the eyelet",
      elev=0, azim=-90)
    # 8 reel and lid screws, cut through the left posts
    hx0 = D["drum_cx"] - P["reel_box"][0] / 2
    xs = hx0 + P["reel_wall"] + 4.0                                   # screw axis
    box_ = (xs - 12, xs + 12, 0, 80, -3, 30)
    j(8, [part("Reference plate", win(C["plate"].shape, *box_), COL["plate"]),
          part("Housing body and post", win(C["reel_body"].shape, *box_), COL["body"]),
          part("Lid", win(C["reel_lid"].shape, *box_), COL["lid"]),
          part("M4 countersunk screws from below", win(C["reel_screws"].shape, *box_), COL["bolt"]),
          part("M3 lid screw", win(C["lid_screws"].shape, *box_), "#374151")],
      "reel housing on the plate", "Cut through the lower left post. M4 screws come up through the plate into inserts in the post",
      cut="-X", elev=35, azim=40)
    # 9 wire eye on the arm
    ct = D["collar_top"]
    box_ = (RX - 25, RX + 25, RY - 25, RY + 25, ct - 40, ct + 30)
    j(9, [part("Wire arm", win(C["clamp"].shape, *box_), COL["clamp"]),
          part("Preload eye spring", C["eye_spring"].shape, "#F59E0B"),
          part("Wire end stop, crimped", C["crimp"].shape, "#475569"),
          part("Draw wire through the eye", win(thick_wire(ct - 40, ct + 20, 0.6), *box_), COL["wire"])],
      "wire eye on the arm", "Cut open. The wire passes up through the arm, through the spring, and is crimped above it",
      cut="+Y", elev=6, azim=-90)
    # 10 logger end with glands and cables
    lx1 = P["logger_xy"][0] + P["logger_box"][0] / 2
    box_ = (lx1 - 45, lx1 + 45, 0, 110, 0, 60)
    j(10, [part("Plate", win(C["plate"].shape, *box_), COL["plate"]),
           part("Logger box and flange", win(S("logger", "logger_lid"), *box_), COL["logger"]),
           part("M4 flange screws", win(C["flange_screws"].shape, *box_), COL["bolt"]),
           part("M12 glands", win(C["glands"].shape, *box_), COL["gland"]),
           part("Coiled sensor cable", win(C["cable"].shape, *box_), "#1F2937"),
           part("Reel cable, in a P-clip", win(S("reel_cable", "pclips"), *box_), "#64748B")],
       "logger glands and cables", "The two cables enter through glands in the end wall facing the rod; flanges screw to the plate",
       elev=25, azim=-30)
    return out


def Pos_z(shape, dz):
    from build123d import Pos
    return Pos(0, 0, dz) * shape


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    def short(p, z0, z1, name=None):
        return part(name or p.name, zwin(p.shape, z0, z1), p.color)
    zr = D["z_rod"]
    rod_lo = short(M["rod"], 0, 260, "Lower drive rod (shown short)")
    st(1, [rod_lo], [mv(M["cone"], (0, 0, -70))], "cone onto the lower rod",
       "Medium thread locker on the bottom stud; screw the cone on until the rod shoulder seats", elev=12, azim=-60)
    rod_hi = short(M["rod"], ZA - 260, ZA + 30, "Lower drive rod (shown short)")
    st(2, [rod_hi], [mv(M["clamp"], (0, 0, 140))], "clamp collar onto the lower rod",
       "Slide it on from the top end, screw slack, arm roughly toward where the reel will be", elev=20, azim=-60)
    st(3, [rod_hi, M["clamp"]], [mv(M["anvil"], (0, 0, 140))], "anvil onto the lower rod",
       "Thread locker on the top stud; screw the anvil down to the shoulder; push the collar up against it",
       elev=15, azim=-60)
    st(4, [rod_hi, M["clamp"], M["anvil"]], [mv(M["pad"], (-120, 0, 0))], "sensor pad and band onto the anvil",
       "Pad top 8 mm below the anvil top, opposite the arm; band round the anvil and over the pad, tight",
       elev=15, azim=-60, label_done=False)
    upper_set = [M["upper"], M["stop"], M["tube"]]
    st(5, upper_set, [mv(M["hammer"], (0, 0, -260))], "hammer onto the upper rod",
       "The rod already carries the pinned stop collar and the welded handle; slide the hammer on from the bottom end",
       elev=12, azim=-60, label_done=True)
    st(6, [short(M["rod"], ZA - 200, ZA + 30, "Lower drive rod (shown short)"), M["clamp"], M["anvil"], M["pad"]],
       [mv(part("Hammer assembly", S("upper_rod", "stop", "pin", "tube", "seat", "level", "hammer", "magnets"), COL["hammer"]), (0, 0, 120))],
       "hammer assembly into the anvil",
       "Hold the hammer up; thread locker on the stud; screw the upper rod into the anvil to its shoulder",
       elev=10, azim=-60, label_done=False)
    st(7, [part("Housing body", C["reel_body"].shape, "#D1D5DB")],
       [mv(part("Drum, spring motor and shaft", S("drum", "motor", "shaft", "magnet"), "#0891B2"), (0, -130, 0))],
       "drum and shaft into the reel housing",
       "Wire wound on in one layer first; shaft into the bearings in the back boss; wire up through the eyelet hole",
       elev=15, azim=-60, label_done=True)
    st(8, [part("Housing with drum", S("reel_body", "drum", "motor", "shaft", "magnet"), "#D1D5DB")],
       [mv(part("Lid with sensor board", S("reel_lid", "board", "lid_screws"), COL["lid"]), (0, -90, 0)),
        mv(part("Eyelet", C["eyelet"].shape, "#D4A017"), (0, 0, 40))],
       "lid, sensor board and eyelet", "Sealing cord in the joint; four M3 screws; press the eyelet into the top over the wire",
       elev=15, azim=-60, label_done=False)
    reel = part("Draw-wire reel", S("reel_body", "reel_lid", "drum", "motor", "shaft", "magnet", "board", "eyelet", "lid_screws"), COL["body"])
    st(9, [M["plate"]], [mv(reel, (0, 0, 120)), mv(part("M4 countersunk screws (4)", C["reel_screws"].shape, COL["bolt"]), (0, 0, -80))],
       "reel onto the plate", "Four M4 countersunk screws up through the plate into the inserts; heads flush underneath",
       elev=28, azim=-60, label_done=False)
    st(10, [M["plate"], reel], [mv(M["logger"], (0, 0, 120))], "logger onto the plate",
       "Glands fitted, cells and board inside; four M4 pan-head screws through the flanges into the plate",
       elev=28, azim=-60, label_done=False)
    st(11, [M["plate"], reel, M["logger"]], [mv(M["rcable"], (0, 0, 80))], "reel-to-logger cable",
       "Through both glands; lay it on the plate in the two P-clips; tighten the glands", elev=30, azim=-60, label_done=False)
    # at the test point: the drive train stands on its cone; the plate slides round the rod
    ground = part("Ground (test point)", _ground(), COL["ground"])
    drive = part("Cone and lower rod (rest of the instrument not shown)", _fuse([zwin(C[k].shape, 0, 330) for k in ("cone", "lower_rod")]), "#D1D5DB")
    sensor_plate = part("Plate with reel and logger", S("plate", "reel_body", "reel_lid", "eyelet", "logger", "logger_lid", "glands",
                                                       "reel_cable", "pclips", "flange_screws"), COL["plate"])
    st(12, [drive], [mv(sensor_plate, (0, 260, 0))], "plate round the rod at the test point",
       "Cone point on the ground; slide the plate on so the rod passes along the slot into the centre hole",
       context=[ground], elev=30, azim=-35, label_done=True)
    # whole instrument: hook the wire and plug the cable
    whole_done = [part(k, C[k].shape, "#D1D5DB") for k in ("cone", "lower_rod", "clamp", "clamp_screw", "anvil", "hammer", "magnets",
                                                          "upper_rod", "stop", "pin", "tube", "seat", "level", "pad", "isolator",
                                                          "band", "plate", "reel_body", "reel_lid", "eyelet", "logger",
                                                          "logger_lid", "glands", "reel_cable", "pclips")]
    st(13, whole_done, [mv(part("Draw wire to the arm eye", thick_wire(D["reel_top"], D["arm_under"] + 25, 2.5), COL["wire"]), (0, 0, 0)),
                        mv(part("Coiled cable, pad to logger", C["cable"].shape, "#7C3AED"), (0, 0, 0))],
       "wire to the arm and cable to the logger",
       "Pull the wire up through the arm eye, spring and end stop; plug in the coiled cable. Wire drawn thick to show",
       elev=18, azim=-55, label_done=False, size=(8, 9))
    return out


def _ground():
    from build123d import Box, Pos, Align
    return Pos(0, 0, -20) * Box(500, 700, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))


# ----------------------------------------------------------------- plate hole positions
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    fig = plt.figure(figsize=(10, 10), dpi=150)
    ax = fig.add_axes([0.06, 0.07, 0.62, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((-140, -140), 280, 280, boxstyle="round,pad=10", fc="#F5F5F4", ec=INK, lw=1.2))
    ax.add_patch(Circle((0, 0), 30, fc="white", ec=INK, lw=1.1))
    ax.add_patch(Rectangle((-30, -151), 60, 151, fc="white", ec="none"))
    ax.plot([-30, -30], [-150, 0], color=INK, lw=1.1); ax.plot([30, 30], [-150, 0], color=INK, lw=1.1)
    ax.axvline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3))); ax.axhline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    holes = [((45.3, 30), "csk"), ((45.3, 60), "csk"), ((103.3, 30), "csk"), ((103.3, 60), "csk"),
             ((-113, 14), "tap"), ((-113, 96), "tap"), ((-77, 14), "tap"), ((-77, 96), "tap"),
             ((4, 66), "tap"), ((-14, 66), "tap")]
    for (x, y), k in holes:
        ax.add_patch(Circle((x, y), 2.1 if k == "tap" else 4.0, fc="white", ec=INK, lw=1))
        if k == "csk":
            ax.add_patch(Circle((x, y), 2.1, fc="white", ec=INK, lw=0.6))
        ax.plot([x - 6, x + 6], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - 6, y + 6], color=MUT, lw=0.4)
    # outlines of what sits on the plate
    hx0 = D["drum_cx"] - 36
    ax.add_patch(Rectangle((hx0, 10), 72, 60, fc="none", ec="#2563EB", lw=0.8, ls="--"))
    ax.text(hx0 + 36, 74, "reel housing", color="#2563EB", fontsize=7.5, ha="center")
    ax.add_patch(Rectangle((-145, 20), 100, 70, fc="none", ec="#16A34A", lw=0.8, ls="--"))
    ax.text(-95, 52, "logger box", color="#16A34A", fontsize=7.5, ha="center")
    ax.plot([RX], [RY], marker="x", color="#B91C1C", ms=6)
    ax.text(RX + 7, RY + 8, "wire exit", color="#B91C1C", fontsize=7, zorder=5, bbox=dict(fc="white", ec="none", pad=1))
    ax.text(0, -120, "slot, 60 wide", ha="center", fontsize=7.5, color=MUT, zorder=5, bbox=dict(fc="#F5F5F4", ec="none", pad=1.5))
    ax.text(0, 36, "60 hole", ha="center", fontsize=7.5, color=MUT, zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))
    xs = sorted({x for (x, _), _ in holes})
    for i, x in enumerate(xs):
        yl = -160 - 9 * (i % 2)
        ax.plot([x, x], [-150, yl + 3], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
    ys = sorted({y for (_, y), _ in holes})
    for i, y in enumerate(ys):
        ax.plot([150, 158 + 14 * (i % 2)], [y, y], color=AC, lw=0.4, ls=":")
        ax.text(160 + 14 * (i % 2), y, f"{y:g}", va="center", fontsize=7.5, color=AC)
    ax.text(0, -186, "X from the centre, mm (+ toward the reel)", ha="center", fontsize=8, color=MUT, zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.text(196, 0, "Y from the centre, mm (+ away from the slot)", rotation=90, ha="center", va="center", fontsize=8, color=MUT, zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_xlim(-160, 205); ax.set_ylim(-195, 160)
    fig.text(0.04, 0.975, "Reference plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.948, "Seen from above (the face the reel and logger sit on). Figures in mm, taken from the model.", fontsize=8.5, color=MUT, va="top")
    key = ["Centre hole 60, slot 60 wide", "  to the -Y edge",
           "Reel: 4 holes 4.2, countersunk", "  from BELOW for M4, at", "  X 45.3 and 103.3, Y 30 and 60",
           "Logger flanges: 4 holes tapped", "  M4 (drill 3.3), at", "  X -113 and -77, Y 14 and 96",
           "P-clips: 2 holes tapped M4", "  at (4, 66) and (-14, 66)",
           "", "Dashed: where the reel and", "  logger sit. Cross: wire exit", "  (X 105, Y 40)"]
    fig.text(0.71, 0.86, "What each hole is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.71, 0.83 - i * 0.022, t, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, "github.com/BoujeeEnjinia1701/conepro", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "plate-holes.png"


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    INK, MUT = "#111827", "#4B5563"
    fig = plt.figure(figsize=(12, 6.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 66); ax.set_axis_off()
    ax.text(2, 64, "ConePro prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 60.6, "Bought modules wired at block level; no circuit board is laid out. Everything runs from three AA cells (4.5 V).",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/conepro", fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.4, sub, ha="center", va="top", fontsize=7.4, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, t, color, ha="left"):
        ax.text(x, y, t, fontsize=7.4, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    ax.add_patch(FancyBboxPatch((40, 9), 44, 44, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(41.5, 51.8, "Inside the logger box (IP65)", fontsize=8, color=MUT, va="top")
    blk(3, 34, 22, 15, "Sensor pad (potted)", "Hall-effect switch\n3-axis accelerometer", "#7C3AED")
    blk(3, 11, 22, 15, "Draw-wire reel", "12-bit magnetic angle\nsensor board", "#2563EB")
    blk(46, 28, 20, 18, "BLE logger board", "microcontroller with BLE,\n4 MB flash, button,\nstatus LED", "#0F766E")
    blk(46, 11, 20, 11, "Cell holder", "3 x AA, 4.5 V,\non/off switch", "#C2410C")
    blk(92, 28, 22, 14, "Phone app", "plots depth against\nblows; exports CSV", "#374151")
    wire([(25, 41.5), (40, 41.5), (46, 41.5)], "#7C3AED")
    lab(25.8, 46, "coiled 6-core cable,\ngland 1: 3.3 V, ground,\nHall out, SDA, SCL,\ninterrupt", "#7C3AED")
    wire([(25, 18.5), (36, 18.5), (36, 32), (46, 32)], "#2563EB")
    lab(26.5, 13.5, "4-core cable, gland 2:\n3.3 V, ground, SDA,\nSCL (own bus)", "#2563EB")
    wire([(56, 22), (56, 28)], "#B91C1C"); lab(57, 25, "0.5 mm², fused 1 A", "#B91C1C")
    wire([(66, 37), (92, 37)], "#6B7280", 1.2); ax.text(76.5, 38.6, "Bluetooth Low Energy", ha="center", fontsize=7.4, color=MUT)
    ax.text(41, 6.2, "Extra-low voltage only (4.5 V). No lithium cells. Screened cable; shields to ground at the logger end only.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps", "layouts", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps, "layouts": layouts, "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
