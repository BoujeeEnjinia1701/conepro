---
doc_id: CNP-DEC-001
title: ConePro design decisions register
project: ConePro
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open items from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# ConePro design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/` or in the review note `docs/REVIEW.md`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Decisions awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction: M12 rod joints and a 12 mm cone shoulder, pinned stop collar and welded handle, magnet pockets outside the strike area, one-piece clamp against the anvil, curved pad under the band, reel internals with the drum's edge under the exit, fixings for the reel and logger, reel-to-logger cable, coupling sleeve on the extension rod (P1 to P12) | Accept all; accept some and ask for alternatives to others | Accept all; each keeps what ConePro does and was needed to make a part buildable | Every component; the whole build plan follows these changes | CNP-DDR-004, Tables 1 and 2 |
| 2 | Keeping the hammer on the upper rod when it is off the anvil (packing and carrying): the 8 kg hammer can slide off the rod's lower end | (a) a screw-on end cap on the rod's M12 stud whenever it is off the anvil; (b) pack with the anvil on the upper rod and relax the 10 kg heaviest-piece limit of R10 (about 11.3 kg); (c) user guidance only | (a); it adds to the safety case, so it is Amish's call | A small cap in BOM line 14; packing | CNP-DDR-004, A1 |
| 3 | First co-design partner and user group | Small contractors, an NGO shelter or water team, or a low-volume road agency | None yet; to be picked per area | Not part of the TRL 3 build; shapes field trials at TRL 4 | CNP-DDR-001 and CNP-DDR-002, O1 |
| 4 | Clear windows in the reel housing and logger lid shown in the photoreal renders | (a) render-only features, opaque parts in the design; (b) real inspection windows, each with an extra seal | (a), since each window adds a seal to an IP65 box | None if (a); housing and lid if (b) | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 5 | Grip grooves on the hammer in the appearance model | Accept; leave the hammer plain | Accept; length is set at machining to keep 8.00 kg (the magnet pockets are now defined in CNP-DDR-004) | Hammer making sketch (grooves would be added) | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 6 | Rubber grips on the T-handle | Add grips of about 33 mm diameter to BOM line 6; no grips | Add them (a few dollars) | T-handle | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 7 | Coiled cable path as drawn in the renders | Accept; redraw | Accept | None | `docs/REVIEW.md`, 2026-09-26, item 5 |

## To confirm when parts are bought

*Table 2. Items to check against the parts actually bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The tolerances of ASTM D6951 for the cone, hammer mass and drop, against a copy of the standard | R1 is met only nominally until the tolerances are checked | CNP-CAL-001 section A |
| 2 | The bubble level is 20 mm across and about 6 mm tall | It sits in a 20 x 3 mm recess in the seat disc | CNP-DDR-004, P4 |
| 3 | The spring motor fits in 40 mm diameter x 8 mm and gives about 3 N retracted to 5 N extended | The reel layout and the wire slack and snap calculations assume it | CNP-CAL-001 [E5] |
| 4 | The angle sensor board is about 30 x 30 mm, 12-bit, with a matching diametric magnet | It mounts on the lid 1.4 mm from the shaft magnet | CNP-DDR-004, P8 |
| 5 | The flanged IP65 logger box, about 100 x 70 x 42 mm, and its flange hole spacing (82 mm across, 36 mm along) | It sets the four tapped holes in the plate | CNP-DDR-004, P9 |
| 6 | The M12 glands seal on 5 mm and 6 mm cable | IP65 entries for both cables (R11) | CNP-DDR-004, P10, P11 |
| 7 | The band clamp's range takes the anvil plus the pad (about 90 mm across) | It goes round the anvil and over the pad | CNP-DDR-004, P7 |
| 8 | The Hall switch and accelerometer are rated to 10,000 g shock, and the elastomer gives about 300 Hz isolation with the pad | The shock calculation assumes both | CNP-CAL-001 section G |
| 9 | The bearings are 6 x 13 x 5 mm and fit the 18 mm boss | The boss is printed to suit | CNP-DDR-004, P8 |

## Value engineering

Value-engineering target: USD 400 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 335 for the instrument (USD 65 under the target); the kit with both optional accessories is USD 401 (USD 1 over the target).

- **Main cost drivers:** the mechanical penetrometer (items 1 to 7, USD 174), sensing and logging (items 8 to 12 and 17, USD 113), and the carry bag, hardware and consumables (USD 48); the optional lever (USD 50) and extension rod (USD 16) are outside the instrument total. The design for construction added USD 16 (the reel-to-logger cable at USD 6 and USD 10 of welding, fixings and reel parts).
- **Savings worth trying:** trim the price of an optional accessory, which would bring the full kit to the target; and re-price the sensing parts at purchase.

## Decisions made

*Table 3. Decisions made, with the record that holds each.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: accelerometer tilt with a bubble level backup; optional lever extraction; sensor set designed to fit standard DCPs; draw-wire depth with a laser fallback; standard 8 kg geometry; Hall blow detection with cross-checks; electronics on the plate; three AA cells | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | [CNP-DDR-001](decisions/0001-trl2-review-decisions.md) |
| 2026-09-25 | D9 lighter carried set (6 mm plate, aluminum clamp, 0.40 kg bag); D10 R5 at 850 mm per rod with an optional extension rod; D11 reel details and 850 mm usable range; D12 disposable-cone practice for stiff ground | Amish: "i accept all your recommendations, go with them across all repos." | [CNP-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-27 | Keep the 60 mm drum and grow the reel housing to 72 x 60 x 72 mm | Amish asked to "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense" and chose this option | [CNP-DDR-003](decisions/0003-reel-housing-size.md) |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; changes recorded in CNP-DDR-004 and open for review (open decision 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | [CNP-DDR-004](decisions/0004-design-for-construction.md) |
| 2026-09-30 | Open decisions go in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
