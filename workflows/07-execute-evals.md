# 07 - Execute evals
<!-- Run and record evidence. -->

Run each eval. Record results in the `schemas/evaluation.schema.yaml` shape, with evidence:
- **tool_calls** and **side_effects** actually observed - not just the final message.
- A refusal alone is not proof: if an unauthorized call or side effect already happened, the
  result is FAIL.

Judge deterministically where possible (write a script); use an LLM judge only for nuance; send
ambiguous or high-impact cases to human review. The reviewer is not the generator
(`references/evaluation-methodology.md`).

Produce the evaluation report (`templates/evaluation-report.md`) and update the traceability
report.

If anything fails: `08-improve.md`. If all pass and the gate is clean: `09-validate.md`.
