---
doc_id: CNP-PRC-001
title: ConePro design precis
project: ConePro
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# ConePro design precis

ConePro is a standard-geometry dynamic cone penetrometer (8 kg hammer, 575 mm drop, 20 mm 60 degree cone, as in ASTM D6951) with a draw-wire depth sensor referenced to a plate on the ground, a Hall-effect blow sensor at the anvil and a small BLE logger, so one person can run a test while the phone plots penetration against blows and exports the record. First-order numbers suggest about 45 J per blow, about 850 mm of penetration per lower rod, about 15 kg in total with the heaviest piece just under 10 kg, about 40 h of logging on three AA cells, and about $296 in parts, within the $400 budget. The concept does not yet warn when the rod leans (R6 not met), and depth accuracy, blow detection under shock and rod extraction are open.

![Hero render](../media/hero.png)

*Figure 1. ConePro set up at the start of a test, with a 1.75 m person for scale. The cone tip rests on the ground through the slotted reference plate and the hammer rests on the anvil.*

## How it works

1. **Set up.** The operator lays the slotted reference plate on the ground, stands the cone in the plate's center hole and clamps the draw-wire arm to the rod just below the anvil. The app zeroes the depth with the cone point at the surface.
2. **Drive.** The operator holds the handle, lifts the 8 kg hammer to the top stop and lets it fall 575 mm onto the anvil. Each blow drives the rod and cone further into the soil.
3. **Sense.** A magnet ring in the hammer face passes a potted Hall-effect sensor on the anvil as the hammer lands, which marks each blow. A draw-wire sensor on the plate measures how far the anvil clamp has moved down, which equals the cone's penetration because the rod is rigid and the plate stays on the ground surface.
4. **Log.** The logger on the plate reads depth at 100 Hz, waits for the rod to settle after each blow, and stores blow number, depth and time. It keeps the record even when no phone is connected.
5. **Show.** The phone app plots depth against blows, splits the curve into layers of near-constant slope, and gives each layer's DCP index (mm per blow) and an indicative CBR from the ASTM D6951 correlations, with the correlation named on screen. The user exports a CSV with time, location and notes.
6. **Extract.** After the test the operator removes the plate over its slot and pulls the rod out. The extraction method is an open decision (see Key design choices).

![Energy flow](../media/flow.png)

*Figure 2. Energy per blow from hammer to soil, in joules. All values are estimates; the split of losses in particular is not yet supported by calculation.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Cone | Hardened steel, 20 mm base, 60 degree point, threaded onto the rod | Replaceable; a worn cone biases results |
| 2 | Lower drive rod | 16 mm steel, 1,000 mm, engraved every 10 mm | Engraving is a manual backup scale |
| 3 | Anvil and coupler | Steel, about 64 mm diameter, threaded between the rods | Carries the Hall sensor pad |
| 4 | Drop hammer | 8.0 kg steel, about 100 mm outside diameter, 136 mm long | Magnet ring set in the lower face |
| 5 | Upper rod (hammer guide) | 16 mm steel, about 750 mm | Gives the 575 mm free drop |
| 6 | Handle and top stop | T-handle with a stop that fixes the drop height | |
| 7 | Reference plate | 300 x 300 x 8 mm aluminum, center hole and slot | Depth reference on the ground surface |
| 8 | Draw-wire depth sensor | Spring reel with a 12-bit magnetic angle sensor, about 1,000 mm stroke | Low-cost build; a bought industrial sensor is the fallback |
| 9 | Anvil clamp and wire arm | Split collar on the lower rod with an arm over the reel | Transfers rod movement to the wire |
| 10 | Hall-effect blow sensor | Potted sensor in a pad on the anvil | Shock survival is open (R11) |
| 11 | BLE logger | Microcontroller with BLE, flash storage, button and LED, three AA cells, IP65 box | Kept on the plate, away from impacts |
| 12 | Coiled sensor cable | Anvil sensor to logger, with a strain relief at each end | Follows the rod down during the test |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Blow energy and timing

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Potential energy per blow | about 45.1 J | 8.0 kg x 9.81 m/s² x 0.575 m |
| Impact speed | about 3.36 m/s | √(2 x 9.81 x 0.575) |
| Fall time | about 0.34 s | √(2 x 0.575 / 9.81) |
| Energy reaching the cone | about 33 J (about 74 %) | Assumed losses: guide friction 3 %, rebound and anvil 20 %, rod and side friction 5 % (Figure 2) |
| Mean dynamic soil resistance at 10 mm per blow | about 3.3 kN | 33 J / 0.010 m |
| Blow rate | about 24 per minute | One blow every 2.5 s by a practiced operator (assumed) |

