# Requirement Traceability - {{skill_name}}
<!-- TEMPLATE. Every normative instruction traces to a source.
     Provenance values: documented | inferred | unknown. -->

| Requirement | Source | Provenance | Generated instruction | Eval | Result |
|---|---|---|---|---|---|
| REQ-GET-CUSTOMER | API guide section 2 | documented | Call GET /customers/{id} with bearer token | FUNC-001 | PASS |
| REQ-CREATE-REQUIRES-VENDOR | error example | documented | Reject create without vendor_id | NEG-001 | PASS |
| 403 behavior | none | unknown | Ask the user; recorded as an open question | - | INCONCLUSIVE |

## Open questions / unknowns
- {{each undocumented behavior recorded as ask-or-unknown, with the point where a decision is needed}}

## Coverage
- Mandatory requirements with a source: {{x}}/{{n}}
- Mandatory requirements linked to an eval: {{x}}/{{n}}
