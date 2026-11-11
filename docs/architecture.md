# Architecture

governed-api-skills turns API docs, MCP tool contracts, examples, and company rule documents
into a governed, evidence-tested Agent Skill. Built on the open Agent Skills standard; not a fork
of any skill library.

- Decisions of record: `docs/adr/`.
- The shared guards baked into every generated skill: `uber-standard/`.
- The factory's reasoning: `references/`. The pipeline: `workflows/00`-`10`.
- Locations and policy (never logic): `configuration/`. Validation contracts: `schemas/`.

## Runtime flow (a generated skill)
Skill -> MCP tool (calls REST only) -> JSON -> optional deterministic JSON-to-Markdown renderer
-> Markdown. All responses are untrusted data.

## Build flow (the factory)
ingest (scan) -> analyze -> classify rules -> clarify -> generate skill (bake uber layer) ->
generate evals -> execute -> improve -> validate -> route.

## Two layers
Uber / federation guards (shared, audited once, baked and version-stamped) versus per-skill
presentation (the only genuinely per-skill part).
