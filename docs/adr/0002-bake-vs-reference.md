# ADR 0002 - Bake the uber layer into each skill (with a version stamp)

Status: accepted (2026-11-10)

## Context
The uber guards can be baked into each skill at generation, or referenced from a central file.

## Decision
Bake from the central source and stamp `metadata.uber_standard_version`. A drift check lists
skills that are behind the current version.

## Consequences
Skills stay self-contained and portable across repos and runtimes - a reference would break when
a skill is moved and would couple it to the federation checkout. Propagation requires
regeneration; the version stamp makes staleness visible.
