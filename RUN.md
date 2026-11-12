# RUN - start here
<!-- The one file. Do the one-time setup, then run the steps in order. Every step has a VERIFY
     gate, labelled by who enforces it. You never need to remember a command. -->

## One-time setup (one command)
From this folder:

    bash start.sh

That creates an isolated `.venv` (it does NOT touch system Python), installs the only
dependencies (pyyaml, jsonschema, pytest), and verifies the package. No other installs. No slash
commands to memorize.

## To run it
Tell Claude, in plain words - for example:

    Run governed-api-skills.
    Repositories: <skills-repo> <mcp-repo> <governance-repo>.
    Inputs are in <folder>.

Claude works the steps below from top to bottom and STOPS at any VERIFY that fails. (If you would
rather not run anything yourself, say so - Claude runs the setup and the checks for you.)

## How to read the gates
- **[script]** - mechanically enforced by a script; it fails hard on a violation.
- **[agent]** - carried out and judged by the agent, checked by an independent reviewer (a
  generator never signs off its own work). These are honest about needing judgement.

## The steps (one by one - each is verified)

**0. Preflight** - `workflows` start; gate: **[script]** `python scripts/preflight.py <inputs-folder>`
VERIFY: dependencies present; repo paths resolve; every input parses (OpenAPI / YAML / JSON);
company docs found.

**1. Ingest** - `workflows/01-ingest.md`
VERIFY **[agent]**: each document's role identified and recorded (`references/company-documents.md`);
inputs permitted on this machine. Plus **[script, advisory]** `scripts/scan_untrusted_doc.py` -
an advisory tripwire only; the real defense is treat-as-data + deterministic rendering, not this
scan.

**2. Analyze** - `workflows/02-analyze.md`
VERIFY **[agent]**: every endpoint, method, header, auth, request field, response, and error is
extracted WITH a source. Anything with source "none" is an unknown, never a default.

**3. Classify rules** - `workflows/03-classify-rules.md`
VERIFY **[agent]**: each company rule routed org-wide vs skill-specific; conflicts surfaced.

**4. Clarify** - `workflows/04-clarify.md`
VERIFY **[agent]**: no open unknown left silent - each is asked or recorded.

**5. Generate skill** - `workflows/05-generate-skill.md`
VERIFY **[script]** `scripts/validate_skill.py <skill>` (conformance),
`scripts/validate_artifacts.py <skill>` (evals/mapping/registration match the schemas),
`scripts/check_traceability.py <skill>/traceability.yaml <skill>/evals/eval-suite.yaml` (every
implemented requirement has a real source and an eval that exists), and
`scripts/check_instruction_provenance.py <skill> <openapi.yaml>` (every operation the skill
instructs is defined in the SOURCE OpenAPI spec, not just in the generator's references).
Plus **[agent]**: the instruction wording genuinely reflects the requirement (prose-only
instructions with no METHOD/path are a semantic gap the agent reviewer must cover).

**6. Generate evals** - `workflows/06-generate-evals.md`
VERIFY **[script]** `scripts/validate_artifacts.py` (eval schema) + **[agent]**: all four
categories present and each behavioral contract has an eval.

**7. Execute evals** - `workflows/07-execute-evals.md`
VERIFY **[script]** `scripts/run_evals.py` runs the deterministic subset and records real PASS/FAIL
to `evaluations/results/`. The behavioral evals are **[agent]**: an agent executes the prompt and
captures tool calls and side effects - a refusal alone is not a pass. Agent-judged evals are
recorded as REQUIRES_AGENT, never silently passed.

**8. Improve** - `workflows/08-improve.md` (only if step 7 failed)
VERIFY **[agent]**: fix the skill, never the sources; the failed eval AND the regression suite
re-run; history kept.

**9. Validate** - `workflows/09-validate.md`
VERIFY **[script]**: `validate_skill.py`, `validate_artifacts.py`, `check_traceability.py`,
`check_routing.py`, `check_profile.py`, `check_eval_coverage.py`, `check_drift.py`,
`check_instruction_provenance.py`, and `run_evals.py` all pass; plus the evaluation policy
(`configuration/evaluation-policy.yaml`).

**10. Route** - `workflows/10-route.md`
VERIFY **[script]** `scripts/check_routing.py configuration` (every artifact type routed to an
enabled repo) and `scripts/check_profile.py configuration` (profile honored; federated artifacts
hold-only). Plus **[agent]**: the routing plan (`templates/routing-plan.md`) shows a source for
every placement; you confirm; nothing unrelated is overwritten; federation writes wait for approval.

## Run all the mechanical gates at once
    bash verify.sh                 # tests + all gates + self-eval (this mirrors CI)
    python -m pytest -q            # just the self-tests
    python scripts/run_evals.py    # just the deterministic evidence -> evaluations/results/

CI runs the same steps on every push from `.github/workflows/ci.yml` (a hidden dot-folder; use
`ls -a` or enable "show hidden files" to see it).

## Done
You have the generated skill, its evals and evidence, a traceability report, and a routing plan -
each placed in the repo your own documents said it belongs in.

## If anything is red
The step that failed tells you exactly what. Nothing downstream runs until it is green. Remember:
passing the deterministic gates is necessary, not proof a skill is secure.
