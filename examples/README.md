# Worked example - customer-api

A complete, verifiable run of the factory, used both as a demo and as the test fixture.

## inputs/
What a user supplies: an OpenAPI spec (`customer-api.openapi.yaml`), request/response/error
examples (`examples/`), the three company documents (`company/`: best-practices, routing-policy,
repository-map) and routing examples, and the MCP tool contract (`mcp/`).

Note two deliberate traps the factory must handle correctly:
- 403 is **not** documented - it must be recorded as unknown, never invented.
- `email` is PII - it must be omitted from rendered output.

## expected/customer-api/
What a correct run produces: a generated skill with core-only frontmatter, baked uber-standard
guards (`references/`), the endpoint contract, a presentation mapping (email omitted), an eval
suite (all four categories), a structured `traceability.yaml`, a `registration.yaml`, and a
`routing-plan.md`.

## Verify it
From the package root, with the venv active:

    python scripts/validate_skill.py examples/expected/customer-api
    python scripts/validate_artifacts.py examples/expected/customer-api
    python scripts/check_traceability.py examples/expected/customer-api/traceability.yaml examples/expected/customer-api/evals/eval-suite.yaml
    python scripts/run_evals.py

The self-test suite (`python -m pytest -q`) runs all of the above against this example.
