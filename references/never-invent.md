# Never Invent API Behavior
<!-- Factory reference. The epistemic backbone. Read during 02-analyze and 04-clarify. -->

The factory must always know WHY it believes something about the API, and label it. Inventing
behavior to make a skill look complete is the failure mode this guards against.

## Five states for any claim about the API
1. `documented` — stated in the API docs or OpenAPI.
2. `example-supported` — shown by a supplied request/response/error example.
3. `inferred` — a reasonable deduction from documented facts, not directly stated.
4. `user-approved-assumption` — an inference the user has explicitly confirmed.
5. `unknown` — neither documented, exampled, nor safely inferable.

## Rules
- Build instructions freely from `documented` and `example-supported` facts.
- You MAY use `inferred`, but label it; prefer to confirm it and promote to
  `user-approved-assumption`.
- NEVER turn `unknown` into an instruction. Example: docs describe 401 but say nothing about
  403 — do not invent 403 handling. Record it as a question or an open gap.
- Never modify the source docs or invent a business rule to make an eval pass.

## When you hit an unknown
Record it in the requirement's `open_question`, and either ask now (see clarification-bank.md)
or, when running unattended, record it and proceed with the rest, surfacing it in the report.
