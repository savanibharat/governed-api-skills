# Requirements and Provenance
<!-- Factory reference. Read during 02-analyze, 05-generate-skill, 06-generate-evals. -->

The differentiator: every normative instruction in a generated skill can be traced back to a
source and forward to the eval that verifies it. Evidence, not assertion.

## A requirement record
Give each requirement an id (REQ-...) and capture:
- statement: what must be true (e.g. "create requires vendor_id").
- source: doc section, example id, company rule doc, or "none".
- provenance: one of `documented`, `example-supported`, `inferred`, `user-approved-assumption`,
  `unknown` (see never-invent.md).
- generated_instruction: the skill text that implements it.
- eval: the test id that verifies it.
- result: the latest eval result.
- open_question: present when provenance is `unknown` or a conflict is unresolved.

## The traceability report
Fill `templates/traceability-report.md` from these records. Coverage targets (see
`configuration/evaluation-policy.yaml`): every mandatory requirement has a source, and every
mandatory requirement is linked to an eval.

## Rules
- Never write a normative instruction with no requirement behind it.
- `inferred` and `user-approved-assumption` are allowed but must be labeled as such — they are
  not the same as `documented`.
- A requirement whose provenance is `unknown` does not become an instruction; it becomes a
  question or a recorded gap.
