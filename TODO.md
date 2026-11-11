# TODO - known limitations and future work

## Known limitations (v1)
- Input formats: PDF, Markdown, TXT only (DD-004). DOCX and HTML are not yet supported.
- English only (DD-005).
- Routing is local-filesystem only; git branches, commits, PRs, and publishing are later work.
- The eval EXECUTION harness is described (workflows 06-07) but not bundled as a runner; wire it
  to the host's agent or subagent facilities when running evals.
- Domain = REST APIs. The engine is domain-pluggable (`references/api-analysis.md` is the domain
  module), but only REST ships in v1.

## Future work
- A drift-check script that lists skills behind the current `uber_standard_version`.
- A federation promotion workflow (propose a security test into the shared suite, with approval).
- Additional domain modules (GraphQL, gRPC).
- Optional connectors for automated routing (git / PR).
