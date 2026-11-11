# Clarification Question Bank
<!-- Factory reference. Read during 04-clarify.md. Ask only what the sources leave open;
     do not interrogate the user about things the docs already answer. -->

Ask when information is incomplete, contradictory, or `unknown` (never-invent.md). When running
unattended, record the question as an open gap and proceed with the rest, surfacing it in the
report. Prefer specific, answerable questions over open-ended ones.

## Authentication & authorization
- Which auth scheme, and where does the credential go (header name, scheme)?
- What scopes/permissions does each endpoint require?
- Behavior for 401 vs 403 if the docs cover only one?

## Endpoints & sequences
- Is there a required call order or dependency between endpoints?
- Pagination/filtering/sorting conventions?
- Which calls mutate state (side effects), and are any idempotent?

## Requests & validation
- Which request fields are mandatory vs optional?
- Validation rules the docs imply but do not state?

## Errors & limits
- Documented error statuses and their meanings beyond what examples show?
- Rate-limit and retry behavior?

## Business rules (from company rule docs)
- When two rules conflict, which wins?
- Is this rule org-wide (propose to federation) or specific to this API?

## MCP tool
- Which exposed tool fronts this endpoint, and what are its argument names?
- Does the tool handle auth, or must the skill supply it?

## Presentation & routing
- Should responses be rendered to Markdown (presentation on/off)? Which fields matter?
- Destination repos for skill, evals, registration — and is federation write approved?

## Confidentiality
- Are these inputs permitted on this machine under the active workspace profile?
