---
doc_id: CNP-REQ-001
title: ConePro requirements
project: ConePro
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-09-30'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R5 restated to 850 mm per rod with the extension rod as a separate accessory; R10 met by the lighter plate, clamp and bag; status from CNP-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-27'
  author: Amish Chadha
  change: Status from CNP-CAL-001 v0.3 after the reel housing change in CNP-DDR-003 (decided by Amish on 2026-09-27); R5 stroke 928 mm, 850 mm usable still met; R2 lean term 2.0 mm
- version: "0.6"
  date: '2026-09-30'
  author: Amish Chadha
  change: Status from CNP-CAL-001 v0.4 after the design for construction (CNP-DDR-004); R5 stroke 939 mm; R2 lean term 1.8 mm; R13 $335; R15 sensor set now includes the reel cable (line 17); no status changes
---

# ConePro requirements

These requirements were checked by calculation at TRL 3 in CNP-CAL-001 v0.4 against the design decided in CNP-DDR-001, CNP-DDR-002 and CNP-DDR-003 and made constructable in CNP-DDR-004. None is now not met: two are at risk, nine are met on paper and four cannot be verified until hardware exists. The two at risk are **R2** (depth accuracy) and **R11** (shock survival). Version 0.4 applies Amish's 2026-09-25 acceptance of the review recommendations (CNP-DDR-002): **R5** is restated as 850 mm per lower rod, with a 500 mm extension rod offered as a separately carried accessory instead of a 1,000 mm clause (D10), and **R10** is now met at about 15.7 kg (was 16.7 kg) with a 6 mm plate, an aluminum clamp and arm and a lighter bag (D9). Targets are still proposals, not yet validated with users, and will be revised after co-design (see CNP-PRB-001). Version 0.5 reflects the larger reel housing decided by Amish on 2026-09-27 (CNP-DDR-003): R5 stays met with a 928 mm stroke, and the lean term in R2 grows from 1.8 mm to 2.0 mm, so R2 stays at risk. R15 carries decision D3.

**Reference test.** A single test point driven to 850 mm in a medium-stiff soil averaging 15 mm per blow (about 57 blows), by one person, on level ground.

*Table 1. Requirements and status at TRL 3.*

| ID | Requirement | Target | Status at TRL 3 (CNP-CAL-001) | Verification (later) |
| --- | --- | --- | --- | --- |
| R1 | Standard DCP geometry | 8.0 kg hammer, 575 mm free drop, 16 mm rod, 20 mm cone with a 60 degree point, replaceable cone; tolerances as ASTM D6951 | Met (nominal): model gives 8.00 kg and 575 mm; tolerances to check against the standard | Drawing check against the standard |
| R2 | Depth measurement | Resolution 0.5 mm or finer; error within ±1 mm over a 1,000 mm range compared with a steel rule | **At risk:** 0.046 mm resolution; bench error ±0.98 mm worst case, ±0.49 mm root sum square; a 2 degree lean adds up to 1.8 mm at 850 mm after tilt correction; usable range set at 850 mm (D11) | Bench calibration |
| R3 | Blow detection | Every blow counted and no false counts from handling, over a 200-blow sequence | Not verifiable at TRL 3: Hall margin 2.3 times at the worst angle; three-signal logic (Hall, accelerometer peak, depth) | Bench blow sequence |
| R4 | Per-blow record | Depth after each blow logged within 0.5 s of impact, with blow number and time | Met (calculation): settled within 35 ms, recorded at 0.21 s | Firmware sketch review |
| R5 | Penetration range | 850 mm or more per lower rod; deeper tests with an optional 500 mm extension rod carried as a separate accessory, with automatic re-zero (restated by D10; was 1,000 mm or more with one extension rod) | Met: 939 mm stroke, 850 mm usable per rod; extension rod in BOM line 16 (optional); re-zero not verifiable at TRL 3 | Model check; field test |
| R6 | Verticality | Warn the operator when the rod is more than 5 degrees off vertical | Met by design (D1): accelerometer reads tilt to about ±0.3 degree; bubble level as backup | Bench tilt check |
| R7 | Phone output | Live plot of depth against blows; DCP index per layer; indicative CBR from the ASTM D6951 correlations with the soil type selected; CSV export with time, location and operator notes | Not verifiable at TRL 3 (app specified, not written) | App specification review |
| R8 | Works offline | No cell signal needed; logger stores 50 or more tests if the phone is absent or disconnects | Met (calculation): about 830 tests in 4 MB | Firmware sketch review |
| R9 | One-person test time | Reference test, including setup and rod extraction with the optional lever (D2), in 12 min or less by one person | Met (estimate), thin: 8.1 to 11.7 min | Timed trials |
| R10 | Portability | Total mass as carried in the bag, cells included and the optional lever and extension rod excluded, 16 kg or less; heaviest piece 10 kg or less; packed length 1.1 m or less | Met, thin: 15.7 kg (was 16.7 kg before D9); heaviest piece 9.8 kg; packed length about 1.08 m | Mass roll-up; weighing |
| R11 | Rugged electronics | Logger, sensors and connectors IP65; operate at 0 to 45 °C; anvil-mounted parts survive 10,000 blows | **At risk:** about 1,400 to 5,500 g mean at the anvil; about 540 g on the isolated pad against 10,000 g part ratings; cable and connector fatigue not calculated | Drop-count test |
| R12 | Battery life | 8 h or more of continuous logging on user-replaceable non-lithium cells | Met (calculation): about 40 h, about 20 h at 0 °C | Power measurement |
| R13 | Cost | $400 or less in parts for one complete instrument (optional lever and extension rod excluded) | Met: $335; $401 with the lever and extension rod | Priced BOM (`bom/bom.csv`) |
| R14 | Honest results | App states the correlation used and that results are indicative and not for foundation design | Not verifiable at TRL 3 (app not written) | App specification review |
| R15 | Retrofit fit (D3) | Sensor set (BOM items 8 to 12 and 17) fits a standard ASTM D6951 penetrometer with a 16 mm rod and a 50 to 80 mm anvil, without machining | Not verifiable at TRL 3: interfaces sized in the model; needs a commercial DCP to check | Fit check on a commercial DCP |

## Assumptions

- Soil behavior, blow rate and extraction time are estimates, not measurements. A practiced operator drops the hammer about once every 2.5 s; a slow one every 3.5 s.
- CBR correlations are those given in ASTM D6951 (from US Army Corps of Engineers work); other soils and regions may need local correlations.
- Mass estimates use steel at 7,850 kg/m³ and aluminum at 2,700 kg/m³ applied to the parametric model `cad/src/model.py`, plus catalog masses for bought parts (CNP-CAL-001, Table 2).
- Battery life assumes an average electronics draw of about 50 mA and about 2,000 mAh usable from AA alkaline cells at that current, halved at 0 °C.
- All other calculation assumptions are listed in CNP-CAL-001, Table 1.
