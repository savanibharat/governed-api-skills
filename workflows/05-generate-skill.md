# 05 - Generate skill
<!-- Build the skill from requirements + contracts. Bake the uber layer. -->

From `templates/skill-template.md`, produce the generated skill:
- Core-only frontmatter; name kebab-case, 64 chars max, no reserved words, matches the directory;
  description states what plus when, with the API's domain nouns as triggers.
- Body: the safety section, how it uses the MCP tool, endpoints (push per-endpoint detail into
  `references/`, loaded on demand), business rules each with a source, and unknowns recorded as
  ask / unknown.
- Every normative instruction traces to a REQ (`references/requirements-and-provenance.md`).

Bake the uber layer (`references/uber-layer-bake.md`): copy the active uber-standard guard docs
into the skill's `references/`, inline the safety section, stamp
`metadata.uber_standard_version`, and copy `render_markdown.py` into the skill's `scripts/` when
presentation is on.

Presentation (optional): if on, generate a declarative mapping from
`templates/presentation-mapping.yaml` (`references/response-presentation.md`). Only documented
fields.

## Verify (script-enforced)
Run on the generated skill; all must pass before continuing:
`scripts/validate_skill.py <skill>`, `scripts/validate_artifacts.py <skill>` (evals/mapping/
registration match the schemas), and `scripts/check_traceability.py <skill>/traceability.yaml
<skill>/evals/eval-suite.yaml` (every implemented requirement has a real source and a real eval),
and `scripts/check_instruction_provenance.py <skill>` (every operation the skill instructs is
documented in its references).

Next: `06-generate-evals.md`.
