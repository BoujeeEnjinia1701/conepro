---
doc_id: CNP-CAL-001
title: ConePro sizing calculations
project: ConePro
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (geometry, blow energy, mass, range, depth error, wire dynamics, blow detection, shock, tilt, data, time, power, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); rerun for the 6 mm plate, aluminum clamp, lighter bag and optional extension rod; R5 and R10 now met
- version: "0.3"
  date: '2026-09-27'
  author: Amish Chadha
  change: Reel housing grown to 72 x 60 x 72 mm round the 60 mm drum (CNP-DDR-003, decided by Amish on 2026-09-27); rerun; stroke 940 to 928 mm, 850 mm usable range still met; tilt error at 850 mm slightly larger
- version: "0.4"
  date: '2026-09-30'
  author: Amish Chadha
  change: Rerun for the design for construction (CNP-DDR-004); M12 rod joints and 12 mm cone shoulder, one-piece clamp against the anvil, reel cable added; stroke 939 mm, height 1,874 mm, instrument $335; no requirement changes status
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Rerun for Amish's decisions of 2026-10-02: hammer grip grooves (hammer 138.0 mm long to keep 8.00 kg), rubber grips on the T-handle, end cap for the upper rod, spanner flats on the rod joints; heaviest piece 9.96 kg, carried mass 15.8 kg, instrument $346; no requirement changes status"
---

# ConePro sizing calculations

