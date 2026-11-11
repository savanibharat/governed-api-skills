# ADR 0001 - Two-layer model (uber guards vs per-skill presentation)

Status: accepted (2026-11-09)

## Context
Every generated skill needs the same guards: injection defense, naming and validation limits,
output sanitization, language policy, metadata standard, and a safe renderer. Re-authoring them
per skill invites drift and quietly weakened guards.

## Decision
Separate the universal guards (the uber / federation layer, authored and audited once) from the
only genuinely per-skill concern: how this API's responses are shown.

## Consequences
Fix a guard once, regenerate, and every skill inherits it. Presentation stays per-skill. The
uber layer maps onto the federation plane rather than adding a new component.
