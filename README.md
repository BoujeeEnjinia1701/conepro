# ConePro

**Area:** Situational Field Hardware · **Status:** Concept · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

Portable dynamic cone penetrometer with a digital depth encoder and blow counter that logs penetration curves to a phone.

## Problem

Early site assessments need soil bearing data, but lab geotech is slow.

## Concept

Portable dynamic cone penetrometer with a digital depth encoder and blow counter that logs penetration curves to a phone.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Hardened steel rod and cone
- 8 kg drop hammer
- Linear encoder or laser rangefinder
- Hall-effect blow counter
- BLE logger

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Confirm utility locates before driving any rod into the ground.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CNP-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CNP-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
