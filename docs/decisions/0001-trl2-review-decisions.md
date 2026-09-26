---
doc_id: CNP-DDR-001
title: ConePro TRL 2 review decisions
project: ConePro
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); TRL 3 items now decided in CNP-DDR-002
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D8; item O1 remains proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the design precis CNP-PRC-001 v0.2 listed the same key design choices with options. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open.

The same instruction approved three portfolio-wide SwapCell decisions (a wake method for hosts without CAN, a charge-while-discharging mode and a vehicle latch vibration rating in SwapCell interface v0.3; shared packs priced once and excluded from dependent kit budgets) and directed that community designs pick co-design partners per area later. ConePro runs on three AA cells and does not use a SwapCell pack, so the SwapCell items do not apply to it.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CNP-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Verticality (R6) | Option (a): a 3-axis accelerometer in the anvil sensor pad reads rod tilt between blows, with option (b), a bubble level on the handle, as a backup. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Rod extraction | Option (a): an optional lever rod puller with a rod clamp, carried separately and kept out of the instrument BOM total (R13) and the carried mass (R10). Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Complete instrument or retrofit kit | Design the sensor set (BOM items 8 to 12) to fit standard 16 mm ASTM D6951 penetrometers from the start, and build the complete instrument for the prototype. The pitch in `project.yaml` is unchanged; the review made no rewording recommendation. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Depth sensing | Draw-wire sensor referenced to a plate on the ground, with a laser time-of-flight sensor as the fallback to compare later. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Hammer | Standard 8 kg hammer and 575 mm drop; the 4.6 kg option is noted for later. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Blow detection | Hall-effect sensor with the depth signal as a cross-check. With D1, the accelerometer's impact peak is added as a third signal. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Electronics location | Logger on the stationary plate, so only the sensor pad sees impacts. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Cells | Three AA cells rather than a lithium-ion cell. Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items that remain open (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and user group (small contractors, an NGO shelter or water team, or a low-volume road agency) | Proposed, awaiting Amish. Co-design partners are to be picked per area later, as Amish directed for community designs. |

## Consequences

- `project.yaml`: `budget_usd` stays $400 (no change was recommended). Pitch and problem lines are unchanged.
- CNP-PRB-001, CNP-PRC-001 and CNP-REQ-001 are revised to v0.3. R6 is now met by design (D1). R9 now assumes the lever puller (D2). A new requirement, R15, carries D3: the sensor set must fit standard DCPs without machining. No target is relaxed.
- The BOM gains the accelerometer (line 10), the bubble level (line 6) and the optional extraction lever (line 15, excluded from the instrument total). The anvil loses its sensor pocket, because the pad now clamps on (D3).
- CNP-CAL-001 checks every requirement against the decided design. The new issues it raised (R10 mass with the bag, the R5 extension-rod clause, the draw-wire reel details and stiff-ground extraction) are now Decided by Amish, 2026-09-25: go with recommendation, and recorded in CNP-DDR-002 (D9 to D12).
