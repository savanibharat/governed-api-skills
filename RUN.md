# RUN - start here
<!-- The one file. Do the one-time setup, then run the steps in order. Every step has a VERIFY
     gate. You never need to remember a command: just tell Claude to run governed-api-skills. -->

## One-time setup (one command)
From this folder:

    bash start.sh

That installs the only two dependencies (pyyaml, jsonschema) and verifies the package. Done.
No other installs. No slash commands to memorize.

## To run it
Tell Claude, in plain words - for example:

    Run governed-api-skills.
    Repositories: <skills-repo> <mcp-repo> <governance-repo>.
    Inputs are in <folder>.

Claude then works the steps below from top to bottom and STOPS at any VERIFY that fails. (If you
would rather not run anything yourself, just say that - Claude runs the setup and the checks for
you.)

## The steps (one by one - each is verified)

**0. Preflight** - `scripts/preflight.py <inputs-folder>`
VERIFY: python deps present; repo paths resolve; every input parses (OpenAPI / YAML / JSON);
company docs found. Fix anything marked FIX before continuing.

**1. Ingest** - `workflows/01-ingest.md`
VERIFY (input): each document's role identified and recorded (`references/company-documents.md`);
`scripts/scan_untrusted_doc.py` reviewed; inputs permitted on this machine (workspace profile).

**2. Analyze** - `workflows/02-analyze.md`
VERIFY (API): every endpoint, method, header, auth, request field, response, and error is
extracted WITH a source. Anything with source "none" is an unknown, never a default.

**3. Classify rules** - `workflows/03-classify-rules.md`
VERIFY: each company rule routed org-wide vs skill-specific; conflicts surfaced, not guessed.

**4. Clarify** - `workflows/04-clarify.md`
VERIFY: no open unknown left silent - each is asked or recorded.

**5. Generate skill** - `workflows/05-generate-skill.md`
VERIFY (output): `scripts/validate_skill.py` PASS; every instruction traces to a REQ; the uber
layer is baked and version-stamped.

**6. Generate evals** - `workflows/06-generate-evals.md`
VERIFY: functional + negative + adversarial (both surfaces) + regression present; each
behavioral contract has an eval.

**7. Execute evals** - `workflows/07-execute-evals.md`
VERIFY (behavior): tool calls and side effects captured; a refusal alone is not a pass; the
thresholds in `configuration/evaluation-policy.yaml` are met.

**8. Improve** - `workflows/08-improve.md` (only if step 7 failed)
VERIFY: fix the skill, never the sources; the failed eval AND the regression suite re-run;
history kept.

**9. Validate** - `workflows/09-validate.md`
VERIFY: the conformance gate and the evaluation policy both pass.

**10. Route** - `workflows/10-route.md`
VERIFY (placement): `scripts/check_routing.py` PASS; the routing plan
(`templates/routing-plan.md`) shows a source for every placement; you confirm; nothing unrelated
is overwritten; federation writes wait for approval.

## Done
You have the generated skill, its evals and evidence, a traceability report, and a routing plan -
each placed in the repo your own documents said it belongs in.

## If anything is red
The step that failed tells you exactly what. Nothing downstream runs until it is green.
