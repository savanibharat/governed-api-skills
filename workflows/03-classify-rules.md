# 03 - Classify rules
<!-- Split company rules into org-wide vs skill-specific. -->

For each rule extracted from the company rule documents, classify it:
- **org-wide** - a policy that should hold for every skill (for example "never log PII", or an
  auth standard).
- **skill-specific** - a rule about this API only.

Route:
- skill-specific rules shape this skill directly (they become requirements and contracts).
- org-wide rules are **proposed** for the uber / federation standard. Never silently modify a
  shared standard - propose with justification; a human approves (see `10-route.md`).

When a rule is ambiguous (org-wide or specific?) or two rules conflict, do not choose silently -
ask (stage 04) or record it as an open gap.

Next: `04-clarify.md`.
