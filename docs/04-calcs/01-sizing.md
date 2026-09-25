---
doc_id: CNP-CAL-001
title: ConePro sizing calculations
project: ConePro
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (geometry, blow energy, mass, range, depth error, wire dynamics, blow detection, shock, tilt, data, time, power, cost)
---

# ConePro sizing calculations

On paper, ConePro meets seven of its fifteen requirements, has two at risk, misses two and has four that cannot be verified at TRL 3. The two misses are mass and range. Carried in its bag, the instrument weighs about 16.7 kg against the 16 kg target (R10), and the BOM has no extension rod, so the 1,000 mm clause of R5 is not met (850 mm per rod is). The two at risk are depth accuracy (R2), where the bench error budget uses the whole ±1 mm and rod lean adds more near the end of the stroke, and shock survival (R11), where the isolated sensor pad sees about 530 g but cable and connector fatigue are not calculated. The calculations also corrected two TRL 2 estimates: about 28 J, not 33 J, reaches the cone, and the impact at the anvil is thousands of g, not hundreds. They also found that the draw-wire goes slack for a few milliseconds after each blow, which the reel design must allow for. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They are not test data and do not show that any part is safe to use. ConePro drops an 8 kg hammer about 45 J per blow onto a steel anvil and drives a steel rod into the ground; utility locates, eye and hearing protection and the precautions in CNP-PRC-001, Safety, apply to any use.

## Scope and method

The note checks every requirement in CNP-REQ-001 v0.3 against the design in CNP-PRC-001 v0.3, the decisions in CNP-DDR-001 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and solids, so the masses, travel limits and interfaces used here are those in the STEP files and in drawing CNP-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The reference test is the one in CNP-REQ-001: one test point driven to 850 mm in a medium-stiff soil at about 15 mm per blow (57 blows), by one person, on level ground.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Materials | Steel 7,850 kg/m³, aluminum 2,700 kg/m³ applied to the model solids; bought parts from typical catalog masses (Table 3) | To confirm by weighing |
| Blow | Guide friction 3 % of the drop energy; coefficient of restitution 0.4 (range 0.2 to 0.6) between hammer and anvil; rod wave and side friction 5 % | Assumed; the restitution sets the largest loss and is not measured |
| Operator | One blow every 2.5 s (practiced) to 3.5 s (slow) | As at TRL 2 |
| Draw-wire | 60 mm grooved aluminum drum, single layer; 12-bit angle sensor with ±0.5° nonlinearity; scale calibrated once against a steel rule read to ±0.2 mm; ±15 K from the calibration temperature; 0.45 mm 7x7 steel wire, axial stiffness 12.8 kN; constant-force spring 3 N retracted to 5 N extended; drum inertia equal to 20 g at the wire | Typical low-cost parts; to confirm from datasheets |
| Tilt | Accelerometer offset removed by a 180° rotation of the rod at setup; residual ±0.3° | Typical MEMS offsets and noise, averaged over 0.5 s |
| Shock | Hammer contact time from 2L/c = 53 µs to 0.2 ms; pad on a 300 Hz elastomer isolator; Hall switch and accelerometer rated 10,000 g | Typical MEMS and IC shock ratings; to confirm from datasheets |
| Magnets | Sixteen 8 x 4 mm N42 disks (Br 1.3 T) on a 41 mm radius in the hammer face; Hall switch operate point 6 mT; dipole model with the steel hammer ignored | The steel body will change the field; bench check later |
| Logger | 16 bytes per blow, 256 bytes per test header, up to 300 blows per test, 4 MB flash; average current 50.2 mA; 2,000 mAh from three AA alkaline cells, halved at 0 °C | As at TRL 2 plus the accelerometer |

## A. Geometry (R1)

The model builds the ASTM D6951 geometry from its parameters: a 20 mm cone with a 60° point (17.3 mm tall) on a 16 mm rod [A1], and a 100 mm OD, 22 mm bore hammer whose length, 136.4 mm, is derived from the 8.0 kg target [A2]. The upper rod length follows from the drop: the model's free drop from anvil top to stop collar is 575.0 mm, the upper rod is 729 mm and the instrument stands 1,867 mm tall [A3]. The nominal geometry therefore meets R1; the tolerances in the standard are still to be checked against a copy of it.

## B. Blow energy

The hammer stores 45.1 J at the top of its drop, reaches 3.36 m/s at impact and falls in 0.342 s [B1]. After 3 % guide friction it lands with 43.8 J [B2]. The driven mass (cone, both rods, anvil, handle, clamp and pad) is 5.35 kg [B3]. With the Hiley impact efficiency (M + e²m) / (M + m), a restitution of 0.4 gives an efficiency of 0.663, a rod velocity after impact of 2.78 m/s and about 27.6 J at the cone, 61 % of the drop energy; the range for e = 0.2 to 0.6 is 25.6 to 30.9 J [B4]. The TRL 2 figure of 33 J assumed a 20 % impact loss; the calculation gives about 34 % [B5], and Figure 2 of CNP-PRC-001 is updated to match.