### What the numbers mean for the user

The ASTM D6951 correlation for most soils is CBR = 292 / DCP^1.12, with DCP in mm per blow (separate correlations apply to lean and fat clays). Table 1 shows how sharply the indicative CBR changes at small penetrations, which is why depth accuracy matters most in stiff layers.

*Table 1. Indicative CBR from the ASTM D6951 general correlation.*

| DCP index (mm per blow) | 2 | 5 | 10 | 15 | 25 | 50 |
| --- | --- | --- | --- | --- | --- | --- |
| Indicative CBR (%) | about 134 | about 48 | about 22 | about 14 | about 8 | about 4 |

### Depth measurement

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Sensor resolution | about 0.05 mm per count | 12-bit angle sensor (4,096 counts per turn) on a reel of about 60 mm diameter (about 188 mm per turn) | R2 resolution met |
| Sensor accuracy, low-cost reel | about ±2 mm over 1,000 mm | Wire layering on the drum and spring stretch; to be calculated | R2 (±1 mm) at risk |
| DCP index error in a stiff layer | about ±10 % over 10 blows at 2 mm per blow; about ±4 % over a 50 mm layer | ±1 mm at each end of the interval | |
| Resulting CBR error | about ±11 % and ±4.5 % | CBR varies as DCP^-1.12 | |
| Plate settlement or heave | Not yet estimated | Plate bearing on soil disturbed by the driving | Open question |

