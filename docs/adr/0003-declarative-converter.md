# ADR 0003 - Declarative presentation, gated bespoke scripts

Status: accepted (2026-11-10)

## Context
JSON-to-Markdown rendering could be a per-skill generated script, or a declarative mapping
interpreted by one audited primitive.

## Decision
Declarative mapping by default (`uber-standard/render_markdown.py`). A bespoke script is a gated
escape hatch: written justification, human review, sandboxed execution, registration in
`design-decisions.yaml`, and its own adversarial eval.

## Consequences
No freshly generated code executes by default, shrinking the security and maintenance surface.
Exotic layouts remain possible under the gate.
