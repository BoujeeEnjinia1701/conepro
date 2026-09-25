---
doc_id: CNP-REQ-001
title: ConePro requirements
project: ConePro
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CNP-CAL-001; decisions in CNP-DDR-001 (R6 met by D1, R9 assumes the lever of D2, new R15 from D3); R10 total defined as carried in the bag
---

# ConePro requirements

These requirements were checked by calculation at TRL 3 in CNP-CAL-001 against the design decided in CNP-DDR-001. Seven are met on paper, two are at risk, two are not met and four cannot be verified until hardware exists. The misses are **R5**, whose 1,000 mm clause needs an extension rod that is not in the BOM, and **R10**, where the instrument carried in its bag weighs about 16.7 kg against 16 kg. The two at risk are R2 (depth accuracy) and R11 (shock survival). Targets are still proposals for review, not yet validated with users, and will be revised after co-design (see CNP-PRB-001). No target was relaxed at TRL 3; R15 is new and carries decision D3.

**Reference test.** A single test point driven to 850 mm in a medium-stiff soil averaging 15 mm per blow (about 57 blows), by one person, on level ground.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status at TRL 3 (CNP-CAL-001) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Standard DCP geometry | 8.0 kg hammer, 575 mm free drop, 16 mm rod, 20 mm cone with a 60 degree point, replaceable cone; tolerances as ASTM D6951 | Met (nominal): model gives 8.00 kg and 575 mm; tolerances to check against the standard | Drawing check against the standard |
| R2 | Depth measurement | Resolution 0.5 mm or finer; error within ±1 mm over a 1,000 mm range compared with a steel rule | **At risk:** 0.046 mm resolution; bench error ±0.98 mm worst case, ±0.49 mm root sum square; a 2 degree lean adds up to 1.8 mm at 850 mm after tilt correction | Bench calibration |
| R3 | Blow detection | Every blow counted and no false counts from handling, over a 200-blow sequence | Not verifiable at TRL 3: Hall margin 2.3 times at the worst angle; three-signal logic (Hall, accelerometer peak, depth) | Bench blow sequence |
| R4 | Per-blow record | Depth after each blow logged within 0.5 s of impact, with blow number and time | Met (calculation): settled within 36 ms, recorded at 0.21 s | Firmware sketch review |
| R5 | Penetration range | 850 mm or more per lower rod; 1,000 mm or more with one extension rod and automatic re-zero | **Not met (1,000 mm clause):** 938 mm stroke, 850 mm usable, but no extension rod in the BOM; re-zero unverified | Model check; field test |
| R6 | Verticality | Warn the operator when the rod is more than 5 degrees off vertical | Met by design (D1): accelerometer reads tilt to about ±0.3 degree; bubble level as backup | Bench tilt check |
| R7 | Phone output | Live plot of depth against blows; DCP index per layer; indicative CBR from the ASTM D6951 correlations with the soil type selected; CSV export with time, location and operator notes | Not verifiable at TRL 3 (app specified, not written) | App specification review |
| R8 | Works offline | No cell signal needed; logger stores 50 or more tests if the phone is absent or disconnects | Met (calculation): about 830 tests in 4 MB | Firmware sketch review |
| R9 | One-person test time | Reference test, including setup and rod extraction with the optional lever (D2), in 12 min or less by one person | Met (estimate), thin: 8.1 to 11.7 min | Timed trials |
| R10 | Portability | Total mass as carried in the bag, cells included and the optional lever excluded, 16 kg or less; heaviest piece 10 kg or less; packed length 1.1 m or less | **Not met (total):** 16.7 kg; heaviest piece 9.8 kg and packed length about 1.08 m are met | Mass roll-up; weighing |
| R11 | Rugged electronics | Logger, sensors and connectors IP65; operate at 0 to 45 °C; anvil-mounted parts survive 10,000 blows | **At risk:** about 1,400 to 5,400 g mean at the anvil; about 530 g on the isolated pad against 10,000 g part ratings; cable and connector fatigue not calculated | Drop-count test |
| R12 | Battery life | 8 h or more of continuous logging on user-replaceable non-lithium cells | Met (calculation): about 40 h, about 20 h at 0 °C | Power measurement |
| R13 | Cost | $400 or less in parts for one complete instrument (optional lever excluded) | Met: $321; $371 with the lever | Priced BOM (`bom/bom.csv`) |
| R14 | Honest results | App states the correlation used and that results are indicative and not for foundation design | Not verifiable at TRL 3 (app not written) | App specification review |
| R15 | Retrofit fit (D3) | Sensor set (BOM items 8 to 12) fits a standard ASTM D6951 penetrometer with a 16 mm rod and a 50 to 80 mm anvil, without machining | Not verifiable at TRL 3: interfaces sized in the model; needs a commercial DCP to check | Fit check on a commercial DCP |

## Assumptions

- Soil behavior, blow rate and extraction time are estimates, not measurements. A practiced operator drops the hammer about once every 2.5 s; a slow one every 3.5 s.
- CBR correlations are those given in ASTM D6951 (from US Army Corps of Engineers work); other soils and regions may need local correlations.
- Mass estimates use steel at 7,850 kg/m³ and aluminum at 2,700 kg/m³ applied to the parametric model `cad/src/model.py`, plus catalog masses for bought parts (CNP-CAL-001, Table 2).
- Battery life assumes an average electronics draw of about 50 mA and about 2,000 mAh usable from AA alkaline cells at that current, halved at 0 °C.
- All other calculation assumptions are listed in CNP-CAL-001, Table 1.
