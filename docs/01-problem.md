---
doc_id: CNP-PRB-001
title: ConePro problem statement
project: ConePro
doc_type: Problem statement
version: "0.3"
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
  change: Populate to TRL 2 (users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Citations checked online and corrected (Kleyn report number, ORN 8 title); retrofit question closed by CNP-DDR-001 (D3)
---

# ConePro problem statement

Early site assessments need soil strength data within the hour, but laboratory geotechnical testing takes days to weeks, and the fast field alternative, the manual dynamic cone penetrometer (DCP), needs two people, a steel rule and a clipboard, and produces hand-written records that are slow to reduce and easy to get wrong. ConePro aims to keep the standard DCP test and remove the manual reading and transcription.

## The problem

The DCP is a simple, well-established field test. An 8 kg hammer dropped 575 mm drives a 20 mm, 60 degree cone into the ground on a 16 mm steel rod, and the penetration per blow (the DCP index, in mm per blow) gives a profile of soil strength with depth. ASTM D6951/D6951M standardizes the apparatus and method for shallow pavement applications and gives correlations from the DCP index to the California Bearing Ratio (CBR) ([ASTM D6951/D6951M-18](https://www.astm.org/d6951_d6951m-18.html)). The method goes back to Scala's cone penetrometer for pavement design in Australia (Scala 1956, "Simple methods of flexible pavement design using cone penetrometers," *New Zealand Engineering* 11 (2); [Informit record](https://search.informit.org/doi/10.3316/informit.218423931293630)), was developed for road assessment in South Africa (Kleyn 1975, *The use of the Dynamic Cone Penetrometer (DCP)*, in Afrikaans, Transvaal Roads Department, Pretoria, Report L2/75), and was adopted by the US Army Corps of Engineers for rapid airfield and road assessment (Webster, Grau and Williams 1992, *Description and Application of Dual Mass Dynamic Cone Penetrometer*, USACE Waterways Experiment Station, Instruction Report GL-92-3, [DTIC ADA251960](https://apps.dtic.mil/sti/tr/pdf/ADA251960.pdf)). The UK Transport and Road Research Laboratory published a program and manual for analyzing DCP data for roads in developing countries (Overseas Road Note 8, *A users manual for a program to analyse dynamic cone penetrometer data*, TRRL, 1990; [record](https://transport-links.com/fcdo-publications/orn8-a-users-manual-for-a-program-to-analyse-dynamic-cone-penetrometer-data-dos-version)).

The weak point is the reading. In the manual method, one person drops the hammer and a second reads the rod position against a separate rule after each blow or set of blows, then the record is typed up and reduced by hand or in a spreadsheet. That makes the test slow, needs two trained people, and introduces reading and transcription errors, which matter most in stiff layers where the penetration is only a few millimeters per blow.

Instrumented and automated penetrometers exist. Examples include variable-energy penetrometers that record the energy and penetration of every blow (the PANDA variable-energy penetrometer developed at Blaise Pascal University and sold by Sol Solution, France; [manufacturer literature](https://www.insitutek.com/products/panda-instrumented-dcp/)) and vehicle- or trailer-mounted automated DCPs. They are built for professional survey teams, are closed, and cost many times the $400 prototype budget (estimate; prices were not checked in this session). There is no open, low-cost, standard-geometry DCP with automatic depth and blow logging that a small contractor, NGO engineer or student can build, audit and repair.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Site engineer or technician at a small contractor or municipality | A quick, recorded strength profile for subgrade, trench backfill or a pad before work starts | Road edges, building plots, trenches; one person on site |
| NGO or humanitarian engineer | Screen ground for shelters, water tanks, latrines and access tracks where no lab is within reach | Remote sites, no reliable grid or cell signal, heat and dust |
| Low-volume road agency staff | Layer strengths along a road to plan gravel and drainage, in line with DCP-based design practice | Rural roads, many test points per day |
| Student or researcher | An open instrument and data format to study DCP correlations and soils | Teaching labs, field courses |

## What the user gets, and what they do not

ConePro gives a DCP index profile and an **indicative** CBR profile from the published correlations. It does not give an allowable bearing pressure for foundation design. Correlations from DCP results to bearing capacity exist but are soil-specific and scattered, so ConePro results are for screening and for deciding where proper geotechnical investigation is needed, not a substitute for it.

## Constraints

- Garage-buildable prototype, about $400 USD in parts, using machined or bought steel parts and off-the-shelf electronics modules.
- Keep the ASTM D6951 mechanical geometry (8 kg hammer, 575 mm drop, 16 mm rod, 20 mm 60 degree cone) so results can be compared with published correlations and existing DCP data.
- One person must be able to carry, set up and run a test.
- Works with no cell signal: data stays on the logger and the phone until the user exports it.
- Electronics must survive steel-on-steel impacts every few seconds, rain, dust and 0 to 45 °C.

## Out of scope

- Allowable bearing pressure or foundation design.
- Static cone penetration testing (CPT) with pushing rigs.
- Cloud services; the phone app exports files only.
- Motorized hammer lifting.

## Open questions

- Which user group to co-design with first (small contractors, an NGO shelter or water team, or a low-volume road agency)? Proposed, awaiting Amish; co-design partners are to be picked per area later.
- Build complete instruments, or also offer the sensor set as a retrofit? Decided by Amish, 2026-09-25 (CNP-DDR-001, D3): design the sensor set to fit standard DCPs, and build the complete instrument for the prototype.
- The sources above were checked online on 2026-09-25 (ASTM D6951 geometry and correlations, Scala, Kleyn, Webster and others, ORN 8, PANDA). Commercial prices for instrumented penetrometers are still unchecked.
