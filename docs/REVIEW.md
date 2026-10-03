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


## Session 2026-09-26: sources strengthened

Amish asked for the weaker sources in the README to be fixed. Every link kept or added was fetched and checked against the claim. No controlled document changed; `docs/01-problem.md` did not share any of the replaced sources.

| Where | Old source | New source |
| --- | --- | --- |
| Burning platform, subgrade sentence | Uncited claim that most roads to be built are gravel and earth | Rewritten to what Liu et al. (*Earth System Science Data* 18, 267) state: most unpaved roads are dirt |
| Burning platform, lab testing sentence | Uncited claim that CBR testing is slow and far away | Scala (1956) abstract on why road authorities skip strength tests, [TRID record](https://trid.trb.org/View/1194062) |
| Burning platform and United States row | Mn/DOT catalog page (does not carry the quoted text) | Mn/DOT *User Guide to the Dynamic Cone Penetrometer* PDF itself |
| South Africa row | Uncited (Kleyn 1975 report, no online record found) | Row replaced by Peru: Rural Access Index 37.2 %, World Bank *Measuring Rural Access: Update 2017/18* |
| Bangladesh row | World Bank 2017/18 update, plus an uncited claim about embankment roads | Same World Bank report, row limited to what it states (87 % in the 2016 pilot, highest of the pilot countries) |
| Australia row | Informit record alone, plus an uncited claim about unsealed networks | Row reframed as Australia and New Zealand; TRID record of the 1956 conference paper added beside Informit; unsealed-network claim removed |
| What sparked the idea | Mn/DOT guide only, with the I-94 and Albertville location unsupported by it | MnDOT MnROAD page added for the location; "to characterize the pavement foundations" trimmed to "during construction", as the guide states |

The inspiration event (Mn/ROAD construction and the Mn/DOT DCP user guide) is unchanged. No budget change.


## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; the render images themselves (`media/render-hero.png`, `media/render-exploded.png` and a detail view) are produced later from it.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 52 appearance parts (39 shell, 5 internal, 2 accessory, 6 context), with color, material, BOM line, group and explode offset for each, plus `TITLE` and three `RENDER_VIEWS` (hero, exploded, detail). It imports `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py`, so every main dimension and interface is unchanged. It adds:
  - filleted and chamfered steel parts: hardened cone, anvil with its coupler seam, top stop collar with its set screw;
  - rod graduations every 10 mm (heavier every 100 mm) on the lower rod;
  - a painted teal drop hammer with bare steel strike faces, six grip grooves, the ring of 16 magnets in the lower face and an "8.0 kg" label patch;
  - a powder-coated T-handle with a tee, ribbed rubber grips and a bubble level with a clear vial;
  - an anodized reference plate with rounded corners, zero-depth ticks round the hole and a nameplate;
  - a two-part draw-wire reel housing with a parting line, lid screws, a clear window onto a grooved drum, the wire exit eyelet and the wire;
  - a split clamp collar with its clamp screw, a filleted wire arm, the wire eye and the preload spring;
  - a potted sensor pad on an elastomer isolator, with the stainless band clamp and its worm housing;
  - a logger box with a parting line, lid screws, a clear lid window onto three AA cells in a holder, a teal button, a lit green status LED, a cable gland and a label;
  - a coiled sensor cable with a strain relief;
  - a spare cone and rubber cone cover (accessory, exploded view only);
  - context: a compact patch of soil with a few pebbles, and a phone lying on the ground showing a penetration curve.
- Self-check previews with the kit's matplotlib renderer (clear parts left out): `/tmp/conepro-prod/prev-hero.png`, `prev-exploded.png`, `prev-detail.png` (scratch files, not in the repo).
- `README.md`: hero image now points to `media/render-hero.png`, and an "Exploded render" link opens the links line.

### Where the appearance model differs from model.py

Each item is Proposed, awaiting Amish.

1. **Draw-wire drum drawn at 48 mm, not 60 mm.** A 60 mm drum (`drum_d`) cannot fit inside the 60 x 56 x 60 mm reel housing (`reel_box`) once it has walls, so the render shows a 48 mm drum. The calculations need the 60 mm drum (0.046 mm per count). Recommendation: keep the 60 mm drum and grow the housing to about 72 x 60 x 72 mm; that raises the reel top by 12 mm and cuts the stroke from 940 mm to about 928 mm, which still clears the 850 mm usable range.
2. **Reel housing and logger lid windows.** Both housings get a clear window so the drum and cells show in the renders. Recommendation: keep them as render features only and use opaque parts in the design unless Amish wants inspection windows, since each window adds a seal to an IP65 box.
3. **Hammer grip grooves and magnet pockets.** Six shallow grooves and 16 magnet pockets change the hammer mass slightly. Recommendation: accept; the BOM already says the mass is trimmed to 8.0 kg, so length is set at machining.
4. **Rubber grips on the T-handle.** Grips of about 33 mm diameter over the 26 mm tube are not in BOM line 6. The overall 260 mm width is unchanged. Recommendation: add grips to the BOM line 6 spec (a few dollars).
5. **Coiled cable path.** The cable keeps the model's end points and bend point but is drawn as a tight coil near the pad and a stretched coil below, and ends in a gland on the logger lid. Recommendation: accept as drawn.
6. **No cable from the reel to the logger.** Neither `model.py` nor the BOM shows how the angle sensor board in the reel reaches the logger, so none is drawn. Recommendation: add a short cable (or a connector on the plate) to BOM line 12 and to the model at the next update.

### TRL

This is an appearance model only: no tolerances, no fabrication detail, nothing past TRL 3. `trl` stays 3, and TRL 4 remains on hold.


## Session 2026-09-27: owner decision applied

Amish asked on 2026-09-27 to "resolve the challenges for ConePro, BridgePulse, Grainguard and WellSense". For ConePro that is item 1 of the 2026-09-26 session: the draw-wire drum drawn at 48 mm because the 60 mm drum did not fit its housing. Decided by Amish on 2026-09-27: keep the 60 mm drum and grow the reel housing to about 72 x 60 x 72 mm, accepting about 12 mm less stroke. Recorded in `docs/decisions/0003-reel-housing-size.md` (CNP-DDR-003 v0.1, new, added to `trl_evidence` in `project.yaml`).

### What changed

- `cad/src/model.py`: `reel_box` 60 x 56 x 60 mm to 72 x 60 x 72 mm. The reel exit point and every other dimension and interface are unchanged.
- `cad/src/product_model.py`: the 48 mm `DRUM_SHOWN` stand-in is removed; the drum is drawn from `drum_d` (60 mm) inside the larger housing, with the drum axis, window, window bezel and lid parting line resized to suit. 52 parts, all valid; no interference between drum and housing.
- `cad/step/`, `cad/stl/` regenerated; `cad/src/sheets.py` and `cad/drawings/CNP-DWG-001.*` Rev P2 to P3; `media/` concept media regenerated (`hero.png`, `concept-blueprint.*`, `exploded.png`, `flow.png`, `model.glb`, `viewer.html`).
- CNP-CAL-001 v0.3 (`docs/04-calcs/01-sizing.md`), CNP-REQ-001 v0.5, CNP-PRC-001 v0.5, `bom/bom.csv` line 8 (housing size stated), `bom/bom-notes.md`, `docs/pdf/` rebuilt.

### Result

- Reel top 66 to 78 mm above the ground. Stroke per lower rod 940 to 928 mm, still limited by the wire arm on the reel housing; the 850 mm usable range holds with a 78 mm margin [D1, D2]. R5 stays met.
- Knock-on from the shorter free wire: lean error at 850 mm after tilt correction 0.94 to 1.07 mm at 1 degree and 1.77 to 2.02 mm at 2 degrees [E4]; rigid-eye snap tension 41 to 283 N became 44 to 304 N, still limited to 9 to 35 N by the preloaded eye spring [E5]. R2 stays at risk.
- Cost ($319), carried mass (15.7 kg) and `budget_usd` ($400) unchanged. Requirement count unchanged: 9 met, 2 at risk (R2, R11), 4 not verifiable at TRL 3.

### Renders

The photoreal renders (`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`) need regenerating: YES, all three views. The reel housing is larger in every view, and the drum is now 60 mm (visible through the window in the hero and detail views and as a separate part in the exploded view). The render images were not regenerated in this session.

### Still Proposed, awaiting Amish

- Items 2 to 6 of the 2026-09-26 session (render-only windows, hammer grooves and magnet pockets, T-handle grips in BOM line 6, coiled cable path, reel-to-logger cable).
- O1: first co-design partner and user group.

### TRL

`trl` stays 3; TRL 4 remains on hold. No fabrication detail was added. No new safety concerns.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: design for construction and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept out of the build plan and in a separate design decisions register. He also wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session applies both to ConePro. `trl` stays 3; nothing was built or bought.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten to a constructable model: `build_components()` gives 39 separate parts and fixing sets; `build_parts()` fuses them into the BOM-numbered parts the calculations, drawing and concept media use; `python cad/src/model.py --check` runs 64 constructability checks (contacts, clearances, and no overlap between any two components). All 64 pass.
- New decision record `docs/decisions/0004-design-for-construction.md` (CNP-DDR-004 v0.1, Draft), made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `bom/bom.csv`: specs of lines 1 to 11, 14 and 16 now carry the joints and fixings; line 17 (reel-to-logger cable) added; `bom/bom-notes.md` updated.
- Calculations rerun: CNP-CAL-001 v0.4 (`docs/04-calcs/sizing.py` now also allows for the magnet recess and line 17); CNP-PRC-001 v0.6; CNP-REQ-001 v0.6. No requirement changes status: 9 met, 2 at risk (R2, R11), 4 not verifiable at TRL 3.
- STEP and STL regenerated; general arrangement CNP-DWG-001 Rev P4 to P5; concept media regenerated (`hero.png`, `concept-blueprint.*`, `exploded.png` now with the kit's own numbered callouts, `flow.png`, `model.glb`, `viewer.html`).
- `cad/src/build_plan_media.py` (new): overview, 13 making sketches (CNP-DWG-101 to 113, rods drawn as broken views), 10 joint close-ups, 13 step pictures, a plate hole layout and a block wiring diagram, all from the model.
- `docs/05-build-plan.md` (CNP-BLD-001 v0.1) and `docs/06-design-decisions.md` (CNP-DEC-001 v0.1) written; both added to `trl_evidence`; `design_state: constructable` in `project.yaml`; README links line and "Building the prototype" section added.

### Design changes made for construction (CNP-DDR-004)

1. Cone shoulder 5 to 12 mm, tapped M12 x 1.75, 14 mm deep (cone 29.3 mm overall); instrument 1,867 to 1,874 mm tall.
2. M12 studs on the rod ends and M12 tapped holes 24 mm deep in both anvil faces; every joint seats on a square shoulder.
3. Upper rod runs through the stop collar (6 mm roll pin, drilled at the set drop) and through the T-handle tube (welded); upper rod 776 mm above the anvil plus a 20 mm stud.
4. Bubble level is a 20 mm bullseye in a seat disc welded to the rod top.
5. Sixteen magnet pockets on an 82 mm circle, outside the anvil strike area, magnets 0.5 mm below the face; hammer 136.5 mm long to stay at 8.00 kg.
6. Clamp collar and arm cut in one piece from 12 mm aluminum plate (was a collar with an arm through the rod), with a saw slit and M5 clamp screw; its top now butts the anvil underside (was 4 mm below it), so the anvil carries it at every blow.
7. Sensor pad face curved on a curved 4 mm isolator; the band goes round the anvil and over the pad (it ran through the pad); cable strain relief boss.
8. Reel housing given walls, posts, a bearing boss, a screwed lid, a drum on a shaft in two bearings, a spring motor, shaft magnet and sensor board; the drum's edge is under the wire exit, so the housing centre moved 30.7 mm toward the rod (exit point and housing size unchanged).
9. Reel screwed to the plate from below into heat-set inserts; logger is a flanged box screwed to tapped plate holes.
10. Reel-to-logger cable added (BOM line 17, $6), with glands and two P-clips (closes item 6 of the 2026-09-26 session, subject to Amish's review of CNP-DDR-004).
11. Two M12 glands in the logger end wall for the coiled cable and the reel cable.
12. Wire through the arm eye, preload spring and a crimped end stop drawn.
13. Optional extension rod gets M12 studs and a 20 mm coupling sleeve ($15 to $16).

Knock-on numbers: stroke 928 to 939 mm (850 mm usable unchanged); lean error at 850 mm after tilt correction 1.07 to 0.95 mm (1°) and 2.02 to 1.79 mm (2°); rigid-eye snap tension 44 to 304 N became 42 to 284 N; driven mass 5.12 to 5.09 kg; carried mass 15.7 kg unchanged; heaviest piece 9.83 kg; instrument cost $319 to $335; kit with both optional accessories $401 ($1 over the $400 value-engineering target; instrument $65 under it).

### Proposed, awaiting Amish

All are in `docs/06-design-decisions.md`:

1. Accept CNP-DDR-004 as a whole.
2. Hammer can slide off the upper rod when it is unscrewed from the anvil; recommendation: a screw-on end cap on the stud (adds to the safety case).
3. Carried over: O1 co-design partner; render windows, hammer grip grooves, T-handle grips and coiled cable path (2026-09-26 items 2 to 5).

### Stale images (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` are stale: the clamp is now one piece against the anvil, the handle has a seat and bullseye level instead of a block level, the pad sits under its band, the reel housing sits 30.7 mm nearer the rod and the logger has flanges, glands and a second cable. `cad/src/product_model.py` needs the same updates before they are rendered again.

### Safety

No new hazard in the product. The build adds welding (handle) and lathe work on hardened steel, covered by the build plan's safety stops. The packing hazard of the hammer sliding off the upper rod is listed as open decision 2.

### Recommended next step

Amish reviews CNP-DDR-004 and the open decisions in the register. TRL 4 remains on hold; when it is released, the build plan is the starting point for the bench build.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." Nothing was built or tested; TRL 4 remains on hold.

### Decisions recorded

7 decisions moved from "Open decisions" to "Decisions made" in the design decisions register, dated 2026-10-02. Design for construction (CNP-DDR-004) accepted with one exception (no thread locker on the rod, anvil and cone joints) and its item A1 (end cap on the upper rod); a low-volume road agency named as the first co-design partner to approach; render-only windows, hammer grip grooves, T-handle grips and the cable path accepted.

### Documents changed

- `docs/01-problem.md` (CNP-PRB-001 v0.4)
- `docs/02-concept.md` (CNP-PRC-001 v0.8)
- `docs/05-build-plan.md` (CNP-BLD-001 v0.2)
- `docs/06-design-decisions.md` (CNP-DEC-001 v0.3)
- `docs/decisions/0001-trl2-review-decisions.md` (CNP-DDR-001 v0.3)
- `docs/decisions/0002-recommendations-accepted.md` (CNP-DDR-002 v0.2)
- `docs/decisions/0004-design-for-construction.md` (CNP-DDR-004 v0.3)
- `README.md` (not a controlled document)
- `bom/bom-notes.md` (not a controlled document)
- `docs/pdf/`: every controlled document re-rendered.

### Follow-up actions to carry approved decisions into the design

The model, drawings, build plan pictures, BOM quantities and prices, and calculations were not changed in this session. These actions carry the approved decisions into them:

1. Decision 1 (model): Add spanner flats to the rods (and the anvil and cone if needed) in cad/src/model.py so the joints can be tightened with spanners now that no thread locker is used; re-run the constructability checks.
2. Decision 1 (drawings): CNP-DWG-001 and the making sketches of the rods, anvil and cone (CNP-DWG-101 to 104): add the spanner flats; remove any thread-locker note.
3. Decision 1 (pictures): Build plan pictures of joints 1 and 2 and steps 1, 3 and 6: remove any thread-locker callout and show the spanner flats.
4. Decision 2 (model): Model the screw-on end cap for the upper rod's M12 stud and the label position on the hammer.
5. Decision 2 (bom): Add the end cap and the hammer label to BOM line 14 and price them.
6. Decision 2 (calcs): CNP-CAL-001: add the end cap's mass to the packed mass and heaviest-piece checks (R10); a few grams.
7. Decision 2 (pictures): Build plan pictures: show the end cap in step 5 and in the packing stop S6.
8. Decision 5 (drawings): Hammer making sketch: add the grip grooves and the note that the length is set at machining to keep 8.00 kg.
9. Decision 5 (model): Add the grip grooves to the hammer in cad/src/model.py and adjust its length to keep 8.00 kg.
10. Decision 6 (bom): BOM line 6: add rubber grips of about 33 mm diameter and reprice the line.
11. Decision 6 (model): Add the rubber grips to the T-handle in the model and the appearance model.
12. Decision 4 (pictures): At the next render session on Amish's Mac, keep the windows render-only and redraw the renders, card and social preview to the constructable design (clamp, handle, pad and reel position).

### Points found in the review

Raised when the recommendations were written (2026-10-01) and not yet acted on:

- The value-engineering section compares the kit with both optional accessories (USD 401) against the USD 400 target; the like-for-like figure is the instrument at USD 335, USD 65 under.
- The build plan applies medium thread locker to joints that must be undone for packing (upper rod to anvil) and for disposable cones, which conflicts with routine disassembly.
- Renders and appearance model still show the concept clamp, handle, pad and reel position.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out ("APPROVED CHANGES, COMPLETE THESE"). Nothing was built or tested; TRL 4 remains on hold.

### Follow-ups

1. Decision 1 (model): done. Spanner flats in `cad/src/model.py`: 17 mm across on the top 10 mm of the cone shoulder (3.4 mm wall left to the tapping drill), 13 mm across and 20 mm long on the lower rod 8 mm above its bottom shoulder, 55 mm across and 17 mm long on the anvil 3 mm above its bottom face (2 mm below the sensor pad). The upper rod has no flats: it is turned by its T-handle. New checks added; 73 checks, 0 failed. STEP and STL regenerated.
2. Decision 1 (drawings): done. CNP-DWG-001 Rev P6 (flats, no thread locker, grooves, grips, end cap in the notes); CNP-DWG-101, 102 and 104 at Rev P2 with the flats and no thread-locker note (CNP-DWG-103, the clamp, has no rod joint and is unchanged).
3. Decision 1 (pictures): done. Joints 1 and 2 and steps 1, 3 and 6 redrawn: no thread locker, flats shown and named.
4. Decision 2 (model): done. `end_cap()` in `cad/src/model.py` (aluminum, 32 mm diameter x 24 mm, tapped M12 21 mm deep, fluted grip); checks for the cap on the stud, the hammer resting on it and the cap 10 mm wider than the hammer bore; `hammer-assembly.step` and `.stl` now show the packed state with the cap. The hammer label is modeled (25 x 50 mm, front face, above the grooves).
5. Decision 2 (BOM): done. Line 14 adds the end cap (about USD 4) and the label (about USD 1): USD 18 to USD 23.
6. Decision 2 (calcs): done. End cap 0.045 kg in the packed and heaviest-piece masses (CNP-CAL-001 v0.6, [C1] to [C4]); packed hammer assembly 810 mm long.
7. Decision 2 (pictures): done. Step 5 shows the end cap going on; a new picture, `docs/05-build-plan/packing-s6.png`, shows it at safety stop S6.
8. Decision 5 (drawings): done. CNP-DWG-105 Rev P2: three grip grooves 6 mm wide and 2 mm deep, length set at machining to keep 8.00 kg, label position.
9. Decision 5 (model): done. Grooves in the model; the derived hammer length grows from 136.5 mm to 138.0 mm to keep 8.00 kg, so the upper rod is 778 mm above the anvil (798 mm cut), the stop collar 713.0 mm and the pin hole 722.0 mm above the shoulder, and the instrument 1,875 mm tall. CNP-DWG-106 and 107 Rev P2 carry the new lengths.
10. Decision 6 (BOM): done. Line 6 adds two closed-end rubber grips about 33 mm across (about USD 3 each): USD 20 to USD 26.
11. Decision 6 (model): done. Grips (33 mm OD, 100 mm long) on the tube ends in `cad/src/model.py`, with fit checks, and ribbed grips in the appearance model; CNP-DWG-108 Rev P2 and joint 5 show them.
12. Decision 4 (renders): not done: the photoreal renders, card and social preview are made on Amish's Mac. The appearance model is ready for it (below).

### Appearance model and render scenes

`cad/src/product_model.py` now builds on the constructable parts of `cad/src/model.py`: the one-piece clamp and arm, the pinned stop collar and welded T-handle with the 33 mm grips, the curved pad under its band, the reel at its constructable position (drum edge under the exit), the flanged logger with its glands, the grooved hammer with its label, the spanner flats, and the end cap lying beside the plate. The windows in the reel lid and logger lid stay render-only, as decided. Views kept: hero, exploded, detail. Scenes exported to `/home/claude/renders/conepro` (one .npz and .json per view and `conepro__jobs.json`). No photoreal images, card or social preview were made.

### Key results

- No requirement changed status: 9 met, 2 at risk (R2, R11), 0 not met, 4 not verifiable at TRL 3.
- R10: carried mass 15.7 kg to 15.8 kg (grips 0.08 kg, end cap 0.04 kg); heaviest piece 9.83 kg to 9.96 kg, **only 0.04 kg under the 10 kg limit**. Any further mass on the hammer assembly breaks R10.
- R13: value-engineering target: USD 400. Estimated cost of the constructable design: USD 346 (USD 54 under the target). The kit with both optional accessories is USD 412 (USD 12 over).
- Small knock-on changes in CNP-CAL-001 from the heavier handle: driven mass 5.14 kg, 27.9 J at the cone, isolated pad peak about 542 g.

### Documents changed

- `cad/src/model.py`, `cad/src/sheets.py`, `cad/src/build_plan_media.py`, `cad/src/concept_media.py`, `cad/src/product_model.py`; `cad/step/`, `cad/stl/`
- `cad/drawings/CNP-DWG-001` Rev P6; `CNP-DWG-101`, `102`, `104`, `105`, `106`, `107`, `108` Rev P2 (others regenerated unchanged)
- `docs/05-build-plan/`: overview, joints 1, 2 and 5, steps 1, 3, 5, 6 and 13, new `packing-s6.png` (all pictures regenerated)
- `media/`: hero, concept blueprint, exploded, flow, model.glb
- `docs/04-calcs/sizing.py` and `docs/04-calcs/01-sizing.md` (CNP-CAL-001 v0.6)
- `docs/03-requirements.md` (CNP-REQ-001 v0.8)
- `docs/02-concept.md` (CNP-PRC-001 v0.9)
- `docs/05-build-plan.md` (CNP-BLD-001 v0.3)
- `docs/06-design-decisions.md` (CNP-DEC-001 v0.4)
- `bom/bom.csv`, `bom/bom-notes.md`, `README.md` (not controlled documents)

### Cross-repo actions

None.

### Safety

The end cap and the hammer label carry decision A1 into the design; safety stop S6 now has its own picture. With no thread locker, the joint check before each test (S4) is the only guard against a joint working loose.

### Recommended next step

Render session on Amish's Mac from the exported scenes (hero, exploded, detail), then card and social preview.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## 2026-10-03: decisions recorded

Amish decided on 2026-10-03: "TIght Margins - i accept the margins". For ConePro this is the heaviest piece at 9.96 kg against the 10 kg limit of R10 (0.04 kg margin).

- `docs/06-design-decisions.md` (CNP-DEC-001) and `docs/03-requirements.md` (CNP-REQ-001) updated.