This does not change the indicative CBR, because the ASTM D6951 correlations are empirical for the standard apparatus. It does change the mean dynamic soil resistance: about 1.8 kN at 15 mm per blow and 13.8 kN at 2 mm per blow [B6].

## C. Mass and packing (R10)

*Table 2. Mass by part [C1].*

| Part | Mass (kg) | Source |
| --- | --- | --- |
| 1 Cone | 0.03 | Model |
| 2 Lower drive rod | 1.58 | Model |
| 3 Anvil and coupler | 1.52 | Model |
| 4 Drop hammer | 8.00 | Model |
| 5 Upper rod | 1.15 | Model |
| 6 Handle, stop and level | 0.67 | Model |
| 7 Reference plate | 1.72 | Model |
| 9 Clamp and arm (steel) | 0.34 | Model |
| 8 Draw-wire reel; 10 pad; 11 logger with cells; 12 cable | 0.30; 0.06; 0.35; 0.12 | Catalog estimates |
| 13 Canvas roll bag; 14 hardware and spare cone | 0.80; 0.08 | Catalog estimates |

The instrument as carried, in its bag with cells, weighs about 16.7 kg; without the bag it is 15.9 kg [C2]. The TRL 2 estimate of 15.2 kg left out the bag and underestimated the anvil and handle. **R10 is not met** by about 0.7 kg. The heaviest piece, the hammer captive on the upper rod with the handle, is 9.82 kg, and the hammer alone is 8.00 kg [C3], so the 10 kg limit is met. The longest piece is the lower rod with the cone, 1,022 mm, which fits a bag about 1.08 m long [C4]. The optional extraction lever adds 3.0 kg carried separately [C5].

One way to meet R10, proposed in `docs/REVIEW.md`, is a 0.40 kg bag, an aluminum clamp and arm (0.12 kg) and a 6 mm plate (1.29 kg), which together give 15.7 kg [C6].

## D. Penetration range (R5)

As the rod goes down, the first contact is the wire arm landing on the reel housing after 938 mm; the clamp collar would reach the plate at 988 mm and the anvil at 1,014 mm [D1]. The usable range is set at 850 mm, because the tilt error in section E grows quickly as the wire gets short [D2]. That meets the 850 mm clause of R5. A 1,000 mm test needs an extension rod, which is not in the BOM, so **the 1,000 mm clause of R5 is not met**. A 500 mm extension rod weighs 0.79 kg and would take the carried mass to 17.5 kg, or 16.4 kg with the section C savings [C7]. Automatic re-zero after adding a rod is a firmware function and is not verifiable at TRL 3.

## E. Depth measurement (R2, R4)

**Resolution.** The drum pays out 188.5 mm per turn, so a 12-bit sensor resolves 0.046 mm per count. A 1,000 mm stroke is 5.3 turns, which fits in a single layer on a 7 mm wide grooved drum [E1]. A single layer matters: each extra layer of wire would add about 1.5 % to the effective diameter.

**Bench error, vertical rod.** Table 3 lists the error sources over 1,000 mm after one scale calibration against the engraved rod or a steel rule [E2].

*Table 3. Draw-wire error budget over 1,000 mm, vertical rod [E2], [E3].*

| Source | Error (mm) |
| --- | --- |
| Quantization | ±0.02 |
| Angle sensor nonlinearity (±0.5° of a 188.5 mm turn) | ±0.26 |
| Scale calibration against a steel rule | ±0.20 |
| Drum thermal expansion, aluminum, ±15 K | ±0.34 |
| Wire stretch left after calibration | ±0.10 |
| Exit eyelet geometry | ±0.05 |
| **Worst case; root sum square** | **±0.98; ±0.49** |

The worst case uses the whole ±1 mm allowance of R2, so **R2 is at risk**. The raw wire stretch, 0.37 mm at zero depth, is mostly removed by the calibration. A printed plastic drum would add about 0.9 mm of thermal error, so the drum must be metal [E3].

**Rod lean in the field.** If the rod leans, the arm eye moves sideways over the reel and the wire reads short, most of all near the end of the stroke where the wire is short. At 1° of lean the uncorrected error is 0.16 mm at 500 mm, 1.36 mm at 850 mm and 15.4 mm at the full 938 mm; at 2° it is 5.34 mm at 850 mm [E4]. The app can correct for the lean using the tilt reading (D1), but a ±0.3° tilt error still leaves 0.96 mm at 1° and 1.81 mm at 2° at 850 mm [E4]. This is why the usable range stops at 850 mm, and why the depth accuracy in stiff layers near the end of a rod is weaker than the bench budget.

