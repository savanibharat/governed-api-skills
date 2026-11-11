# Routing Derivation - ironclad placement
<!-- Factory reference. Read during 10-route. Derives the repository topology + per-type routing
     from the company's routing-policy and repository-map documents and their examples, then
     proves it is complete and consistent before any write. -->

Goal: every artifact the factory produces has exactly one justified destination, traceable to a
company document or a consistent example. No artifact is ever placed on a guessed default.

## Artifact types (the closed set that MUST be routed)
generated_skill, project_evaluation, regression_test, adversarial_eval, federated_eval,
mcp_reference, skill_registration, evaluation_report, traceability_report,
proposed_shared_standard. This list lives in `configuration/artifact-routing.yaml:artifact_types`
and is enforced by `scripts/check_routing.py`.

## Steps
1. **Read** the routing-policy and repository-map docs (`references/company-documents.md`) and the
   routing **examples**. The company's repos are typically an MCP repo, a skills / project repo,
   and a broader repo (evals, standards, registry, governance).
2. **Derive** a destination (repo + path) for each artifact type. For each, record the SOURCE of
   the decision - the doc line or example id. This is ROUTING PROVENANCE.
3. **Cross-check** stated rules against examples. If an example contradicts a stated rule, do not
   choose - flag the conflict and ask.
4. **Write** the derived topology to `configuration/repository-topology.yaml` (schema-validated),
   and keep the provenance in the routing plan (`templates/routing-plan.md`).
5. **Gate** with `scripts/check_routing.py`: every artifact type routed; every target repo enabled;
   every destination key defined. A failure BLOCKS routing.
6. **Dry-run and confirm.** Produce the routing plan (artifact -> destination -> source -> action)
   and confirm before writing. Cross-repo or shared / federation writes that cannot be undone
   always require approval, even when running unattended.

## Ironclad rules
- No artifact type may be unrouted. If docs + examples do not cover a type, ASK - never default.
- Every placement cites its source. A placement with source "none" is not allowed; it is a question.
- Inspect before write; never overwrite unrelated content; never silently overwrite a skill.
- Federation / shared destinations are proposals requiring approval.
- The routing plan is recorded as evidence alongside the artifact manifest.
