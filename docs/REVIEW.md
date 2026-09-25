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
