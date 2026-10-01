"""ConePro sizing calculations for CNP-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Every number quoted in docs/04-calcs/01-sizing.md is printed here with a tag such as [B3].
Geometry comes from cad/src/model.py (PARAMS, derived, build_parts); cost from bom/bom.csv;
budget from project.yaml. First-principles estimates with stated assumptions; not test data.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import ALU, PARAMS as P, STEEL, build_parts, derived  # noqa: E402

G = 9.81
D = derived(P)
RESULTS = []


def out(tag, text):
    print(f"[{tag}] {text}")


def req(rid, value, target, status):
    RESULTS.append((rid, value, target, status))


# ---------------------------------------------------------------- assumptions
A = {
    "guide_friction": 0.03,        # fraction of drop energy lost on the upper rod
    "e_restitution": (0.2, 0.4, 0.6),   # steel hammer on steel anvil with soil behind (low, nominal, high)
    "rod_loss": 0.05,              # rod wave and side friction, fraction of energy after impact
    "c_steel": 5190.0,             # m/s, bar wave speed
    "blow_period": (2.5, 3.5),     # s per blow, practiced and slow operator
    # draw-wire reel
    "counts": 4096, "inl_deg": 0.5, "cal_rule_mm": 0.2, "dT_K": 15.0, "alpha_al": 23e-6,
    "stretch_resid_mm": 0.10, "exit_resid_mm": 0.05,
    "wire_EA_N": 135000.0 * 0.095,  # N; 0.45 mm 7x7 steel, 0.095 mm^2 metal, 135 GPa strand modulus
    "spring_N": (3.0, 5.0),        # constant-force spring, retracted and extended
    "drum_Jr2_kg": 0.020,          # drum, magnet, shaft and spring inertia referred to the wire
    "eye_preload_N": 8.0, "eye_k_N_per_mm": 2.0,
    # tilt
    "tilt_resid_deg": 0.3,         # after 180 degree rotation zeroing; noise averaged over 0.5 s
    # shock
    "isolator_fn_Hz": 300.0, "part_rating_g": 10000.0,
    # magnets and Hall switch
    "Br_T": 1.3, "mag_d": 8.0, "mag_t": 4.0, "n_mag": 16, "mag_r": 41.0, "hall_op_mT": 6.0,
    # logger
    "record_B": 16, "header_B": 256, "max_blows": 300, "flash_MB": 4.0,
    "currents_mA": {"BLE microcontroller": 35.0, "angle sensor": 7.0, "Hall switch and LED": 5.0,
                    "accelerometer": 0.2, "flash, average": 3.0},
    "aa_mAh": 2000.0, "cold_derate": 0.5,
    # bought-part masses, kg
    "mass_bought": {"8 draw-wire reel and housing": 0.30, "10 sensor pad and band": 0.06,
                    "11 logger with 3 AA cells": 0.35, "12 coiled cable": 0.12,
                    "13 lightweight roll bag": 0.40, "14 hardware, cone cover, spare cone": 0.10,
                    "17 reel-to-logger cable and P-clips": 0.04},
    "extractor_kg": 3.0,
    "ext_rod_L": 500.0,            # optional extension rod, carried separately (DDR-002, R5)
}

# ---------------------------------------------------------------- A. geometry (R1)
out("A1", f"cone base {P['cone_d']:.0f} mm, included angle {P['cone_angle']:.0f} deg, point height {D['cone_h']:.1f} mm; "
          f"rod {P['rod_d']:.0f} mm")
parts = build_parts()
m_hammer = parts["hammer"][1].volume * STEEL
out("A2", f"hammer {P['hammer_od']:.0f} OD x {P['hammer_id']:.0f} bore x {D['hammer_L']:.1f} mm, model mass {m_hammer:.2f} kg")
out("A3", f"free drop from the model: {D['drop_check']:.1f} mm; upper rod {D['upper_L']:.0f} mm; assembled height {D['height']:.0f} mm")
req("R1", f"8.00 kg, {D['drop_check']:.0f} mm, 16 mm rod, 20 mm 60 deg cone [A1 to A3]",
    "ASTM D6951 geometry", "Met (nominal; tolerances to check against the standard)")

# ---------------------------------------------------------------- C. masses (R10), done first for the driven mass
masses = {}
dens = {"cone": STEEL, "lower_rod": STEEL, "anvil": STEEL, "hammer": STEEL, "upper_rod": STEEL, "handle": STEEL,
        "plate": ALU, "clamp": ALU}
bag = A["mass_bought"]["13 lightweight roll bag"]
for k, rho in dens.items():
    masses[f"{parts[k][2]} {parts[k][0]}"] = parts[k][1].volume * rho
masses.update(A["mass_bought"])
driven = sum(parts[k][1].volume * dens[k] for k in ("cone", "lower_rod", "anvil", "upper_rod", "handle", "clamp")) \
    + A["mass_bought"]["10 sensor pad and band"]

# ---------------------------------------------------------------- B. blow energy
M = P["hammer_mass"]
h = P["drop"] / 1000
E0 = M * G * h
v0 = math.sqrt(2 * G * h)
tf = math.sqrt(2 * h / G)
E1 = E0 * (1 - A["guide_friction"])
v1 = math.sqrt(2 * E1 / M)
out("B1", f"potential energy {E0:.1f} J; free-fall impact speed {v0:.2f} m/s; fall time {tf:.3f} s")
out("B2", f"after 3 % guide friction: {E1:.1f} J at {v1:.2f} m/s")
out("B3", f"driven mass (cone, rods, anvil, handle, clamp, pad) {driven:.2f} kg")
eta = {}
for e in A["e_restitution"]:
    eta[e] = (M + e ** 2 * driven) / (M + driven)
    vd = M * v1 * (1 + e) / (M + driven)
    Ec = E1 * eta[e] * (1 - A["rod_loss"])
    out("B4", f"e = {e:.1f}: impact efficiency {eta[e]:.3f}, rod velocity after impact {vd:.2f} m/s, energy at cone {Ec:.1f} J "
              f"({Ec / E0 * 100:.0f} % of {E0:.1f} J)")
e_n = A["e_restitution"][1]
v_rod = M * v1 * (1 + e_n) / (M + driven)
E_imp_in = E1 * eta[e_n]
E_cone = E_imp_in * (1 - A["rod_loss"])
out("B5", f"nominal flow: {E0:.1f} J drop, {E1:.1f} J at impact, {E_imp_in:.1f} J into rod, {E_cone:.1f} J at cone; "
          f"losses {E0 - E1:.1f}, {E1 - E_imp_in:.1f}, {E_imp_in - E_cone:.1f} J")
for p_mm in (2, 10, 15, 25):
    out("B6", f"mean dynamic soil resistance at {p_mm} mm per blow: {E_cone / (p_mm / 1000) / 1000:.1f} kN")

# ---------------------------------------------------------------- C. masses continued
out("C1", "part masses, kg: " + "; ".join(f"{k} {v:.2f}" for k, v in masses.items()))
total = sum(masses.values())
heavy = sum(parts[k][1].volume * STEEL for k in ("hammer", "upper_rod", "handle"))
out("C2", f"instrument as carried (items 1 to 14 and 17, bag and cells included): {total:.1f} kg; without the bag {total - bag:.1f} kg")
out("C3", f"heaviest piece, hammer captive on the upper rod with the handle: {heavy:.2f} kg; hammer alone {m_hammer:.2f} kg")
long_rod = P["lower_rod_L"] + D["z_rod"]
hammer_asm = D["height"] - D["z_anvil_top"]
out("C4", f"longest pieces: lower rod with cone {long_rod:.0f} mm; hammer assembly {hammer_asm:.0f} mm; plate {P['plate']:.0f} mm; "
          f"bag about 1,080 mm")
out("C5", f"optional extraction lever {A['extractor_kg']:.1f} kg, carried separately; kit with lever {total + A['extractor_kg']:.1f} kg")
clamp_st = parts["clamp"][1].volume * STEEL
plate8 = masses["7 Reference plate, slotted"] * 8.0 / P["plate_t"]
before = total + (0.80 - bag) + (clamp_st - masses["9 Anvil clamp and wire arm, aluminum"]) \
    + (plate8 - masses["7 Reference plate, slotted"])
out("C6", f"DDR-002 mass savings: 0.40 kg bag (was 0.80), aluminum clamp and arm "
          f"{masses['9 Anvil clamp and wire arm, aluminum']:.2f} kg (steel {clamp_st:.2f}), 6 mm plate "
          f"{masses['7 Reference plate, slotted']:.2f} kg (8 mm {plate8:.2f}); carried mass {before:.1f} kg before, {total:.1f} kg after")
ext_rod = math.pi / 4 * P["rod_d"] ** 2 * A["ext_rod_L"] * STEEL
out("C7", f"optional {A['ext_rod_L']:.0f} mm extension rod {ext_rod:.2f} kg, carried separately with the lever (DDR-002); "
          f"instrument plus both accessories {total + ext_rod + A['extractor_kg']:.1f} kg")
req("R10", f"{total:.1f} kg total, {heavy:.1f} kg heaviest, about 1.08 m packed [C2 to C4]",
    "16 kg, 10 kg, 1.1 m", "Met, thin margins" if total <= 16 and heavy <= 10 else "Not met")

# ---------------------------------------------------------------- D. penetration range (R5)
for k, v in D["limits"].items():
    out("D1", f"travel to contact, {k}: {v:.0f} mm")
out("D2", f"penetration range per lower rod {D['travel']:.0f} mm, limited by the {D['travel_by']}; "
          f"usable range set at 850 mm to keep the tilt error small (E4)")
req("R5", f"{D['travel']:.0f} mm stroke, 850 mm usable per rod [D1, D2]; optional extension rod in the BOM [C7]",
    "850 mm per rod; extension rod as a separate accessory", "Met (850 mm per rod; re-zero with the extension not verifiable)")

# ---------------------------------------------------------------- E. depth measurement (R2, R4)
circ = math.pi * P["drum_d"]
res = circ / A["counts"]
turns = 1000 / circ
out("E1", f"drum circumference {circ:.1f} mm per turn; resolution {res:.3f} mm per count; {turns:.1f} turns per 1,000 mm, "
          f"single layer at 1 mm groove pitch needs a {math.ceil(turns) + 1:.0f} mm wide drum")
wire_start = D["wire_start"]
stretch = [A["spring_N"][1] * wire_start / A["wire_EA_N"], A["spring_N"][0] * (wire_start - 850) / A["wire_EA_N"]]
budget = {"quantization": res / 2, "angle sensor nonlinearity": circ * A["inl_deg"] / 360,
          "scale calibration (steel rule)": A["cal_rule_mm"],
          "drum thermal expansion": 1000 * A["alpha_al"] * A["dT_K"],
          "wire stretch after calibration": A["stretch_resid_mm"], "exit eyelet geometry": A["exit_resid_mm"]}
worst = sum(budget.values())
rss = math.sqrt(sum(v * v for v in budget.values()))
out("E2", "bench error budget over 1,000 mm, vertical rod, mm: " + "; ".join(f"{k} {v:.2f}" for k, v in budget.items()))
out("E3", f"bench error: worst case +/-{worst:.2f} mm, RSS +/-{rss:.2f} mm; raw wire stretch {stretch[0]:.2f} mm at zero depth "
          f"(calibrated out); a printed plastic drum would add {1000 * 60e-6 * A['dT_K']:.1f} mm")


def wire_err(s, th, h0=wire_start):
    """Wire reading minus true penetration along the rod, mm, for a rod tilted th radians from zero."""
    L = math.hypot(h0 - s * math.cos(th), s * math.sin(th))
    return (h0 - L) - s


def corrected_err(s, th, dth, h0=wire_start):
    """Residual when the app solves for s using a tilt reading th + dth."""
    L = math.hypot(h0 - s * math.cos(th), s * math.sin(th))
    lo, hi = 0.0, 1000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        Lm = math.hypot(h0 - mid * math.cos(th + dth), mid * math.sin(th + dth))
        lo, hi = (mid, hi) if Lm > L else (lo, mid)
    return (lo + hi) / 2 - s


dth = math.radians(A["tilt_resid_deg"])
for deg in (1.0, 2.0, 5.0):
    th = math.radians(deg)
    out("E4", f"tilt {deg:.0f} deg: uncorrected wire error at 500 / 850 / {D['travel']:.0f} mm = "
              f"{wire_err(500, th):.2f} / {wire_err(850, th):.2f} / {wire_err(D['travel'] - 1, th):.1f} mm; "
              f"tilt-corrected with a {A['tilt_resid_deg']} deg reading error at 850 mm: {corrected_err(850, th, dth):.2f} mm")
e2_850 = abs(corrected_err(850, math.radians(2), dth))
req("R2", f"resolution {res:.3f} mm; bench +/-{worst:.2f} mm worst, +/-{rss:.2f} mm RSS; plus up to {e2_850:.1f} mm at 850 mm "
          f"with a 2 deg lean after tilt correction [E1 to E4]", "0.5 mm; +/-1 mm over 1,000 mm",
    "At risk: bench budget uses the whole +/-1 mm worst case")

# per-blow settle and wire slack
Fs = A["spring_N"][0]
a_w = Fs / A["drum_Jr2_kg"]
t_settle = 0.0
for p_mm in (2.0, 15.0, 50.0):
    p = p_mm / 1000
    t_r = 2 * p / v_rod
    a_r = v_rod / t_r
    dt, t, x_eye, x_w, v_w, slack_max = 1e-6, 0.0, 0.0, 0.0, 0.0, 0.0
    while True:
        t += dt
        x_eye = p if t >= t_r else v_rod * t - 0.5 * a_r * t * t
        v_w += a_w * dt
        x_w += v_w * dt
        slack_max = max(slack_max, x_eye - x_w)
        if x_w >= x_eye and t > t_r:
            break
    t_settle = max(t_settle, t)
    Ek = 0.5 * A["drum_Jr2_kg"] * v_w ** 2
    k_short = A["wire_EA_N"] / (wire_start - 850) * 1000
    F_hard = math.sqrt(2 * Ek * k_short)
    k2 = A["eye_k_N_per_mm"] * 1000
    x = (-A["eye_preload_N"] + math.sqrt(A["eye_preload_N"] ** 2 + 2 * k2 * Ek)) / k2
    F_soft = A["eye_preload_N"] + k2 * x
    out("E5", f"{p_mm:.0f} mm per blow: rod stops in {t_r * 1000:.1f} ms; peak wire slack {slack_max * 1000:.1f} mm; wire taut again "
              f"after {t * 1000:.1f} ms at {v_w:.2f} m/s; snap tension {F_hard:.0f} N with a rigid eye at 850 mm, "
              f"{F_soft:.0f} N with the preloaded eye spring")
out("E6", f"record written after a 0.2 s settle window (wire taut after at most {t_settle * 1000:.0f} ms, E5) plus 0.01 s at 100 Hz: 0.21 s")
req("R4", f"Depth settled within about {t_settle * 1000:.0f} ms; record at 0.21 s [E5, E6]", "Within 0.5 s of impact",
    "Met (calculation); firmware not written")

# CBR sensitivity
for dcp in (2, 5, 10, 15, 25, 50):
    out("E7", f"DCP {dcp} mm per blow: indicative CBR {292 / dcp ** 1.12:.0f} % (ASTM D6951 general correlation)")
for n, p_mm in ((10, 2.0), (25, 2.0)):
    span = n * p_mm
    out("E8", f"layer {span:.0f} mm ({n} blow{'s' if n > 1 else ''} at {p_mm:.0f} mm): DCP index error +/-{2 * rss / span * 100:.1f} % RSS "
              f"(+/-{2 * worst / span * 100:.1f} % worst), CBR +/-{1.12 * 2 * rss / span * 100:.1f} % RSS")
plate_area = (P["plate"] ** 2 - math.pi / 4 * P["plate_hole"] ** 2 - P["slot_w"] * P["plate"] / 2) / 1e6
plate_load = (masses["7 Reference plate, slotted"] + 0.30 + 0.35) * G
out("E9", f"plate bearing area {plate_area:.3f} m2; static bearing pressure {plate_load / plate_area / 1000:.2f} kPa; "
          f"settlement under blows not calculable from first principles")

# ---------------------------------------------------------------- F. blow detection (R3)
mu0 = 4e-7 * math.pi
Vm = math.pi / 4 * (A["mag_d"] / 1000) ** 2 * (A["mag_t"] / 1000)
mom = A["Br_T"] * Vm / mu0
zc = (P["pad_gap"] + P["mag_recess"] + A["mag_t"] / 2) / 1000   # magnets set 0.5 mm into the face (CNP-DDR-004)
R = A["mag_r"] / 1000


def bz(phi0):
    b = 0.0
    for i in range(A["n_mag"]):
        ph = 2 * math.pi * i / A["n_mag"] + phi0
        rx, ry, rz = R - R * math.cos(ph), -R * math.sin(ph), zc     # sensor at (R, 0, 0), magnets above
        r = math.sqrt(rx * rx + ry * ry + rz * rz)
        b += 1e-7 * mom * (3 * rz * rz / r ** 5 - 1 / r ** 3)
    return b * 1000


b_on, b_gap = bz(0.0), bz(math.pi / A["n_mag"])
lift = 0.030
b_lift = sum(1e-7 * mom * (3 * (zc + lift) ** 2 / ((2 * R * math.sin(math.pi * i / A['n_mag'])) ** 2 + (zc + lift) ** 2) ** 2.5
                           - 1 / ((2 * R * math.sin(math.pi * i / A['n_mag'])) ** 2 + (zc + lift) ** 2) ** 1.5)
             for i in range(A["n_mag"])) * 1000
out("F1", f"{A['n_mag']} magnets {A['mag_d']:.0f} x {A['mag_t']:.0f} mm on a {A['mag_r']:.0f} mm radius, Hall {P['pad_gap'] + P['mag_recess']:.1f} mm below the magnets, "
          f"0.5 mm inside the hammer face: {b_on:.0f} mT under a magnet, {b_gap:.0f} mT between magnets, {b_lift:.1f} mT with the hammer "
          f"lifted 30 mm; switch operate point {A['hall_op_mT']:.0f} mT (dipole model, steel hammer ignored)")
out("F2", f"minimum time between real blows: fall {tf:.2f} s plus lift; blow period {A['blow_period'][0]} to {A['blow_period'][1]} s; "
          f"count needs Hall arrival, accelerometer peak and a depth step or hold within 0.5 s")
req("R3", f"Hall margin {b_gap / A['hall_op_mT']:.1f}x at worst angle; three-signal logic [F1, F2, G3]",
    "Every blow, no false counts over 200 blows", "Not verifiable at TRL 3 (needs a bench sequence)")

# ---------------------------------------------------------------- G. shock (R11)
tc = 2 * D["hammer_L"] / 1000 / A["c_steel"]
for t_c in (tc, 2e-4):
    out("G1", f"anvil velocity step {v_rod:.2f} m/s in {t_c * 1e6:.0f} us: mean {v_rod / t_c / G:,.0f} g "
              f"(peaks about twice the mean)")
pk = v_rod * 2 * math.pi * A["isolator_fn_Hz"] / G
out("G2", f"pad on a {A['isolator_fn_Hz']:.0f} Hz elastomer isolator: peak about {pk:.0f} g "
          f"({A['part_rating_g'] / pk:.0f}x below the {A['part_rating_g']:,.0f} g part rating); static sag "
          f"{G / (2 * math.pi * A['isolator_fn_Hz']) ** 2 * 1e6:.1f} um")
h_short = h * 0.5 ** 2
out("G3", f"pad peak scales with the square root of drop: a 50 % threshold ({pk / 2:.0f} g) flags drops below "
          f"{h_short * 1000:.0f} mm as short")
req("R11", f"about {pk:.0f} g at the isolated pad vs {A['part_rating_g']:,.0f} g ratings; unisolated anvil "
           f"{v_rod / tc / G:,.0f} g mean [G1, G2]", "IP65, 0 to 45 C, 10,000 blows",
    "At risk: cable, connector and isolator fatigue not calculated")

# ---------------------------------------------------------------- H. tilt (R6)
out("H1", f"accelerometer tilt error after 180 deg rotation zeroing: +/-{A['tilt_resid_deg']} deg; warning at 5 deg trips "
          f"between {5 - A['tilt_resid_deg']:.1f} and {5 + A['tilt_resid_deg']:.1f} deg; bubble level as backup")
req("R6", f"+/-{A['tilt_resid_deg']} deg tilt reading, warning at 5 deg [H1]", "Warn above 5 deg",
    "Met by design (D1); bench check later")

# ---------------------------------------------------------------- I. data (R7, R8, R14)
test_B = A["header_B"] + A["record_B"] * A["max_blows"]
n_tests = A["flash_MB"] * 1024 * 1024 / test_B
out("I1", f"test record {test_B / 1024:.1f} KiB at {A['max_blows']} blows; {A['flash_MB']:.0f} MB flash holds {n_tests:.0f} tests")
req("R8", f"{n_tests:.0f} tests stored [I1]", "50 tests offline", "Met (calculation)")
req("R7", "App specified in CNP-PRC-001; not written", "Live plot, DCP index, CBR, CSV", "Not verifiable at TRL 3")
req("R14", "App wording specified in CNP-PRC-001", "Correlation and limits stated", "Not verifiable at TRL 3")

# ---------------------------------------------------------------- J. test time (R9)
blows = round(850 / 15)
for name, setup, per, stroke_s, pack in (("practiced", 2.5, A["blow_period"][0], 6.0, 1.0),
                                         ("slow", 3.0, A["blow_period"][1], 12.0, 1.5)):
    drive = blows * per / 60
    extr = 0.5 + (850 / 50) * stroke_s / 60
    out("J1", f"{name}: setup {setup} min, {blows} blows {drive:.1f} min, extraction {extr:.1f} min "
              f"(50 mm per lever stroke), pack {pack} min: {setup + drive + extr + pack:.1f} min")
    if name == "slow":
        t_slow = setup + drive + extr + pack
    else:
        t_fast = setup + drive + extr + pack
for p_mm in (15, 5):
    Fx = E_cone / (p_mm / 1000) / 1000
    out("J2", f"upper bound on extraction force, the dynamic tip resistance: {Fx:.1f} kN at {p_mm} mm per blow; the 10:1 "
              f"lever with 300 N at the hand gives 3.0 kN; one person pulling gives about 0.4 kN")
req("R9", f"{t_fast:.1f} to {t_slow:.1f} min [J1]", "12 min or less", "Met (estimate), thin in the slow case")

# ---------------------------------------------------------------- K. power (R12)
I = sum(A["currents_mA"].values())
life = A["aa_mAh"] / I
out("K1", "currents, mA: " + "; ".join(f"{k} {v}" for k, v in A["currents_mA"].items()) + f"; total {I:.1f} mA")
out("K2", f"battery life {life:.0f} h at 20 C; {life * A['cold_derate']:.0f} h at 0 C with half capacity")
req("R12", f"{life:.0f} h, {life * A['cold_derate']:.0f} h at 0 C [K2]", "8 h on non-lithium cells", "Met (calculation)")

# ---------------------------------------------------------------- L. cost (R13)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
inst = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if "Optional" not in r["notes"])
opt = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if "Optional" in r["notes"])
budget_usd = yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"]
out("L1", f"BOM {len(rows)} lines, all priced; instrument (lines 1 to 14 and 17) ${inst:.0f}; optional accessories (lever, extension rod) "
          f"${opt:.0f}; kit with accessories ${inst + opt:.0f}; budget ${budget_usd}")
req("R13", f"${inst:.0f} instrument; ${inst + opt:.0f} with the optional lever and extension rod [L1]", f"${budget_usd} or less", "Met")

# ---------------------------------------------------------------- M. retrofit fit (R15)
out("M1", f"sensor set interfaces: clamp collar bore {P['rod_d']:.0f} mm; band clamp 50 to 80 mm anvils; pad top "
          f"{P['pad_gap']:.0f} mm below the anvil top; plate hole {P['plate_hole']:.0f} mm passes the {P['cone_d']:.0f} mm cone")
req("R15", "Interfaces sized for 16 mm rods and 50 to 80 mm anvils [M1]", "Fits standard DCPs without machining",
    "Not verifiable at TRL 3 (needs a commercial DCP)")

# ---------------------------------------------------------------- results table
print("\nRequirement results")
order = {"Not met": 0, "At risk": 1}
for rid, val, tgt, st in sorted(RESULTS, key=lambda r: (min((v for k, v in order.items() if r[3].startswith(k)), default=2),
                                                       int(r[0][1:]))):
    print(f"  {rid:<4} {st:<55} {val}  (target: {tgt})")
counts = {}
for r in RESULTS:
    key = "Not met" if r[3].startswith("Not met") else "At risk" if r[3].startswith("At risk") else \
        "Not verifiable" if r[3].startswith("Not verifiable") else "Met"
    counts[key] = counts.get(key, 0) + 1
print("  counts:", counts)
