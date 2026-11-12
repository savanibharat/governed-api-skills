# 09 - Validate
<!-- Mechanical conformance gate before routing. -->

Run `scripts/validate_skill.py <skill_dir>` on the generated skill. It must pass: core-only
frontmatter; name rules (kebab-case, 64 max, no reserved words, matches the directory);
description rules (non-empty, no angle brackets, 1024 max); compatibility 500 max. Record the
result as the first line of evidence.

Then run the other mechanical gates, all of which must pass: `scripts/validate_artifacts.py
<skill_dir>` (schemas), `scripts/check_traceability.py <skill_dir>/traceability.yaml
<skill_dir>/evals/eval-suite.yaml`, `scripts/check_routing.py configuration`, `scripts/check_profile.py configuration` (the workspace
profile is honored), `scripts/check_eval_coverage.py <skill_dir>/evals/eval-suite.yaml`,
`scripts/check_drift.py` (baked guard version current), and `scripts/run_evals.py` (records the
deterministic evidence to `evaluations/results/`).

Also confirm against `configuration/evaluation-policy.yaml`: the mandatory suites are present,
the functional threshold is met, there is no unresolved critical adversarial failure, and
traceability is complete.

Only a skill that passes both the conformance gate and the policy proceeds to routing.

Next: `10-route.md`.
