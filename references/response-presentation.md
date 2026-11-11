# Response Presentation
<!-- Factory reference. Read during 05-generate-skill. Presentation is OPTIONAL per skill. -->

When a skill should show API results as Markdown, generate a **declarative mapping** — never a
hand-written script by default. The audited `uber-standard/render_markdown.py` primitive, baked
into the skill, interprets the mapping.

## The declarative mapping
Conforms to `schemas/presentation-mapping.schema.yaml`. It only selects fields and labels:
- `title`, then `sections`.
- A `fields` section (label/value pairs) or a `table` section (array -> rows, columns).
- `source` is a dotted JSON path; `path` selects within the section/row; `name: true` marks a
  name-like field (capped at 64 chars).

Only include fields present in the documented/example response schema — never invent columns.
The primitive also redacts secrets, truncates long values, escapes structural characters, and
is deterministic.

## The escape hatch (DD-003 — gated)
A bespoke Python renderer is permitted ONLY when a declarative mapping genuinely cannot express
a required layout. It requires, every time:
1. A written justification of why declarative is insufficient.
2. Human security review.
3. Sandboxed execution: deterministic, no network, reads stdin/args only.
4. An entry in `configuration/design-decisions.yaml`.
5. Its own adversarial eval.
Absent all five, use the declarative mapping.

## Default
Presentation defaults to off (return data plainly). Turn it on when a formatted view is wanted,
and set `metadata.presentation: "on"`.
