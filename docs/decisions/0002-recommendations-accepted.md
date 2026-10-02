---
doc_id: CNP-DDR-002
title: ConePro recommendations accepted
project: ConePro
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of the TRL 3 review recommendations and what changed in the repo
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 decided by Amish on 2026-10-02 (recommendation approved, CNP-DEC-001)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items D9 to D12; item O1 was decided on 2026-10-02 (CNP-DEC-001)

## Context

The TRL 3 review note (`docs/REVIEW.md`, session 2026-09-25, TRL 3) listed five items as "Proposed, awaiting Amish". Four carried a recommendation; the first co-design partner (O1, carried over from CNP-DDR-001) did not. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of that recommendation, and where options were offered the recommended option is the decision. Items without a recommendation stay open. The TRL 2 items D1 to D8 were already decided in CNP-DDR-001 and are unchanged. TRL 4 remains on hold by Amish's instruction, so nothing here starts a build, test or purchase.

## Options considered

The options for each item are those listed in `docs/REVIEW.md`, session 2026-09-25, TRL 3, "Proposed, awaiting Amish", items 2 to 5.

## Decision

*Table 1. Newly decided items.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D9 | R10 carried mass | Option (a): a 0.40 kg bag, an aluminum clamp and arm, and a 6 mm plate. Decided by Amish, 2026-09-25: go with recommendation. | `cad/src/model.py`: `plate_t` 8 to 6 mm; clamp density aluminum in `sizing.py`. BOM line 7 (6 mm plate, $28 to $24), line 9 (aluminum, $8 to $10), line 13 (0.40 kg nylon roll bag). Carried mass 16.7 to 15.7 kg; R10 not met to met. Instrument cost $321 to $319. Stroke 938 to 940 mm. |
| D10 | R5 extension rod | Option (b): relax R5 to 850 mm per rod and offer a 500 mm extension rod as a separately carried accessory. Decided by Amish, 2026-09-25: go with recommendation. | CNP-REQ-001 R5 restated (was "1,000 mm or more with one extension rod"). BOM line 16 added: optional 500 mm extension rod, $15, 0.79 kg, outside the R10 mass and R13 total. R5 not met to met. Kit with both accessories $384. |
| D11 | Draw-wire reel details | Accept the metal single-layer grooved drum, groove keeper and preloaded eye spring (8 N, 2 N/mm) in BOM line 8, and a usable range of 850 mm per rod. Decided by Amish, 2026-09-25: go with recommendation. | No geometry or cost change; CNP-PRC-001 and CNP-CAL-001 now record the details as decided. The bought industrial draw-wire sensor stays the fallback. |
| D12 | Stiff-ground extraction | Note the disposable-cone practice for stiff ground in the user guidance; no hardware change. Decided by Amish, 2026-09-25: go with recommendation. | CNP-PRC-001, How it works (step 6) and Safety, state the practice. No BOM or model change. |

*Table 2. Item left open then, decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First co-design partner and user group (small contractors, an NGO shelter or water team, or a low-volume road agency) | Decided by Amish, 2026-10-02 (recommendation approved): first partner to approach is a low-volume road agency (a county or district road department) that already runs manual DCP tests on unpaved roads; a university pavement or geotechnical lab is the second choice (CNP-DEC-001). |

## Consequences

- `project.yaml`: `budget_usd` stays $400 (no budget change was recommended); pitch and problem unchanged; `trl: 3`, `trl_target: 3`.
- CNP-REQ-001 v0.4: R5 restated; R10 met; no requirement is now not met. Status: 9 met, 2 at risk (R2, R11), 4 not verifiable at TRL 3 (R3, R7, R14, R15).
- CNP-CAL-001 v0.2: rerun against the changed model. Driven mass 5.35 to 5.12 kg, energy at the cone 27.6 to 28.0 J, isolated pad peak 533 to 543 g.
- CNP-PRC-001 v0.4 and drawing CNP-DWG-001 Rev P2 (6 mm plate, aluminum clamp, 15.7 kg note); STEP, STL and concept media regenerated.
- Cross-repo actions: none.
- TRL 4 work that these decisions will eventually need (weighing the kit, fitting the extension rod and testing re-zero, stiff-ground extraction trials) is decided in principle but on hold, because TRL 4 is on hold by Amish's instruction.