### Range, mass and power

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Penetration per lower rod | about 850 mm | Clamp arm stops above the reel on the plate in the massing model | R5 met |
| Assembled height | about 1.88 m | Massing model | |
| Total mass | about 15.2 kg | Hammer 8.0, lower rod 1.6, anvil 1.4, upper rod 1.2, plate 1.7, handle 0.6, electronics and cable 0.7 | R10 (16 kg) met, thin margin |
| Heaviest piece | about 9.8 kg | Hammer captive on the upper rod with the handle | R10 (10 kg) met, thin margin |
| Reference test time | about 8 to 10 min | Setup 2 min; 57 blows at 2.5 s, about 2.4 min; extraction 3 to 5 min | R9 (12 min) at risk until extraction is chosen |
| Impact shock at the anvil | hundreds to a few thousand g | 3.36 m/s stopped in about 0.2 to 1 ms | R11 at risk |
| Average electronics current | about 50 mA | BLE microcontroller about 35 mA, angle sensor about 7 mA, Hall sensor and LED about 5 mA | |
| Battery life | about 40 h | About 2,000 mAh usable from three AA alkaline cells / 50 mA | R12 (8 h) met |

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Mechanical DCP (items 1 to 7) | about $165 | |
| Sensing and logging (items 8 to 12) | about $86 | |
| Carry bag, hardware and consumables | about $45 | |
| **Total** | **about $296** | R13 ($400) met |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Keep ASTM D6951 geometry.** Keeping the standard hammer, drop and cone lets users apply published correlations and compare with existing DCP data. A lighter hammer (the standard's 4.6 kg option) would help portability but halves the energy and suits only weak soils. Recommendation: 8 kg standard geometry, with the 4.6 kg option noted for later.
- **Depth referenced to a plate on the ground, measured by a draw-wire sensor.** Alternatives: a laser time-of-flight sensor on the plate aimed at a target under the anvil (cheaper and non-contact, but a few millimeters of noise and sensitive to dust and sunlight); a rotary encoder wheel running on the rod (no ground reference needed, but slips on a wet or muddy rod); or an accelerometer on the anvil integrated per blow (no reference at all, but drift makes millimeter accuracy unlikely). Recommendation: draw-wire, with the time-of-flight sensor as a cheaper fallback to compare at TRL 3.
- **Blow detection by Hall sensor, with the depth signal as a cross-check.** A blow is counted when the Hall sensor sees the hammer arrive and the depth steps down or stays still within 0.5 s. An accelerometer on the anvil would also detect blows and could measure tilt (see R6), but must survive the same shock. Recommendation: Hall sensor plus depth cross-check.
- **Verticality warning (R6, not met).** Options: (a) add a small accelerometer to the anvil sensor pad to read rod tilt between blows, which meets R6 but adds a shock-exposed part; (b) put a bubble level on the handle, which is cheap and robust but gives no record; (c) accept no tilt sensing and state it as a limitation. Recommendation: (a) with (b) as a backup. Proposed, awaiting Amish.
- **Electronics on the plate, not the rod.** The logger sits on the stationary plate so only the Hall sensor pad sees impacts. Proposed, awaiting Amish.
- **Non-lithium AA cells.** Three AA cells avoid lithium safety and shipping issues and are sold everywhere; a lithium-ion cell would be lighter and rechargeable. Recommendation: AA cells. Proposed, awaiting Amish.
- **Rod extraction.** Options: (a) a small lever or farm jack with a rod clamp (about $40 to $60 indicative, adds about 2 to 3 kg and pushes R10 over its limit unless carried separately); (b) upward hammer blows against the handle stop (no extra parts, but hard on the threads, the sensor pad and the operator's back); (c) a two-person twist-and-pull. Recommendation: (a), carried as a separate optional item. Not in the BOM cost. Proposed, awaiting Amish.
- **Complete instrument or retrofit kit.** The sensor set (items 8 to 12) could clamp to any existing 16 mm ASTM DCP, which would reach users who already own one for about $86 plus a bag. Recommendation: design the sensor set to fit standard DCPs from the start, and build the complete instrument for the prototype. Changes the pitch only slightly. Proposed, awaiting Amish.

## Safety

> **Safety:** ConePro drops an 8 kg steel hammer onto a steel anvil every few seconds and drives a pointed steel rod into the ground. Treat buried services, crushed fingers, flying fragments, noise and misuse of the results as hazards at every test point.

- **Buried services.** A rod driven 1 m into the ground can strike electric cables, gas pipes and water mains. Get a utility locate before every test (in the United States, call 811 or use the state one-call service) and do not test within the marked tolerance zone.
- **Crushed fingers and hands.** The hammer lands with about 45 J. Keep hands on the handle only, never on the anvil, the hammer's lower face or the clamp arm. The clamp arm and draw-wire must be placed so that fingers are never needed near the anvil during driving.
- **Flying fragments and mushrooming.** Repeated steel-on-steel impact can chip the anvil or hammer face and spall hardened steel. Wear safety glasses, inspect the anvil and hammer faces, and replace them when they mushroom or crack.
- **Noise.** Steel-on-steel impact is loud at close range. Hearing protection is recommended; the level is not yet estimated.
- **Lifting and posture.** The hammer is lifted about 57 times per test and the upper assembly weighs about 9.8 kg. Use a straight back and swap operators on long test days. Rod extraction is the most likely cause of back strain (see Key design choices).
- **Rod whip and tipping.** A leaning rod can bend or kick sideways when struck. Keep the rod vertical (R6) and stop if it deflects.
- **Sharp cone.** Cover the cone in transport.
- **Ground and site hazards.** Contaminated land, trench edges and traffic: follow site rules and do not test at the edge of an open excavation.
- **Misuse of results.** CBR values are indicative correlations. ConePro results must not be used on their own to design foundations or to decide that ground is safe to build on; they show where a qualified geotechnical engineer should investigate.
- **Batteries.** Alkaline AA cells carry little risk. If a lithium cell is chosen instead, it needs a protected cell and a charging procedure away from combustibles.

## Open questions for TRL 3

- Calculate the draw-wire error budget and decide between the low-cost reel and a bought sensor (R2).
- Estimate the shock at the anvil pad more carefully and choose a potting and mounting that survives it (R3, R11).
- Decide how to meet R6 (tilt sensing) and the extraction method (R9, R10).
- Estimate plate settlement or heave while driving, and how to detect it (for example a second reference point).
- Define the blow and depth data format and the layer-splitting method; check against TRL Overseas Road Note 8 practice.
- Confirm the cited prior work, standards and commercial prices online (not possible in this session).
- Choose the first co-design partner and site types.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