**Wire slack after each blow.** The rod starts down at 2.78 m/s and stops within 1.4 ms at 2 mm per blow, 10.8 ms at 15 mm per blow and 36 ms at 50 mm per blow. The spring cannot rewind the drum that fast, so the wire goes slack by up to 1.9, 9.5 and 17.0 mm and becomes taut again after 5.2 to 36 ms [E5]. Two consequences follow. First, the reel needs a groove keeper so slack wire cannot jump the groove and break the single-layer assumption. Second, when the wire snaps taut the drum stops suddenly: with a rigid eye the peak wire tension would be 42 to 291 N at 850 mm, near or above the breaking load of a 0.45 mm wire. A preloaded spring at the arm eye (8 N preload, 2 N/mm) limits the peak to 9 to 35 N, and because the spring stays on its stop under the 3 to 5 N reel force it adds no reading error [E5]. Both details are in BOM line 8 and are listed for review in `docs/REVIEW.md`.

**Record latency (R4).** The depth is settled at most 36 ms after impact, so a 0.2 s settle window plus one 100 Hz sample records each blow 0.21 s after impact, inside the 0.5 s of R4 [E6].

**What the error means for the user.** Table 4 repeats the ASTM D6951 general correlation, CBR = 292 / DCP^1.12 [E7]. With the ±0.49 mm root-sum-square error at each end of an interval, the DCP index over 10 blows at 2 mm per blow is good to ±4.9 % (±9.8 % worst case) and the CBR to ±5.5 %; over a 50 mm stiff layer the DCP index is good to ±2.0 % [E8].

*Table 4. Indicative CBR from the ASTM D6951 general correlation [E7].*

| DCP index (mm per blow) | 2 | 5 | 10 | 15 | 25 | 50 |
| --- | --- | --- | --- | --- | --- | --- |
| Indicative CBR (%) | 134 | 48 | 22 | 14 | 8 | 4 |

**Plate settlement.** The plate, reel and logger press on 0.078 m² of ground at only 0.30 kPa, so static settlement is negligible. Settlement or heave caused by the blows cannot be calculated from first principles [E9]; it is left as an open question.

## F. Blow detection (R3)

With sixteen magnets in the hammer face and the Hall switch 8 mm below it, the dipole model gives 39 mT under a magnet and 14 mT between magnets, 2.3 times the 6 mT operate point at the worst angle; with the hammer lifted 30 mm the field falls to 1.7 mT, so the switch releases [F1]. A blow is counted only when the Hall switch sees the hammer arrive, the accelerometer sees an impact peak and the depth steps down or holds within 0.5 s [F2]. The accelerometer peak also flags short drops (section G). The logic is sound on paper, but "every blow and no false counts over 200 blows" can only be shown on a bench, so R3 is not verifiable at TRL 3. The steel hammer body will change the field and must be checked by measurement.

## G. Shock (R11)

The anvil and rods take a 2.78 m/s velocity step in 53 µs to 0.2 ms, a mean acceleration of about 1,400 to 5,400 g with peaks about twice that [G1]. The TRL 2 estimate of hundreds to a few thousand g was low. A sensor pad rigidly fixed to the anvil would be near the 10,000 g rating of typical MEMS accelerometers and Hall ICs. On a 300 Hz elastomer isolator, the pad sees about 533 g, 19 times below that rating, and sags only 2.8 µm under gravity, so the tilt reading is not affected [G2]. Because the pad peak scales with the square root of the drop height, a threshold at half the full-drop peak (267 g) flags drops below 144 mm as short [G3]. **R11 stays at risk**: fatigue of the isolator, the coiled cable and the connector over 10,000 blows is not calculated, and IP65 sealing and the 0 to 45 °C range can only be shown by test.

## H. Tilt (R6)

After zeroing by turning the rod 180° at setup, the accelerometer reads tilt to about ±0.3°, so the 5° warning trips between 4.7° and 5.3° [H1]. With the bubble level as a backup, R6 is met by design (D1).

## I. Data (R7, R8, R14)

A 300-blow test takes 4.9 KiB, so 4 MB of flash holds about 830 tests, well over the 50 of R8 [I1]. R7 (app output) and R14 (honest results wording) are specified in CNP-PRC-001 but the app is not written, so they are not verifiable at TRL 3.

## J. Test time and extraction (R9)

