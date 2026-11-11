# Routing Plan - {{project}} ({{iso_date}})
<!-- TEMPLATE. The dry-run placement, each line justified by a company document or example.
     No line may have source "none". Confirm before writing; federation needs approval. -->

| Artifact | Type | Destination (repo/path) | Source (doc / example) | Action | Approval |
|---|---|---|---|---|---|
| customer-api skill | generated_skill | skills-repo/.claude/skills/customer-api | routing-policy sec 2 | create | - |
| customer-api evals | project_evaluation | skills-repo/evaluations/customer-api | example EX-03 | create | - |
| mcp usage doc | mcp_reference | mcp-repo/documentation/customer-api | repository-map | create | - |
| proposed injection test | proposed_shared_standard | governance-repo/test-suites | best-practices | propose | REQUIRED |
| registration | skill_registration | governance-repo/registrations/customer-api | repository-map | create | - |

## Completeness
- Artifact types routed: {{x}}/{{total}} (check_routing.py: {{PASS/FAIL}})
- Unrouted types: {{none | list}} (any unrouted type is a QUESTION, not a default)

## Conflicts / open questions
- {{stated rule vs example mismatches, ambiguous document roles, uncovered artifact types}}
