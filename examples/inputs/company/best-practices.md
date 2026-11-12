# Engineering Best Practices (Acme)

- All API calls use Bearer authentication; the token goes in the Authorization header.
- Customer email is PII. Do not log it, and do not display it unless the user explicitly asks.
- Skills operate in English only.
- Redact secrets (tokens, keys) in any output.
- Every mandatory requirement must be covered by a test before a skill is approved.