A practiced operator takes about 8.1 min for the reference test (setup 2.5 min, 57 blows 2.4 min, lever extraction 2.2 min at 50 mm per stroke, packing 1.0 min); a slow operator takes about 11.7 min [J1]. R9 is met by estimate, with a thin margin in the slow case. The extraction force is bounded above by the dynamic tip resistance: about 1.8 kN at 15 mm per blow, within the 3.0 kN of the 10:1 lever with 300 N at the hand, but 5.5 kN at 5 mm per blow, beyond it [J2]. The real pull force is expected to be lower because the cone rises through the hole it made, but in stiff ground a disposable cone may be needed. One person pulling by hand gives only about 0.4 kN, which is why the lever (D2) is needed at all.

## K. Power (R12)

The average current is 50.2 mA (microcontroller 35, angle sensor 7, Hall switch and LED 5, flash 3, accelerometer 0.2) [K1], so three AA alkaline cells last about 40 h at 20 °C and about 20 h at 0 °C [K2], well above the 8 h of R12.

## L. Cost (R13)

All 15 BOM lines are priced. The instrument (lines 1 to 14) costs $321 and the optional extraction lever $50, $371 together, against the $400 budget [L1]. R13 is met. Prices are indicative and were not quoted by suppliers.

## M. Retrofit fit (R15)

The sensor set clamps to a 16 mm rod, straps to any 50 to 80 mm anvil, sits 8 mm below the anvil top and passes the 20 mm cone through the 60 mm plate hole [M1]. Fit to commercial penetrometers needs one in hand, so R15 is not verifiable at TRL 3.

## Results

*Table 5. Requirement results, not met and at risk first.*

| ID | Value (calculation tag) | Target | Status |
| --- | --- | --- | --- |
| R5 | 938 mm stroke, 850 mm usable; no extension rod [D1, D2] | 850 mm per rod; 1,000 mm with an extension rod and re-zero | **Not met** (1,000 mm clause) |
| R10 | 16.7 kg carried, 9.8 kg heaviest piece, about 1.08 m packed [C2 to C4] | 16 kg; 10 kg; 1.1 m | **Not met** (total mass) |
| R2 | 0.046 mm resolution; bench ±0.98 mm worst, ±0.49 mm RSS; up to 1.8 mm more at 850 mm with a 2° lean [E1 to E4] | 0.5 mm; ±1 mm over 1,000 mm | At risk |
| R11 | About 533 g at the isolated pad; 1,400 to 5,400 g mean at the anvil [G1, G2] | IP65; 0 to 45 °C; 10,000 blows | At risk |
| R1 | 8.00 kg, 575 mm drop, 16 mm rod, 20 mm 60° cone [A1 to A3] | ASTM D6951 geometry | Met (nominal) |
| R4 | Settled within 36 ms; record at 0.21 s [E5, E6] | Within 0.5 s | Met |
| R6 | ±0.3° tilt reading; warning at 5° [H1] | Warn above 5° | Met by design |
| R8 | About 830 tests stored [I1] | 50 tests | Met |
| R9 | 8.1 to 11.7 min [J1] | 12 min or less | Met (estimate, thin) |
| R12 | 40 h; 20 h at 0 °C [K2] | 8 h, non-lithium | Met |
| R13 | $321 instrument; $371 with the lever [L1] | $400 or less | Met |
| R3 | Hall margin 2.3 times; three-signal logic [F1, F2] | Every blow, no false counts in 200 | Not verifiable at TRL 3 |
| R7 | App specified, not written | Plot, DCP index, CBR, CSV | Not verifiable at TRL 3 |
| R14 | App wording specified, not written | Correlation and limits stated | Not verifiable at TRL 3 |
| R15 | Interfaces for 16 mm rods and 50 to 80 mm anvils [M1] | Fits standard DCPs without machining | Not verifiable at TRL 3 |

Counts: 7 met, 2 at risk, 2 not met, 4 not verifiable at TRL 3.

## Checks against earlier figures

- Energy at the cone: TRL 2 said about 33 J (74 %); this note gives 27.6 J (61 %) [B5]. CNP-PRC-001 and the flow diagram are corrected.
- Anvil shock: TRL 2 said hundreds to a few thousand g; this note gives about 1,400 to 5,400 g mean at the anvil and about 530 g at an isolated pad [G1, G2]. Corrected.
- Total mass: TRL 2 said about 15.2 kg; this note gives 15.9 kg without the bag and 16.7 kg with it [C2]. Corrected, and R10 is now not met.
- Penetration per rod: TRL 2 said about 850 mm; the model's stroke is 938 mm with 850 mm usable [D2]. Consistent.
- Cost: TRL 2 said about $296; the updated BOM is $321 [L1]. Corrected.
- Resolution 0.046 mm, fall time 0.342 s, impact speed 3.36 m/s, battery life about 40 h and the CBR table are unchanged [B1], [E1], [E7], [K2].
