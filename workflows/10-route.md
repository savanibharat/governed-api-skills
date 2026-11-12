# 10 - Route
<!-- Place each artifact in its configured destination. Preserve everything else. -->

## Derive and verify routing first (references/routing-derivation.md)
Before placing anything: derive each artifact type's destination from the company's
routing-policy and repository-map docs and examples, recording the SOURCE of every placement
(routing provenance). Produce the dry-run plan (`templates/routing-plan.md`) and run the gates `scripts/check_routing.py`
(every artifact type must route to an enabled repo and a defined destination) and
`scripts/check_profile.py` (the active workspace profile is honored; when it forbids federation
writes, shared/federated artifacts are HOLD-ONLY - proposed and approval-gated, never auto-written). An uncovered type is a question, not a default. A FAIL blocks routing. Confirm the
plan before writing.

## Then route by artifact TYPE using `configuration/repository-topology.yaml` (the routing map) and the
policy in `configuration/artifact-routing.yaml`:
- generated skill -> project.skills
- project evals / regression tests -> project
- proposed shared standard or federated eval -> federation (APPROVAL REQUIRED - propose, never
  silently modify)
- MCP reference docs -> mcp
- skill registration (`templates/registration.yaml`) -> registry (points to source, no copy)

Rules: inspect existing files before writing; never overwrite unrelated content; never silently
overwrite a skill; on a missing or ambiguous destination, ask; record every generated or
modified file in the manifest. Cross-repo or shared writes that cannot be undone stop for
approval, even when running unattended.

Done: the user has a conformant skill, its evals and evidence, a traceability report, and a
registration - each in the right place.
