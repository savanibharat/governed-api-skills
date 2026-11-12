# TODO - known limitations and future work

## Done since v1 (now enforced, not honor-system)
- Schema validation of generated artifacts (`scripts/validate_artifacts.py`).
- Traceability completeness gate (`scripts/check_traceability.py` + `schemas/traceability.schema.yaml`).
- Deterministic eval evidence (`scripts/run_evals.py` -> `evaluations/results/`).
- Unit tests for every script (`tests/`) and CI (`.github/workflows/ci.yml`).
- A complete worked example (`examples/`) that doubles as the test fixture.
- Isolated venv setup (no `--break-system-packages`).
- Gates in `RUN.md` labelled `[script]` vs `[agent]`; injection scanner demoted to advisory.

## Known limitations (v1)
- Input formats: PDF, Markdown, TXT only (DD-004). DOCX/HTML not yet supported, and PDF text
  extraction still relies on the host (no bundled extractor).
- English only (DD-005).
- Routing is local-filesystem only; git branches, commits, PRs, and publishing are later work.
- **Behavioral evals (functional/negative/adversarial) require an agent to execute the prompt.**
  `run_evals.py` records them as REQUIRES_AGENT; it does not fake a result. A full agent eval
  harness is future work.
- Domain = REST APIs. The engine is domain-pluggable (`references/api-analysis.md`), but only
  REST ships in v1.

## Future work
- An agent-driven eval harness so behavioral/adversarial evals produce recorded evidence too.
- A `check_drift.py` that lists skills behind `uber-standard/VERSION`.
- A bundled PDF text extractor.
- Additional domain modules (GraphQL, gRPC) and a git/PR routing connector.
- Choose and add a LICENSE for distribution.
