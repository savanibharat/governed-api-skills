# 09 - Validate
<!-- Mechanical conformance gate before routing. -->

Run `scripts/validate_skill.py <skill_dir>` on the generated skill. It must pass: core-only
frontmatter; name rules (kebab-case, 64 max, no reserved words, matches the directory);
description rules (non-empty, no angle brackets, 1024 max); compatibility 500 max. Record the
result as the first line of evidence.

Also confirm against `configuration/evaluation-policy.yaml`: the mandatory suites are present,
the functional threshold is met, there is no unresolved critical adversarial failure, and
traceability is complete.

Only a skill that passes both the conformance gate and the policy proceeds to routing.

Next: `10-route.md`.
