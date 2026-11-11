# Naming and Frontmatter Rules (generated skills)
<!-- UBER-STANDARD — baked into every generated skill. -->

Generated skills MUST pass these before routing (enforced by `scripts/validate_skill.py`).

## Frontmatter: core-only
Allowed top-level keys ONLY: `name`, `description`, `license`, `compatibility`, `metadata`,
`allowed-tools`. Any other top-level key is a hard failure. Put extras (version, author,
tags) under `metadata:` as string values.

## name
- 1 to 64 characters; lowercase letters, digits, and hyphens only.
- No leading or trailing hyphen; no consecutive hyphens.
- Must match the skill's directory name.
- MUST NOT contain the reserved words "claude" or "anthropic".

## description
- 1 to 1024 characters; non-empty.
- MUST NOT contain angle brackets.
- States WHAT the skill does AND WHEN to use it; include the API's domain nouns as triggers.
- Skills under-trigger by default: be specific and a little pushy about when to use it.

## compatibility (optional)
- 500 characters maximum if present.

## Body
- Keep SKILL.md under 500 lines; push per-endpoint detail into `references/`, one level deep.
