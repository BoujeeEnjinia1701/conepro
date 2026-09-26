# Review note: ConePro

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CNP-PRB-001 v0.2): problem, prior work (ASTM D6951, Scala, Kleyn, US Army Corps, TRL Overseas Road Note 8, PANDA), users, what ConePro does and does not give, constraints, out of scope, open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (CNP-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets and a status column, a reference test and assumptions.
- `docs/02-concept.md` (CNP-PRC-001 v0.2): how it works, numbered components, blow energy, CBR sensitivity, depth error, range, mass, test time, shock, power and cost estimates, design choices with options, safety, open questions.
- `cad/src/concept_media.py`: massing model of a standard DCP (cone, rods, anvil, 8 kg hammer, handle) with the reference plate, draw-wire sensor, anvil clamp, blow sensor, logger and cable, each with a BOM number; 1.75 m scale figure. It redraws the exploded view with leader lines, because the kit's on-part callouts hid the small sensor parts on a 1.9 m tall assembly, and it removes the renderer's temporary `media/_views*` folders.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png`, `flow.png` (energy per blow, all values labeled as estimates), `model.glb` and `viewer.html`. No cutaway: the parts are solid or simple annular steel pieces, and the hero and exploded views already show how they fit.
- `bom/bom.csv`: 14 lines with indicative USD prices, lines 1 to 12 numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line inserted before "## Problem"; problem, concept, key components and safety text brought in line with the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Energy per blow | about 45.1 J, about 33 J at the cone | R1 (standard geometry) met |
| Penetration per lower rod | about 850 mm | R5 met |
| Depth resolution and accuracy | about 0.05 mm resolution; about ±2 mm accuracy for a low-cost reel | **R2 at risk** (±1 mm target) |
| Total mass, heaviest piece | about 15.2 kg, about 9.8 kg | R10 met, thin margins |
| Reference test time (850 mm, 57 blows) | about 8 to 10 min | **R9 at risk** until extraction is chosen |
| Impact shock at the anvil | hundreds to a few thousand g | **R11 at risk** |
| Battery life, three AA cells | about 40 h | R12 met |
| Parts cost | about $296 | R13 ($400) met; `budget_usd` unchanged |

Requirements not met or at risk:

- **R6 (verticality warning) not met:** the concept has no tilt sensing on the rod.
- **R2 (depth ±1 mm) at risk:** a low-cost draw-wire reel may reach only about ±2 mm.
- **R3 (blow detection) and R11 (shock) at risk:** the Hall sensor pad sits on the anvil.
- **R9 (test time) at risk:** depends on the extraction method, which is open.

### Proposed, awaiting Amish

Status update: items 1 to 8 were Decided by Amish, 2026-09-25: go with recommendation (CNP-DDR-001, D1 to D8). Item 9 has no recommendation and remains Proposed, awaiting Amish.

1. **Verticality (R6).** (a) accelerometer in the anvil sensor pad; (b) bubble level on the handle; (c) accept no tilt sensing. Recommendation: (a) with (b) as a backup.
2. **Rod extraction.** (a) optional lever or farm jack with a rod clamp, about $40 to $60, carried separately; (b) upward hammer blows; (c) two-person pull. Recommendation: (a), outside the BOM total. Adding it would bring parts to about $336 to $356, still within budget.
3. **Complete instrument or also a retrofit sensor kit** for existing 16 mm ASTM DCPs (about $86 of sensing and logging parts). Recommendation: design the sensor set to fit standard DCPs and build the complete instrument for the prototype. This widens the pitch slightly; `project.yaml` is unchanged.
4. Depth sensing by draw-wire referenced to a ground plate, with a laser time-of-flight sensor as the fallback.
5. Standard 8 kg hammer geometry rather than the 4.6 kg option.
6. Blow detection by Hall sensor with a depth cross-check.
7. Electronics on the plate rather than on the rod.
8. Three AA cells rather than a lithium-ion cell.
9. First co-design partner and user group.

`project.yaml` pitch and problem were left unchanged: the findings do not make them wrong. The problem line says "soil bearing data"; the docs make clear ConePro gives a strength index and indicative CBR, not allowable bearing pressure.

### Safety concerns

- Buried services struck by the rod: utility locate before every test.
- Crushed fingers between the 8 kg hammer and the anvil or clamp arm (about 45 J per blow).
- Chipping and mushrooming of hardened steel faces: eye protection and face inspection.
- Impact noise (level not estimated) and back strain from lifting and extraction.
- Misuse of indicative CBR results for foundation design.

### Problems and gaps against the brief

- **Sources not checked online.** Web search was unavailable in this session (search budget used up and page fetches blocked), so prior work is cited from the literature by author, title and report number, with a link only for ASTM D6951. Commercial prices for instrumented penetrometers were not checked and are described only qualitatively. Confirm all citations at TRL 3.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to calculate the draw-wire error budget, anvil shock, blow energy transfer and mass roll-up, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved the TRL 2 review on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session ran `/advance-trl3` and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CNP-DDR-001 v0.1): the eight TRL 2 items with a recommendation recorded as "Decided by Amish, 2026-09-25: go with recommendation" (D1 to D8); the co-design partner (O1) left open.
- `docs/04-calcs/01-sizing.md` (CNP-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: geometry, blow energy, mass, range, draw-wire error budget, tilt error, wire slack dynamics, magnet field, shock, tilt, storage, test time, extraction force, power and cost, with a results table for R1 to R15. The script imports the model and the BOM and prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (ASTM geometry, derived hammer length and upper rod, plate, reel, clamp and arm, band-clamped sensor pad, logger, cable). Exports `cad/step/` and `cad/stl/` for `conepro-assembly`, `hammer-assembly`, `drive-train` and `sensor-set`.
- `cad/src/sheets.py` and `cad/drawings/CNP-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, front, top and right views at 1:20, detail A (anvil, sensor pad and clamp) at 1:5, isometric view and a dimension table, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps CNP-DWG-010, so DWG-001 was free.
- `bom/bom.csv`: 15 lines, all priced, with supplier types; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now renders from `model.py`; `media/` refreshed (hero, blueprint, exploded, flow with the new energy split, GLB and viewer). All images were inspected; no `media/_views*` folders remain.
- CNP-PRB-001, CNP-PRC-001 and CNP-REQ-001 revised to v0.3; `project.yaml` at `trl: 3`, `trl_target: 3` with the evidence files; `README.md` updated. Pitch, problem and `budget_usd` ($400) unchanged, since the review recommended no change to them.
- Citations checked online: ASTM D6951 geometry and the CBR correlations, Scala (1956), Webster, Grau and Williams (GL-92-3, DTIC ADA251960), ORN 8 and PANDA were confirmed. Kleyn's report number was wrong (L2/74); it is L2/75, now corrected. The ORN 8 title and publisher (TRRL) were corrected. Scala's volume and issue number were not confirmed. Commercial prices for instrumented penetrometers are still unchecked.

### Requirements summary (CNP-CAL-001)

7 met, 2 at risk, 2 not met, 4 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| **R5** | **Not met** (1,000 mm clause) | 938 mm stroke, 850 mm usable; no extension rod in the BOM |
| **R10** | **Not met** (total mass) | 16.7 kg carried in the bag against 16 kg; heaviest piece 9.8 kg and packed length 1.08 m are met |
| R2 | At risk | Bench error ±0.98 mm worst case, ±0.49 mm RSS against ±1 mm; a 2 degree lean adds up to 1.8 mm at 850 mm |
| R11 | At risk | About 1,400 to 5,400 g mean at the anvil; about 533 g on the isolated pad; cable and connector fatigue not calculated |
| R1, R4, R6, R8, R9, R12, R13 | Met | 8.00 kg and 575 mm; record at 0.21 s; tilt ±0.3 degree; 830 tests; 8.1 to 11.7 min; 40 h; $321 |
| R3, R7, R14, R15 | Not verifiable at TRL 3 | Blow sequence, app and retrofit fit need hardware |

Other findings: about 27.6 J reaches the cone, not 33 J as estimated at TRL 2; the impact at the anvil is thousands of g, not hundreds; the draw-wire goes slack for 5 to 36 ms after each blow, and with a rigid eye the snap tension could reach 291 N at 50 mm per blow, near or above the breaking load of the wire.

### Decisions recorded (CNP-DDR-001)

D1 accelerometer tilt sensing with a bubble level backup; D2 optional lever extraction, outside the BOM total; D3 sensor set designed to fit standard DCPs, complete instrument for the prototype; D4 draw-wire depth with a time-of-flight fallback; D5 standard 8 kg geometry; D6 Hall blow detection with cross-checks; D7 electronics on the plate; D8 three AA cells. The SwapCell cross-cutting decisions do not apply (ConePro uses AA cells).

### Proposed, awaiting Amish

Status update: items 2 to 5 are now Decided by Amish, 2026-09-25: go with recommendation (CNP-DDR-002, D9 to D12; see the next session). Item 1 has no recommendation and remains Proposed, awaiting Amish.

1. **First co-design partner and user group (O1).** No recommendation; to be picked per area later.
2. **R10 mass (new).** (a) a 0.40 kg bag, an aluminum clamp and arm, and a 6 mm plate, giving about 15.7 kg; (b) redefine R10 to exclude the bag (15.9 kg); (c) relax R10 to 17 kg. Recommendation: (a).
3. **R5 extension rod (new).** (a) add a 500 mm extension rod (about $15, 0.79 kg; total 16.4 kg even with item 2a, so R10 fails again); (b) relax R5 to 850 mm per rod and offer the extension rod as a separately carried accessory; (c) a longer lower rod (breaks the 1.1 m packed length). Recommendation: (b).
4. **Draw-wire reel details (new).** A metal single-layer grooved drum, a groove keeper and a preloaded eye spring (8 N, 2 N/mm), already in BOM line 8, and a usable range of 850 mm because of the tilt error near the end of the stroke. Recommendation: accept; the alternative is the bought industrial draw-wire sensor at higher cost.
5. **Stiff ground extraction (new).** The upper bound on the pull force is 5.5 kN at 5 mm per blow, beyond the 3 kN lever. Recommendation: note the disposable-cone practice for stiff ground in the user guidance; no hardware change now.

### Safety concerns

- Buried services struck by the rod: utility locate before every test.
- Crushed fingers between the hammer and the anvil; the sensor pad sits 8 mm under the hammer overhang, a new pinch point.
- Chipping and spalling of hardened steel faces under impacts of thousands of g: eye protection and face inspection.
- Strong magnets in the hammer (implanted medical devices) and a draw-wire that can whip if it breaks.
- Impact noise (level not estimated), back strain from lifting, and extraction forces that can exceed 3 kN in stiff ground.
- Misuse of indicative CBR results for foundation design.

### Problems and gaps

- No existing TRL 4 material was found (no tests, build procedures or firmware); `build-log/README.md` is the scaffold only.
- R3, R7, R14 and R15 cannot be shown on paper. The magnet field ignores the steel hammer, and the restitution, isolator and wire-stretch values are assumptions.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. The next step is for Amish to decide items 1 to 5 above, after which CNP-REQ-001 and the BOM can be revised within TRL 3. For the record, TRL 4 would need: a bench build of the instrument, a test plan and report (TST, `environment: lab`) covering the draw-wire error against a steel rule, a 200-blow detection sequence, a 10,000-blow drop count on the sensor pad, tilt accuracy, battery life and timed trials, a firmware and app sketch, and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now Decided by Amish, 2026-09-25: go with recommendation, recorded in `docs/decisions/0002-recommendations-accepted.md` (CNP-DDR-002 v0.1). The work stayed at TRL 3.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| D9 | R10 mass, option (a): 6 mm plate, aluminum clamp and arm, 0.40 kg bag | 16.7 kg carried (plate 1.72 kg, steel clamp 0.34 kg, bag 0.80 kg); R10 not met | 15.7 kg carried (plate 1.29 kg, aluminum clamp 0.12 kg, bag 0.40 kg); R10 met, thin |
| D10 | R5, option (b): 850 mm per rod, extension rod as a separate accessory | R5 required 1,000 mm with an extension rod; no rod in the BOM; not met | R5 restated to 850 mm per rod; BOM line 16, optional 500 mm rod ($15, 0.79 kg); met |
| D11 | Draw-wire reel details and 850 mm usable range | Proposed | Accepted; BOM line 8 unchanged |
| D12 | Stiff-ground extraction: disposable-cone practice in user guidance | Proposed | Stated in CNP-PRC-001 (How it works, Safety); no hardware change |

Knock-on numbers from CNP-CAL-001 v0.2: instrument cost $321 to $319 (kit with lever and extension rod $384); stroke 938 to 940 mm; driven mass 5.35 to 5.12 kg; energy at the cone 27.6 to 28.0 J; isolated pad peak 533 to 543 g; `budget_usd` stays $400 (no change was recommended).

Files changed: `cad/src/model.py` (plate 6 mm, aluminum clamp), `cad/step/`, `cad/stl/`, `cad/src/sheets.py` and `cad/drawings/CNP-DWG-001.*` (Rev P1 to P2), `cad/src/concept_media.py` and `media/`, `docs/04-calcs/sizing.py` and CNP-CAL-001 v0.2, CNP-REQ-001 v0.4, CNP-PRC-001 v0.4, CNP-DDR-001 v0.2, new CNP-DDR-002 v0.1, `bom/bom.csv` (16 lines), `bom/bom-notes.md`, `project.yaml` (evidence list only), `README.md`, `docs/pdf/`.

README: added "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" before "Problem". The inspiration point is the Mn/ROAD test road construction in Minnesota (more than 700 DCP tests, two-person crew recording each blow on a form, per the Mn/DOT DCP user guide). `docs/01-problem.md` did not attribute the idea to any review, so it was left unchanged. PDFs, drawings and media were regenerated with the designmolecule.com footer.

### Requirement status (CNP-REQ-001 v0.4)

9 met, 2 at risk, 0 not met, 4 not verifiable at TRL 3 (was 7 met, 2 at risk, 2 not met, 4 not verifiable).

| ID | Status | Key number |
| --- | --- | --- |
| R2 | At risk | Bench ±0.98 mm worst case against ±1 mm; up to 1.8 mm more at 850 mm with a 2 degree lean |
| R11 | At risk | About 543 g at the isolated pad; cable, connector and isolator fatigue not calculated |
| R1, R4, R5, R6, R8, R9, R10, R12, R13 | Met | R5: 850 mm per rod; R10: 15.7 kg; R13: $319 |
| R3, R7, R14, R15 | Not verifiable at TRL 3 | Need hardware or the app |

### Still Proposed, awaiting Amish

1. **First co-design partner and user group (O1).** No recommendation; to be picked per area later.

### Cross-repo actions

None. No ConePro decision needs a change in another repo.

### TRL 4

TRL 4 remains on hold by Amish's instruction. The TRL 4 work these decisions imply (weighing the kit, fitting the extension rod and checking re-zero, stiff-ground extraction trials, plus the bench tests listed in the previous session) is decided in principle but not started.

### Safety

No new hazards. The extension rod adds one more joint to check before driving; the stiff-ground guidance tells the operator to stop rather than force the lever.

