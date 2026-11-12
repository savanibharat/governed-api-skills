# Routing Plan - customer-api (2026-11-11)
<!-- Dry-run placement, each line justified by a company document or example. No source "none". -->

| Artifact | Type | Destination (repo/path) | Source (doc / example) | Action | Approval |
|---|---|---|---|---|---|
| customer-api skill | generated_skill | skills-repo/.claude/skills/customer-api | routing-policy + EX-01 | create | - |
| customer-api evals | project_evaluation | skills-repo/evaluations/customer-api | routing-policy + EX-02 | create | - |
| regression tests | regression_test | skills-repo/tests/skill-behavior | routing-policy | create | - |
| MCP usage doc | mcp_reference | mcp-repo/documentation/customer-api.md | repository-map + EX-04 | create | - |
| registration | skill_registration | governance-repo/registrations/customer-api.yaml | repository-map + EX-03 | create | - |
| proposed injection test | proposed_shared_standard | governance-repo/test-suites | best-practices + EX-05 | propose | REQUIRED |

## Completeness
- Artifact types routed: 6 shown / 10 defined (the rest route by the same topology).
- Unrouted types: none (check_routing.py: PASS).

## Conflicts / open questions
- None. (REQ-403 is an API unknown, recorded in traceability.yaml - not a routing gap.)
