"""ConePro general arrangement sheet CNP-DWG-001, Rev P5 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CNP-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from the model and PARAMS, so
they follow any parameter change. The concept sheet in media/ is CNP-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _t, _viewbox, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, derived  # noqa: E402

DATE = "2026-09-25"
SETUPS = {"front": ((0, -1, 0), (0, 0, 1)), "top": ((0, 0, 1), (0, 1, 0)),
          "right": ((1, 0, 0), (0, 0, 1)), "iso": ((1, -1, 0.8), (0, 0, 1))}


def views_of(shape, workdir, names=("front", "top", "right", "iso"), line_weight=0.35):
    """Project a shape like drawing.project_views, edge by edge so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = shape.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    out = {}
    for name in names:
        (dx, dy, dz), up = SETUPS[name]
        vis, hid = shape.project_to_viewport((c.X + dx * d, c.Y + dy * d, c.Z + dz * d), up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", vis), ("Hidden", hid if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    from build123d import Box, Compound, Pos
    D = derived(P)
    parts = build_parts()
    work = ROOT / "cad" / "drawings" / "_views"
    asm = Compound(children=[v[1] for v in parts.values()])
    bb = asm.bounding_box()
    views = views_of(asm, work)
    s = Sheet(project="ConePro", title="General arrangement", dwg_no="CNP-DWG-001", rev="P5",
              author="Amish Chadha", date="2026-09-30", scale=1 / 20, theme="technical",
              material="Steel rods, anvil, hammer; aluminum plate and clamp; parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "6 mm plate, aluminum clamp, 15.7 kg (CNP-DDR-002)", DATE, "AC"),
                         ("P3", "Reel housing 72 x 60 x 72 round the 60 mm drum; stroke 928 (CNP-DDR-003)", "2026-09-27", "AC"),
                         ("P4", "Layout and labels tidied", "2026-09-30", "AC"),
                         ("P5", "Design for construction: joints, clamp, reel, cables (CNP-DDR-004)", "2026-09-30", "AC")])
    s.add_ortho(views, dims=False)
    k = s.scale
    c = ortho_cells(s, views)
    L = []

    # front view (from -Y): X right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    L += [ext(X(0) - 1, Z(bb.max.Z), x - 27, Z(bb.max.Z)), ext(X(0) - 1, Z(0), x - 27, Z(0))]
    L += dim_v(x - 25, Z(bb.max.Z), Z(0), f"{bb.size.Z:,.0f} overall")
    L += [ext(X(0) - 1, Z(D["z_anvil_top"]), x - 12, Z(D["z_anvil_top"])), ext(X(0) - 1, Z(D["z_stop"]), x - 12, Z(D["z_stop"]))]
    L += dim_v(x - 11, Z(D["z_stop"]), Z(D["z_anvil_top"]), f"{D['upper_free']:.0f} = {D['hammer_L']:.0f} + {P['drop']:.0f} drop")
    L += [ext(X(0) - 1, Z(D["z_rod"]), x - 19, Z(D["z_rod"])), ext(X(0) - 1, Z(D["z_anvil"]), x - 19, Z(D["z_anvil"]))]
    L += dim_v(x - 18, Z(D["z_anvil"]), Z(D["z_rod"]), f"{P['lower_rod_L']:,.0f} lower rod")
    rx = P["reel_xy"][0]
    xr, yr, wr, hr = c["right"]
    L += [ext(xr + wr / 2 + 3, Z(D["arm_under"]), xr + wr + 10, Z(D["arm_under"])), ext(xr + wr / 2 + 3, Z(D["reel_top"]), xr + wr + 10, Z(D["reel_top"]))]
    L += dim_v(xr + wr + 8, Z(D["arm_under"]), Z(D["reel_top"]), "", side=1)
    cxs, cys = xr + wr + 8 + 2.6, (Z(D["arm_under"]) + Z(D["reel_top"])) / 2
    stroke_txt = f"{D['travel']:.0f} stroke (850 usable)"
    L.append(f'<g transform="rotate(-90 {cxs:.2f} {cys:.2f})">{_t(cxs, cys, stroke_txt, 2.1, 400, INK, "middle", mono=True)}</g>')

    # top view (from +Z): X right, Y up the sheet
    x, y, w, h = c["top"]
    L += dim_h(x, x + w, y - 3, f"{P['plate']:.0f} plate")
    L += [ext(x, y, x - 5, y), ext(x, y + h, x - 5, y + h)]
    L += dim_v(x - 4, y, y + h, f"{P['plate']:.0f}")

    # detail A: anvil, sensor pad and clamp, front view at 1:5
    z0, z1 = D["z_anvil"] - 60, D["z_anvil_top"] + 60
    box = Pos(20, 0, (z0 + z1) / 2) * Box(260, 200, z1 - z0)
    keep = ["lower_rod", "anvil", "hammer", "upper_rod", "clamp", "pad", "drawwire", "cable"]
    det = Compound(children=[parts[kk][1] & box for kk in keep])
    dv = views_of(det, work / "detail", names=("front",))
    kd = 0.2
    dvw, dvh = _viewbox(Path(dv["front"]).read_text())[2:]
    dx, dy = 222.0, 110.0
    s.add_svg(dv["front"], dx, dy, scale=kd, label="Detail A: anvil, sensor pad and clamp", sublabel="Front view, scale 1:5")
    dbb = det.bounding_box()
    Xd = lambda mx: dx + (mx - dbb.min.X) * kd
    Zd = lambda mz: dy + dvh * kd - (mz - dbb.min.Z) * kd
    pad_top = D["z_anvil_top"] - P["pad_gap"]
    gx, gy = Xd(-P["anvil_d"] / 2 - P["pad"][0] / 2), Zd(pad_top) - 0.8
    L += [ext(gx, gy, gx - 14, gy - 10), ext(gx - 14, gy - 10, gx - 16, gy - 10),
          f'<circle cx="{gx:.2f}" cy="{gy:.2f}" r="0.5" fill="{INK}"/>']
    L.append(_t(gx - 17, gy - 9.2, f"{P['pad_gap']:.0f} gap, pad to hammer face", 2.2, 400, INK, "end", mono=True))
    L += dim_h(Xd(0), Xd(rx), Zd(D["arm_under"]) + 7, "")[:3]
    L.append(_t(Xd(rx) + 1.8, Zd(D["arm_under"]) + 7.8, f"{rx:.0f} rod to wire", 2.1, 400, INK, "start", mono=True))
    L += dim_h(Xd(-P["hammer_od"] / 2), Xd(P["hammer_od"] / 2), Zd(dbb.max.Z) - 3, f"{P['hammer_od']:.0f} hammer, 8.0 kg")

    s._layers += L
    s.add_svg(views["iso"], 282, 44, 134, 76, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"ASTM D6951: {P['hammer_mass']:.1f} kg hammer, {P['drop']:.0f} drop, {P['rod_d']:.0f} rod, "
        f"{P['cone_d']:.0f} cone at {P['cone_angle']:.0f} deg",
        f"Hammer {P['hammer_od']:.0f} OD x {P['hammer_id']:.0f} bore x {D['hammer_L']:.1f}; anvil {P['anvil_d']:.0f} x {P['anvil_h']:.0f}",
        f"Upper rod {D['upper_L']:.0f}; stop collar {P['stop_d']:.0f} x {P['stop_h']:.0f}; T-handle {P['handle_w']:.0f} wide",
        f"Plate {P['plate']:.0f} x {P['plate']:.0f} x {P['plate_t']:.0f} Al; {P['plate_hole']:.0f} hole, {P['slot_w']:.0f} slot",
        f"Draw-wire exit at X {P['reel_xy'][0]:.0f}, Y {P['reel_xy'][1]:.0f}; {P['drum_d']:.0f} grooved drum, single layer",
        f"One-piece aluminum clamp, {P['collar_d']:.0f} collar against the anvil underside; M12 rod joints",
        f"Sensor pad on a band clamp (50 to 80 anvils), {P['pad_gap']:.0f} below anvil top",
        f"Stroke {D['travel']:.0f}, limited by the {D['travel_by']}",
        "About 15.7 kg with bag; heaviest piece 9.8 kg (CNP-CAL-001 v0.4)",
        "Third-angle; front view from -Y; ground at Z 0",
    ], x=282, y=138, width=134)
    out = s.save(ROOT / "cad" / "drawings" / "CNP-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
