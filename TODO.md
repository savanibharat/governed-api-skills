# TODO - known limitations and future work

## Done since v1 (now enforced, not honor-system)
- Schema validation of generated artifacts (`scripts/validate_artifacts.py`).
- Traceability completeness gate (`scripts/check_traceability.py` + `schemas/traceability.schema.yaml`).
- Deterministic eval evidence (`scripts/run_evals.py` -> `evaluations/results/`).
- Unit tests for every script (`tests/`) and CI (`.github/workflows/ci.yml`).
- A complete worked example (`examples/`) that doubles as the test fixture.
- Isolated venv setup (no `--break-system-packages`).
- Gates in `RUN.md` labelled `[script]` vs `[agent]`; injection scanner demoted to advisory.

## Done in v1.2 (review-2 fixes)
- Renderer: redacts secrets nested inside object values; neutralizes URLs (code span) so they can't autolink.
- Path resolution: `check_routing.py` and `preflight.py` resolve config/repo paths from the package/project, not the cwd.
- Validator: tolerates CRLF; checks metadata values are strings and the body is under 500 lines; `skill-template.md` reordered so it is a valid exemplar.
- Preflight: missing enabled repo is a FIX (not a note); parses YAML inputs too.
- `check_drift.py` (baked guard version), `check_profile.py` (workspace profile enforced, allow-but-hold), `scan_output.py` (verbatim-laundering tripwire), `check_eval_coverage.py` (coverage policy). All wired into `run_evals.py` (13/13 deterministic) and the gates.

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

## Done in v1.4 (review-4 fixes)
- Closed the drift escape hatch: a folder with any generated-skill marker (guards, stamp, traceability.yaml, registration.yaml, evals/) that is missing a guard or stamp now FAILS (can't be hidden by deleting the guard + stamp).
- Instruction-provenance now checks against the SOURCE OpenAPI spec (case-insensitive, URL-aware, path-param normalized), closing the "document the bogus op in references" evasion. Prose-only instructions remain a semantic (agent) gap.
- Removed the unused `references/UBER_VERSION` decoy.
- Added a visible `verify.sh` (runs tests + all gates + self-eval). CI lives at `.github/workflows/ci.yml` - a hidden dot-folder; use `ls -a` or enable "show hidden files".

## Done in v1.3 (review-3 fixes)
- Drift now hash-checks baked guard FILES (catches hand-edits) and flags unstamped skills, not just the version stamp.
- `check_traceability.py` requires the eval suite (a missing suite is now an error, not a silent pass).
- New `check_instruction_provenance.py`: flags HTTP operations instructed by SKILL.md that aren't documented in the skill's references (a tripwire against untraced/laundered operations).

## Future work
- An agent-driven eval harness so behavioral/adversarial evals produce recorded evidence too.
- A semantic instruction-to-requirement matcher (current provenance check is operation-level only).
- A bundled PDF text extractor.
- Additional domain modules (GraphQL, gRPC) and a git/PR routing connector.
- Choose and add a LICENSE for distribution.
