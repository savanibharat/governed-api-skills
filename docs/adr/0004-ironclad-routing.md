# ADR 0004 - Ironclad, provenance-based routing from company documents

Status: accepted (2026-11-10)

## Context
Companies supply several documents with different roles (best-practices, routing-policy,
repository-map) plus many examples, and multiple target repos (MCP, skills, a broader one). The
risk is mis-identifying a document's role or misrouting an artifact.

## Decision
- Identify each document's role explicitly at ingestion (never guess); surface conflicts.
- Derive routing from the routing-policy/repository-map docs and examples, recording the SOURCE
  of every placement (routing provenance). A placement with source "none" is a question.
- Enforce a closed set of artifact types; every one must be routed. No guessed defaults.
- Gate with `scripts/check_routing.py` (completeness + consistency) and a dry-run routing plan
  that is confirmed before writing. Federation/shared writes require approval.

## Consequences
Placement is explainable and verifiable, not guessed. An uncovered artifact type stops the run
with a question rather than landing in the wrong repo. Adds one reference, one template, one
script, and a routing-provenance discipline.
