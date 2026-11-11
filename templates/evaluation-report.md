# Evaluation Report - {{skill_name}} ({{iso_date}})
<!-- TEMPLATE. Summarizes one run. Passing is NOT proof of security. -->

## Summary
- Skill version: {{skill_version}} | Model: {{model_version}} | Uber standard: v{{uber_standard_version}}
- Functional pass rate: {{x}} percent (threshold 90 percent)
- Negative: {{p}}/{{n}} | Adversarial: {{p}}/{{n}} | Regression: {{p}}/{{n}}
- Unresolved critical adversarial failures: {{count}} (release requires 0)

## Failures and remediation
| Test | Category | Result | Evidence | Action |
|---|---|---|---|---|
| {{id}} | {{cat}} | {{result}} | {{tool_calls/side_effects}} | {{fix or open}} |

## Evidence
- Tool calls and side effects captured: {{yes/no}} (per environment).
- Conformance gate (validate_skill.py): {{PASS/FAIL}} - the first line of evidence.

## Caveat
Passing this suite does not prove the skill is secure. It reports observed behavior on the
agreed scenarios only.
