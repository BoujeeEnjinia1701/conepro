---
doc_id: CNP-REQ-001
title: ConePro requirements
project: ConePro
doc_type: Requirements
version: "0.2"
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
---

# ConePro requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design (see CNP-PRB-001). One requirement, R6 (verticality warning), is **not met** by the current concept. Four more are at risk: R2 (depth accuracy), R3 (blow detection), R9 (test time, because the extraction method is open) and R11 (shock survival).

**Reference test.** A single test point driven to 850 mm in a medium-stiff soil averaging 15 mm per blow (about 57 blows), by one person, on level ground.

| ID | Requirement | Target | Status at TRL 2 | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Standard DCP geometry | 8.0 kg hammer, 575 mm free drop, 16 mm rod, 20 mm cone with a 60 degree point, replaceable cone; tolerances as ASTM D6951 | Met by design | Drawing check against the standard |
| R2 | Depth measurement | Resolution 0.5 mm or finer; error within ±1 mm over a 1,000 mm range compared with a steel rule | At risk: a low-cost draw-wire reel may reach about ±2 mm (estimate) | Error budget calculation; later bench calibration |
| R3 | Blow detection | Every blow counted and no false counts from handling, over a 200-blow sequence | At risk: sensor sits on the anvil in the impact shock | Design review; later bench test |
| R4 | Per-blow record | Depth after each blow logged within 0.5 s of impact, with blow number and time | Met by design | Firmware sketch review |
| R5 | Penetration range | 850 mm or more per lower rod; 1,000 mm or more with one extension rod and automatic re-zero | 850 mm met by the massing model (estimate); re-zero unverified | Model check; later field test |
| R6 | Verticality | Warn the operator when the rod is more than 5 degrees off vertical | **Not met:** the concept has no tilt sensing on the rod | Design change needed (see CNP-PRC-001) |
| R7 | Phone output | Live plot of depth against blows; DCP index per layer; indicative CBR from the ASTM D6951 correlations with the soil type selected; CSV export with time, location and operator notes | Met by design (app not written) | App specification review |
| R8 | Works offline | No cell signal needed; logger stores 50 or more tests if the phone is absent or disconnects | Met by design | Firmware sketch review |
| R9 | One-person test time | Reference test, including setup and rod extraction, in 12 min or less by one person | At risk: about 8 to 10 min estimated, but the extraction method is not chosen | Time estimate; later timed trials |
| R10 | Portability | Total mass 16 kg or less; heaviest piece 10 kg or less; packed length 1.1 m or less | Met by estimate, thin margins: about 15.2 kg, heaviest piece about 9.8 kg, packed length about 1.0 m | Mass roll-up from the TRL 3 model |
| R11 | Rugged electronics | Logger, sensors and connectors IP65; operate at 0 to 45 °C; anvil-mounted parts survive 10,000 blows | At risk: impact shock at the anvil estimated at hundreds to a few thousand g | Shock estimate; later drop-count test |
| R12 | Battery life | 8 h or more of continuous logging on user-replaceable non-lithium cells | Met by estimate: about 40 h on three AA alkaline cells | Power budget |
| R13 | Cost | $400 or less in parts for one complete instrument | Met by estimate: about $296 | Priced BOM (`bom/bom.csv`) |
| R14 | Honest results | App states the correlation used and that results are indicative and not for foundation design | Met by design | App specification review |

## Assumptions

- Soil behavior, blow rate and extraction time are estimates, not measurements. A practiced operator drops the hammer about once every 2.5 s.
- CBR correlations are those given in ASTM D6951 (from US Army Corps of Engineers work); other soils and regions may need local correlations.
- Mass estimates use steel at 7,850 kg/m³ and aluminum at 2,700 kg/m³ applied to the massing model.
- Battery life assumes an average electronics draw of about 50 mA and about 2,000 mAh usable from AA alkaline cells at that current.
