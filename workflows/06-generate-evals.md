# 06 - Generate evals
<!-- One eval per behavioral contract; four categories. -->

From `templates/eval-suite.yaml`, generate evals conforming to `schemas/evaluation.schema.yaml`:
- **functional** - the positive contract for each requirement.
- **negative** - the refuse-or-ask contract (missing mandatory data, undocumented fields,
  unauthorized endpoints).
- **adversarial** - from `references/security-test-catalog.md`, across BOTH surfaces (build-time
  ingested docs, runtime responses). State the payload; expect it treated as data; capture
  tool_calls and side_effects.
- **regression** - lock current passing behavior; a new failure becomes a new regression case.

Each eval names the requirement it verifies (provenance). Separate project-local evals from any
proposed federation / canonical evals.

Next: `07-execute-evals.md`.
