---
doc_id: CNP-DDR-004
title: ConePro design for construction
project: ConePro
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0004: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. Every change in Tables 1 and 2 was made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. Nothing here changes what ConePro does, its pitch or its safety case. Items that would are in Table 3 as "Proposed, awaiting Amish" and in the design decisions register (`docs/06-design-decisions.md`).

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The ConePro model of CNP-DDR-003 was a massing model with correct proportions and interfaces, but parts of it could not be made or joined as drawn: the rods had no threads, the wire arm ran through the rod, the stop collar and handle stem overlapped the rod and the tube, the band ran through the sensor pad, the reel was a solid block, and nothing held the reel or logger to the plate.

The model (`cad/src/model.py`) now builds every part as a separate solid, including fixings, and runs 64 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch with no overlap, parts that must stay apart keep their stated clearance, and no two of its 39 components (parts and fixing sets) overlap. All 64 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The cone's 5 mm parallel shoulder could not hold a threaded hole: a 12 mm tapped hole of useful depth would break out through the 60° point. | The shoulder is 12 mm long (cone 29.3 mm overall), tapped M12 x 1.75 to 14 mm deep in its top face; hardened after tapping. | Keeps the 20 mm, 60° ASTM D6951 point. The rod shoulder bears on the cone's top face, so the thread only locates the cone. The instrument stands 7 mm taller (1,874 mm). |
| P2 | Rods, anvil and cone met as plain cylinders with no joint. | M12 x 1.75 studs turned on the rod ends (12 mm at the cone, 20 mm at the anvil) and M12 tapped holes 24 mm deep in both anvil faces; every joint seats on a square 16 mm shoulder, with medium thread locker. | Blows pass through the shoulders, not the threads. One thread size for every joint; ordinary lathe work. |
| P3 | The handle stem overlapped the T-handle tube; the stop collar was solid where the rod passed through it; neither had a fixing. | The upper rod runs up through the stop collar and through a 16 mm cross hole in the tube, its top flush with the tube; the tube is welded to the rod; the collar is fixed by a 6 mm roll pin drilled through collar and rod at the drop height. | The pin lets the 575 mm drop be set on the finished hammer before drilling. Upper rod 776 mm above the anvil. |
| P4 | The bubble level was a block resting on the round tube along a line, with no fixing. | A 30 x 5 mm steel seat disc is welded on the rod top; a 20 mm bullseye level is bonded in a 3 mm recess in it. | A bullseye on the rod axis reads plumb directly; overall height is unchanged. |
| P5 | The hammer magnets had no defined position and would sit in the striking face. | Sixteen 8.2 mm pockets on an 82 mm circle, outside the 64 mm anvil strike area; magnets bonded 0.5 mm below the face; hammer length 136.5 mm to keep 8.00 kg. | Magnets are never struck. The Hall switch sees them from 8.5 mm instead of 8 mm; the calculated field between magnets is still 2.3 times the switch operate point [F1]. |
| P6 | The wire arm ran through the rod and the clamp collar; the arm had no joint to the collar; and only friction held the collar against the rod's acceleration of thousands of g. | Collar and arm cut in one piece from 12 mm aluminum plate (40 mm boss, 16 mm wide arm, 3.2 mm wire eye), split with a saw slit and an M5 clamp screw; its top face butts the underside of the anvil. | The anvil carries the clamp at every blow, so it cannot slip up the rod. One flat part, cut, drilled and tapped. The clamp lands on the reel 4 mm later, so the stroke grows (P1 and P6 together: 928 to 939 mm). |
| P7 | The band clamp passed through the sensor pad, the pad's flat face touched the round anvil on a line, and the isolator was not drawn. | The pad's face is curved to 36 mm radius on a 4 mm curved elastomer isolator; the band goes round the anvil and over the pad's outer face, pressing both on; a strain relief boss carries the cable out underneath. | Full contact through the isolator; a stock worm-drive band does the clamping; any 50 to 80 mm anvil works with a pad face of anvil radius plus 4 mm. |
| P8 | The draw-wire reel was a solid block, and a drum centred under the exit would let the wire leave 30 mm away from the exit eyelet. | A printed housing (body with posts and a bearing boss, screwed lid), a 60 x 20 mm grooved drum on a 6 mm shaft in two bearings, a spring motor, a shaft magnet and the angle sensor board on the lid. The drum is set so its edge is under the exit: the housing centre moves 30.7 mm toward the rod; the wire exit point and the housing size are unchanged. | The wire leaves the drum vertically through the eyelet, as the error budget assumes. The housing still clears the rod by 32 mm and the 72 x 60 x 72 mm size of CNP-DDR-003 is kept. |
| P9 | The reel and the logger sat on the plate with no fixing. | Reel: four M4 countersunk screws up through the plate into heat-set inserts in the housing posts. Logger: a flanged IP65 box held by four M4 screws into tapped holes in the plate. | Nothing stands proud under the plate, so it still lies flat on the ground. |
| P10 | No cable joined the reel's angle sensor to the logger (review item of 2026-09-26). | BOM line 17: a 4-core cable through M12 glands on the reel and the logger, lying on the plate in two P-clips ($6). | The sensor cannot work without it; it lies clear of the rod hole and below the arm's path. |
| P11 | The coiled cable ended inside the logger lid with no entry. | Two M12 glands in the logger end wall that faces the rod, for the coiled pad cable and the reel cable. | Sealed entries for IP65 (R11). |
| P12 | The wire ended at the arm with no eye spring or stop drawn. | The wire passes up through the arm's eye, through the preloaded eye spring of BOM line 8 and into a crimped end stop. | Matches the snap-tension calculation [E5]. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Optional extension rod (BOM line 16) | M12 studs on both ends and a 20 mm OD x 40 mm coupling sleeve tapped M12 through; $15 to $16 | Two male-ended 16 mm rods cannot join without a sleeve, and a 16 mm rod is too thin to tap M12. The sleeve matches the cone diameter, so it follows the cone's hole. |
| Stroke and range | Stroke 928 to 939 mm, still limited by the wire arm on the reel; 850 mm usable unchanged [D1, D2] | P1, P6 |
| Depth error | Lean error at 850 mm after tilt correction 1.07 to 0.95 mm at 1° and 2.02 to 1.79 mm at 2° [E4] | Longer wire above the reel |
| Mass | Carried mass stays 15.7 kg; heaviest piece 9.83 kg [C2, C3] | Mass moves between parts; clamp 0.12 to 0.09 kg |
| Cost | Instrument $319 to $335; kit with both optional accessories $401, $1 over the $400 budget (register item) [L1] | Lines 6, 8, 14 and 16 repriced; line 17 added |
| Documents | CNP-CAL-001 v0.4, CNP-PRC-001 v0.6, CNP-REQ-001 v0.6; drawing CNP-DWG-001 Rev P5; making sketches CNP-DWG-101 to 113; build plan CNP-BLD-001; design decisions register CNP-DEC-001 | Follow the model. No requirement changes status. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | When the upper rod is unscrewed from the anvil for packing, the 8 kg hammer can slide off its lower end onto the user's feet. Keeping the anvil on the upper rod instead makes the heaviest piece about 11.3 kg, over the 10 kg of R10. | (a) a screw-on end cap on the upper rod's M12 stud whenever it is off the anvil; (b) pack with the anvil on the upper rod and relax R10's heaviest piece; (c) leave it to the user guidance. | (a): a cheap cap that also protects the thread. This adds to the safety case, so it is Amish's decision. |
| A2 | The kit with both optional accessories is $401, $1 over the $400 budget; the instrument alone is $335. | (a) keep the budget comparison on the instrument, as D2 and D10 already set; (b) trim an accessory price. | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CNP-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: 9 met, 2 at risk (R2, R11), 4 not verifiable at TRL 3 (CNP-CAL-001 v0.4).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept clamp, handle, pad and reel position; they need updating on Amish's Mac.
- Bought parts to confirm when ordered are in the register: the bubble level, spring motor, angle sensor board, flanged logger box, glands and band clamp.
