# REST API Analysis
<!-- Factory reference. Read during workflows/02-analyze.md. This is the DOMAIN module:
     to support another API style later (GraphQL, gRPC), add a sibling analysis reference
     and leave the rest of the engine untouched. -->

Goal: extract a complete, source-backed picture of the API so the skill is built only from
what the documentation and examples actually say.

## Sources, in order of authority
1. An OpenAPI document (YAML or JSON) — the most structured source.
2. Request/response/error examples — concrete behavior the docs may not spell out.
3. Prose API docs (Markdown) — fill gaps the above leave.
Where sources disagree, do not pick silently: record the conflict and ask (see never-invent.md).

## Extract, per endpoint
- Method and path, with path parameters.
- Query parameters: name, required/optional, type, constraints.
- Headers, especially auth (scheme, where the token goes) and content type.
- Request body: schema, required fields, validation rules.
- Responses: success status + body schema; every documented error status, its meaning,
  and its body; rate-limit and retry behavior if documented.
- Any required call sequence or dependency between endpoints.

## Extract, across the API
- Authentication and authorization model (how a caller is identified and what scopes exist).
- Pagination, filtering, sorting conventions.
- Idempotency and side-effect semantics (which calls mutate state).

## Record each finding with its source
Every extracted fact carries a pointer to where it came from (doc section, example id, or
"none"). This feeds requirements-and-provenance.md. A fact with source "none" is an unknown,
not a default.
