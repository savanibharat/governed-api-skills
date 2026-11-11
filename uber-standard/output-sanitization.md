# Output Sanitization (rendered responses)
<!-- UBER-STANDARD — baked into every generated skill. Applied by render_markdown.py. -->

When rendering API responses to Markdown:

- Cap any displayed name-like field at 64 characters (append an ellipsis when truncated).
- Truncate any single value longer than 500 characters (configurable) and mark it truncated.
- Escape Markdown control characters and strip control and zero-width characters, so response
  data cannot alter document structure or smuggle hidden instructions.
- Never render secrets: fields whose key matches a secret pattern (authorization, token,
  password, secret, api key, bearer, set-cookie) are redacted to "[redacted]".
- Render only fields present in the documented or example response schema. Never invent columns.
- Output is deterministic: the same input plus the same mapping always produces the same Markdown.
