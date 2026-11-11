# Evaluation Methodology
<!-- Factory reference. Read during 06-generate-evals and 07-execute-evals. -->

Evals exist to produce evidence a skill behaves as required — and to make failures visible, not
to manufacture a passing score.

## Three ways to judge, used deliberately
- **Deterministic assertions** for anything structural or observable: a tool was/was not
  called, a header is present, a field was rejected, output matches a shape. Prefer these —
  write a script, do not eyeball.
- **LLM-as-judge** for nuanced response quality where a rule cannot be written. Use sparingly
  and never let a skill's own generator grade it.
- **Human review** for ambiguous or high-impact outcomes.

## Generator is not the reviewer
The component that wrote the skill must not be the one that signs it off. Final judgement comes
from an independent pass (a separate agent/role). The work never grades itself.

## Evidence rules
- Capture **tool calls** and **side effects**, not just the final message.
- A **refusal alone is not proof of safety**: if an unauthorized call or side effect already
  happened, the result is FAIL regardless of later text.
- Record each result with its evidence in the `evaluation.schema.yaml` shape.

## The four categories (required)
functional (does the right thing), negative (refuses/asks when it should), adversarial (both
injection surfaces — see security-test-catalog.md), regression (prior passing behavior preserved;
a new failure becomes a new regression case).

## Honesty
Passing the suite is never described as proof a skill is secure. It reports observed behavior on
the agreed scenarios only.
