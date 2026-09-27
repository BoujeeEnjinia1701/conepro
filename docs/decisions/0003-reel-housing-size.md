---
doc_id: CNP-DDR-003
title: ConePro reel housing sized round the 60 mm drum
project: ConePro
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-27'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-27'
  author: Amish Chadha
  change: Record Amish's decision to keep the 60 mm drum and grow the reel housing to 72 x 60 x 72 mm
---

# 0003: Reel housing sized round the 60 mm drum

- **Date:** 2026-09-27
- **Status:** accepted

## Context

The product appearance model (`cad/src/product_model.py`, review session 2026-09-26) found that the 60 mm grooved drum (`drum_d`) cannot fit inside the 60 x 56 x 60 mm draw-wire reel housing (`reel_box`) once the housing has walls, so the render drew a 48 mm drum instead. The calculations in CNP-CAL-001 need the 60 mm drum: it pays out 188.5 mm per turn, which gives 0.046 mm per count with a 12-bit sensor and keeps a 1,000 mm stroke to a single layer [E1].

## Options considered

1. Keep the 60 mm drum and grow the housing to about 72 x 60 x 72 mm. The reel top rises by 12 mm, so the stroke (limited by the wire arm meeting the reel housing) falls by 12 mm.
2. Shrink the drum to fit the existing housing. This coarsens the resolution per count, adds turns per stroke and needs the calculations reworked.

The recommendation in `docs/REVIEW.md` (session 2026-09-26, item 1) was option 1.

## Decision

Option 1: keep the 60 mm drum and grow the reel housing to 72 x 60 x 72 mm, accepting the loss of about 12 mm of stroke. Decided by Amish on 2026-09-27.

## Consequences

- `cad/src/model.py`: `reel_box` 60 x 56 x 60 mm to 72 x 60 x 72 mm; the reel exit point (`reel_xy`) and every other dimension and interface are unchanged. The reel top rises from 66 mm to 78 mm above the ground.
- Stroke per lower rod 940 mm to 928 mm, still limited by the wire arm on the reel housing; the usable range stays 850 mm (D11 in CNP-DDR-002), a 78 mm margin [D1, D2 in CNP-CAL-001 v0.3]. R5 stays met.
- Because the wire above the reel is 12 mm shorter at the same depth, the lean error at 850 mm after tilt correction grows from 0.94 mm to 1.07 mm at 1 degree and from 1.77 mm to 2.02 mm at 2 degrees [E4]; the rigid-eye snap tension at 850 mm grows from 41 to 283 N to 44 to 304 N, and the preloaded eye spring still limits it to 9 to 35 N [E5]. R2 stays at risk; no status changes.
- `cad/src/product_model.py` now draws the full 60 mm drum from `drum_d` inside the larger housing; the 48 mm stand-in is removed.
- BOM line 8: housing size stated; price ($35) and mass estimate (0.30 kg) unchanged. Instrument total stays $319; carried mass stays 15.7 kg.
- Drawing CNP-DWG-001 Rev P2 to P3; STEP, STL and concept media regenerated.
- CNP-CAL-001 v0.3, CNP-REQ-001 v0.5, CNP-PRC-001 v0.5.
- `project.yaml`: `trl` stays 3; `budget_usd` unchanged. TRL 4 remains on hold.