On paper, ConePro meets nine of its fifteen requirements, has two at risk and has four that cannot be verified at TRL 3; none is now not met. Version 0.2 applies Amish's decisions in CNP-DDR-002: a 6 mm plate, an aluminum clamp and arm and a 0.40 kg bag bring the carried mass from 16.7 kg to 15.7 kg, so R10 is met with a thin margin, and R5 is restated as 850 mm per rod with a 500 mm extension rod as a separately carried accessory, so R5 is met. Version 0.3 applies Amish's 2026-09-27 decision in CNP-DDR-003: the reel housing grows to 72 x 60 x 72 mm round the 60 mm drum, the stroke falls from 940 mm to 928 mm and the 850 mm usable range still holds. Version 0.4 reruns the note for the design for construction (CNP-DDR-004, made under Amish's 2026-09-30 instruction to make the design physically buildable): the threaded rod joints, the longer cone shoulder and the clamp moved up against the anvil raise the stroke to 939 mm, the instrument now costs $335 with the added reel cable and fixings, and no requirement changes status. Version 0.6 applies Amish's decisions of 2026-10-02: grip grooves on the hammer (now 138.0 mm long to keep 8.00 kg), 33 mm rubber grips on the T-handle, a screw-on end cap for the upper rod's stud and spanner flats instead of thread locker on the rod joints. The heaviest piece rises to 9.96 kg, 0.04 kg under the 10 kg limit, the carried mass to 15.8 kg and the instrument cost to $346; no requirement changes status. The two at risk are depth accuracy (R2), where the bench error budget uses the whole ±1 mm and rod lean adds more near the end of the stroke, and shock survival (R11), where the isolated sensor pad sees about 540 g but cable and connector fatigue are not calculated. The calculations also corrected two TRL 2 estimates: about 28 J, not 33 J, reaches the cone, and the impact at the anvil is thousands of g, not hundreds. They also found that the draw-wire goes slack for a few milliseconds after each blow, which the reel design must allow for. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They are not test data and do not show that any part is safe to use. ConePro drops an 8 kg hammer about 45 J per blow onto a steel anvil and drives a steel rod into the ground; utility locates, eye and hearing protection and the precautions in CNP-PRC-001, Safety, apply to any use.

## Scope and method

The note checks every requirement in CNP-REQ-001 v0.6 against the design in CNP-PRC-001 v0.6, the decisions in CNP-DDR-001 to CNP-DDR-004 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and solids, so the masses, travel limits and interfaces used here are those in the STEP files and in drawing CNP-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

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
| Magnets | Sixteen 8 x 4 mm N42 disks (Br 1.3 T) on a 41 mm radius, 0.5 mm inside the hammer face; Hall switch operate point 6 mT; dipole model with the steel hammer ignored | The steel body will change the field; bench check later |
| Logger | 16 bytes per blow, 256 bytes per test header, up to 300 blows per test, 4 MB flash; average current 50.2 mA; 2,000 mAh from three AA alkaline cells, halved at 0 °C | As at TRL 2 plus the accelerometer |

## A. Geometry (R1)

The model builds the ASTM D6951 geometry from its parameters: a 20 mm cone with a 60° point (17.3 mm tall) on a 16 mm rod [A1], and a 100 mm OD, 22 mm bore hammer whose length, 138.0 mm, is derived from the 8.0 kg target with the magnet pockets and the three grip grooves (6 mm wide, 2 mm deep, decided by Amish on 2026-10-02) allowed for [A2]; the hammer is cut to that length at machining so it still weighs 8.00 kg. The upper rod length follows from the drop: the model's free drop from anvil top to stop collar is 575.0 mm, the upper rod runs 778 mm above the anvil to the top of the T-handle tube (plus a 20 mm threaded stud into the anvil) and the instrument stands 1,875 mm tall [A3]. The cone has a 12 mm parallel shoulder above its point so its tapped hole has wall round it (CNP-DDR-004). The spanner flats on the cone, lower rod and anvil (no thread locker on those joints, decided on 2026-10-02) leave the 20 mm cone base and every bearing face unchanged. The nominal geometry therefore meets R1; the tolerances in the standard are still to be checked against a copy of it.

## B. Blow energy

The hammer stores 45.1 J at the top of its drop, reaches 3.36 m/s at impact and falls in 0.342 s [B1]. After 3 % guide friction it lands with 43.8 J [B2]. The driven mass (cone, both rods, anvil, handle, aluminum clamp and pad) is 5.14 kg [B3]. With the Hiley impact efficiency (M + e²m) / (M + m), a restitution of 0.4 gives an efficiency of 0.671, a rod velocity after impact of 2.82 m/s and about 27.9 J at the cone, 62 % of the drop energy; the range for e = 0.2 to 0.6 is 26.0 to 31.2 J [B4]. The TRL 2 figure of 33 J assumed a 20 % impact loss; the calculation gives about 33 % [B5], and Figure 2 of CNP-PRC-001 is updated to match.

This does not change the indicative CBR, because the ASTM D6951 correlations are empirical for the standard apparatus. It does change the mean dynamic soil resistance: about 1.9 kN at 15 mm per blow and 14.0 kN at 2 mm per blow [B6].

## C. Mass and packing (R10)

*Table 2. Mass by part [C1].*

| Part | Mass (kg) | Source |
| --- | --- | --- |
| 1 Cone | 0.03 | Model |
| 2 Lower drive rod | 1.60 | Model |
| 3 Anvil and coupler | 1.45 | Model |
| 4 Drop hammer | 8.00 | Model |
| 5 Upper rod | 1.24 | Model |
| 6 Handle, stop, rubber grips and level | 0.67 | Model (grips at rubber density) |
| 7 Reference plate, 6 mm | 1.29 | Model |
| 9 Clamp and arm (aluminum, one piece) | 0.09 | Model |
| 8 Draw-wire reel; 10 pad; 11 logger with cells; 12 cable | 0.30; 0.06; 0.35; 0.12 | Catalog estimates |
| 13 Lightweight roll bag; 14 hardware and spare cone; 17 reel cable and P-clips | 0.40; 0.10; 0.04 | Catalog estimates |
| 14 End cap for the upper rod (aluminum) | 0.04 | Model |

The instrument as carried, in its bag with cells, weighs about 15.8 kg; without the bag it is 15.4 kg [C2]. Version 0.1 gave 16.7 kg with an 8 mm plate, a steel clamp and arm and a 0.80 kg canvas bag. Amish chose option (a) of the review (CNP-DDR-002, D9): the 6 mm plate saves 0.43 kg (1.72 to 1.29 kg), the aluminum clamp and arm 0.22 kg (0.34 to 0.12 kg) and the lighter bag 0.40 kg, 16.7 kg before and 15.7 kg after. The design for construction (CNP-DDR-004) moves mass between parts (the upper rod now runs through the handle, the clamp is one 12 mm piece, the reel cable and fixings are added) and leaves the total at 15.7 kg [C6]. Version 0.6 adds the rubber grips (0.08 kg) and the end cap (0.04 kg) decided on 2026-10-02, so the total is 15.8 kg [C2]. **R10 is met**, with a margin of about 0.2 kg. The heaviest piece, the hammer captive on the upper rod with the handle, grips and end cap, is 9.96 kg, and the hammer alone is 8.00 kg [C3], so the 10 kg limit is met with only 0.04 kg to spare: any further mass on the hammer assembly would break it. The longest piece is the lower rod with the cone, 1,029 mm, which fits a bag about 1.08 m long; the hammer assembly with its end cap is 810 mm [C4]. The optional extraction lever adds 3.0 kg carried separately [C5], and the optional extension rod 0.79 kg; with both accessories the kit is 19.6 kg, carried as two loads [C7].

## D. Penetration range (R5)

As the rod goes down, the first contact is the wire arm landing on the reel housing after 939 mm; the clamp collar would reach the plate at 1,011 mm and the anvil at 1,023 mm [D1]. Version 0.3 grows the reel housing from 60 x 56 x 60 mm to 72 x 60 x 72 mm so the 60 mm drum fits inside it with walls (CNP-DDR-003, decided by Amish on 2026-09-27); the reel top rises by 12 mm and the stroke falls from 940 mm to 928 mm, which still cleared the 850 mm usable range by 78 mm. Version 0.4 (CNP-DDR-004) lengthens the cone shoulder by 7 mm and moves the clamp up against the anvil by 4 mm, so the stroke is now 939 mm, 89 mm more than the usable range. The usable range is set at 850 mm, because the tilt error in section E grows quickly as the wire gets short [D2]; Amish accepted this range (CNP-DDR-002, D11). Version 0.1 found the 1,000 mm clause of R5 not met because no extension rod was in the BOM. Amish chose option (b) (CNP-DDR-002, D10): R5 is restated as 850 mm per lower rod, and a 500 mm extension rod (0.79 kg, $16 with its coupling sleeve, BOM line 16) is a separately carried accessory for deeper tests [C7]. **R5 is now met.** Automatic re-zero after adding a rod is a firmware function and is not verifiable at TRL 3.

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

**Rod lean in the field.** If the rod leans, the arm eye moves sideways over the reel and the wire reads short, most of all near the end of the stroke where the wire is short. At 1° of lean the uncorrected error is 0.16 mm at 500 mm, 1.35 mm at 850 mm and 15.4 mm at the full 939 mm; at 2° it is 5.29 mm at 850 mm [E4]. The app can correct for the lean using the tilt reading (D1), but a ±0.3° tilt error still leaves 0.95 mm at 1° and 1.79 mm at 2° at 850 mm [E4]. Version 0.3 gave 1.07 mm and 2.02 mm; the longer wire above the reel in version 0.4 (CNP-DDR-004) brings them back near the version 0.2 values. This is why the usable range stops at 850 mm, and why the depth accuracy in stiff layers near the end of a rod is weaker than the bench budget.

**Wire slack after each blow.** The rod starts down at 2.82 m/s and stops within 1.4 ms at 2 mm per blow, 10.6 ms at 15 mm per blow and 35 ms at 50 mm per blow. The spring cannot rewind the drum that fast, so the wire goes slack by up to 1.9, 9.6 and 17.3 mm and becomes taut again after 5.2 to 35 ms [E5]. Two consequences follow. First, the reel needs a groove keeper so slack wire cannot jump the groove and break the single-layer assumption. Second, when the wire snaps taut the drum stops suddenly: with a rigid eye the peak wire tension would be 42 to 285 N at 850 mm, near or above the breaking load of a 0.45 mm wire. A preloaded spring at the arm eye (8 N preload, 2 N/mm) limits the peak to 9 to 35 N, and because the spring stays on its stop under the 3 to 5 N reel force it adds no reading error [E5]. Both details are in BOM line 8; Amish accepted them (CNP-DDR-002, D11).

**Record latency (R4).** The depth is settled at most 35 ms after impact, so a 0.2 s settle window plus one 100 Hz sample records each blow 0.21 s after impact, inside the 0.5 s of R4 [E6].

**What the error means for the user.** Table 4 repeats the ASTM D6951 general correlation, CBR = 292 / DCP^1.12 [E7]. With the ±0.49 mm root-sum-square error at each end of an interval, the DCP index over 10 blows at 2 mm per blow is good to ±4.9 % (±9.8 % worst case) and the CBR to ±5.5 %; over a 50 mm stiff layer the DCP index is good to ±2.0 % [E8].

*Table 4. Indicative CBR from the ASTM D6951 general correlation [E7].*

| DCP index (mm per blow) | 2 | 5 | 10 | 15 | 25 | 50 |
| --- | --- | --- | --- | --- | --- | --- |
| Indicative CBR (%) | 134 | 48 | 22 | 14 | 8 | 4 |

**Plate settlement.** The plate, reel and logger press on 0.078 m² of ground at only 0.24 kPa, so static settlement is negligible. Settlement or heave caused by the blows cannot be calculated from first principles [E9]; it is left as an open question.

## F. Blow detection (R3)

With sixteen magnets set 0.5 mm into the hammer face and the Hall switch 8 mm below the face, 8.5 mm below the magnets, the dipole model gives 34 mT under a magnet and 14 mT between magnets, 2.3 times the 6 mT operate point at the worst angle; with the hammer lifted 30 mm the field falls to 1.7 mT, so the switch releases [F1]. A blow is counted only when the Hall switch sees the hammer arrive, the accelerometer sees an impact peak and the depth steps down or holds within 0.5 s [F2]. The accelerometer peak also flags short drops (section G). The logic is sound on paper, but "every blow and no false counts over 200 blows" can only be shown on a bench, so R3 is not verifiable at TRL 3. The steel hammer body will change the field and must be checked by measurement.

## G. Shock (R11)

The anvil and rods take a 2.82 m/s velocity step in 53 µs to 0.2 ms, a mean acceleration of about 1,400 to 5,500 g with peaks about twice that [G1]. The TRL 2 estimate of hundreds to a few thousand g was low. A sensor pad rigidly fixed to the anvil would be near the 10,000 g rating of typical MEMS accelerometers and Hall ICs. On a 300 Hz elastomer isolator, the pad sees about 542 g, 18 times below that rating, and sags only 2.8 µm under gravity, so the tilt reading is not affected [G2]. Because the pad peak scales with the square root of the drop height, a threshold at half the full-drop peak (271 g) flags drops below 144 mm as short [G3]. **R11 stays at risk**: fatigue of the isolator, the coiled cable and the connector over 10,000 blows is not calculated, and IP65 sealing and the 0 to 45 °C range can only be shown by test.

## H. Tilt (R6)

After zeroing by turning the rod 180° at setup, the accelerometer reads tilt to about ±0.3°, so the 5° warning trips between 4.7° and 5.3° [H1]. With the bubble level as a backup, R6 is met by design (D1).

## I. Data (R7, R8, R14)

A 300-blow test takes 4.9 KiB, so 4 MB of flash holds about 830 tests, well over the 50 of R8 [I1]. R7 (app output) and R14 (honest results wording) are specified in CNP-PRC-001 but the app is not written, so they are not verifiable at TRL 3.

## J. Test time and extraction (R9)

A practiced operator takes about 8.1 min for the reference test (setup 2.5 min, 57 blows 2.4 min, lever extraction 2.2 min at 50 mm per stroke, packing 1.0 min); a slow operator takes about 11.7 min [J1]. R9 is met by estimate, with a thin margin in the slow case. The extraction force is bounded above by the dynamic tip resistance: about 1.9 kN at 15 mm per blow, within the 3.0 kN of the 10:1 lever with 300 N at the hand, but 5.6 kN at 5 mm per blow, beyond it [J2]. The real pull force is expected to be lower because the cone rises through the hole it made. For stiff ground Amish accepted the recommendation to rely on the disposable-cone practice, stated in the user guidance, with no hardware change (CNP-DDR-002, D12). One person pulling by hand gives only about 0.4 kN, which is why the lever (D2) is needed at all.

## K. Power (R12)

The average current is 50.2 mA (microcontroller 35, angle sensor 7, Hall switch and LED 5, flash 3, accelerometer 0.2) [K1], so three AA alkaline cells last about 40 h at 20 °C and about 20 h at 0 °C [K2], well above the 8 h of R12.

## L. Cost (R13)

All 17 BOM lines are priced. The instrument (lines 1 to 14 and 17) costs $346 (v0.3: $319; the design for construction adds the reel-to-logger cable, $6, and $10 of welding, fixings and reel parts, CNP-DDR-004, for $335 in v0.4 and v0.5; the decisions of 2026-10-02 add the rubber grips, $6, and the end cap and hammer label, $5) and the optional accessories $66 (lever $50, extension rod with its coupling sleeve $16), $412 together, against the $400 value-engineering target (a hypothetical control target, not a limit) [L1]. R13, which covers the instrument, is within the target by $54. The kit with both optional accessories is $12 over the target; the savings worth trying are in the Value engineering section of the design decisions register. Prices are indicative. They were not quoted by suppliers.

## M. Retrofit fit (R15)

The sensor set clamps to a 16 mm rod, straps to any 50 to 80 mm anvil, sits 8 mm below the anvil top and passes the 20 mm cone through the 60 mm plate hole [M1]. Fit to commercial penetrometers needs one in hand, so R15 is not verifiable at TRL 3.

## Results

*Table 5. Requirement results, not met and at risk first.*

| ID | Value (calculation tag) | Target | Status |
| --- | --- | --- | --- |
| R2 | 0.046 mm resolution; bench ±0.98 mm worst, ±0.49 mm RSS; up to 1.8 mm more at 850 mm with a 2° lean [E1 to E4] | 0.5 mm; ±1 mm over 1,000 mm | At risk |
| R11 | About 542 g at the isolated pad; 1,400 to 5,500 g mean at the anvil [G1, G2] | IP65; 0 to 45 °C; 10,000 blows | At risk |
| R1 | 8.00 kg, 575 mm drop, 16 mm rod, 20 mm 60° cone [A1 to A3] | ASTM D6951 geometry | Met (nominal) |
| R4 | Settled within 35 ms; record at 0.21 s [E5, E6] | Within 0.5 s | Met |
| R5 | 939 mm stroke, 850 mm usable per rod; optional 500 mm extension rod [D1, D2, C7] | 850 mm per rod; extension rod as a separate accessory | Met (re-zero not verifiable) |
| R6 | ±0.3° tilt reading; warning at 5° [H1] | Warn above 5° | Met by design |
| R8 | About 830 tests stored [I1] | 50 tests | Met |
| R9 | 8.1 to 11.7 min [J1] | 12 min or less | Met (estimate, thin) |
| R10 | 15.8 kg carried, 9.96 kg heaviest piece, about 1.08 m packed [C2 to C4] | 16 kg; 10 kg; 1.1 m | Met (thin) |
| R12 | 40 h; 20 h at 0 °C [K2] | 8 h, non-lithium | Met |
| R13 | $346 instrument; $412 with the lever and extension rod [L1] | $400 or less (value-engineering target) | Within the value-engineering target |
| R3 | Hall margin 2.3 times; three-signal logic [F1, F2] | Every blow, no false counts in 200 | Not verifiable at TRL 3 |
| R7 | App specified, not written | Plot, DCP index, CBR, CSV | Not verifiable at TRL 3 |
| R14 | App wording specified, not written | Correlation and limits stated | Not verifiable at TRL 3 |
| R15 | Interfaces for 16 mm rods and 50 to 80 mm anvils [M1] | Fits standard DCPs without machining | Not verifiable at TRL 3 |

Counts: 9 met, 2 at risk, 0 not met, 4 not verifiable at TRL 3 (v0.1: 7 met, 2 at risk, 2 not met, 4 not verifiable).

## Checks against earlier figures

- Energy at the cone: TRL 2 said about 33 J (74 %); this note gives 27.9 J (62 %) [B5]. CNP-PRC-001 and the flow diagram are corrected.
- Anvil shock: TRL 2 said hundreds to a few thousand g; this note gives about 1,400 to 5,500 g mean at the anvil and about 540 g at an isolated pad [G1, G2]. Corrected.
- Total mass: TRL 2 said about 15.2 kg; v0.1 gave 16.7 kg with the bag, and v0.2, with the DDR-002 savings, gives 15.7 kg with the bag; v0.6, with the grips and end cap, gives 15.8 kg with the bag and 15.4 kg without it [C2, C6]. R10 is met.
- Penetration per rod: TRL 2 said about 850 mm; the model's stroke is 939 mm with 850 mm usable [D2]. Consistent.
- Cost: TRL 2 said about $296; v0.1 gave $321, v0.2 and v0.3 gave $319, v0.4 and v0.5 gave $335, and v0.6 gives $346 [L1].
- Resolution 0.046 mm, fall time 0.342 s, impact speed 3.36 m/s, battery life about 40 h and the CBR table are unchanged [B1], [E1], [E7], [K2].
