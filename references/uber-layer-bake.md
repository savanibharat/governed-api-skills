# Baking the Uber Layer
<!-- Factory reference. Read during 05-generate-skill.md. Implements DD-002. -->

The uber standard (shared guards) is **baked into** each generated skill at generation time, so
the skill is self-contained and portable. A version stamp preserves fix-once governance.

## What gets baked, and where
- Into the skill's `SKILL.md` body: the short, non-removable **Safety** section (the core
  untrusted-data rule), see `templates/skill-template.md`.
- Into the skill's `references/`: copies of `injection-defense.md`, `output-sanitization.md`,
  `naming-validation.md` (and any other active uber-standard guard docs).
- Into the skill's `scripts/`: a copy of `render_markdown.py` when presentation is on.
- Into frontmatter `metadata.uber_standard_version`: the version baked in.

## Versioning & drift
- The uber standard's version is the single value in `uber-standard/VERSION` (start `1.0.0`).
- Each skill records the version it baked.
- A **drift check** compares each skill's stamp to the current version and lists skills that are
  behind. Updating a guard => bump the version => regenerate stale skills to propagate.

## Why bake rather than reference
A referenced central file breaks when a skill is carried into another repo or runtime, and
couples every skill to the federation checkout. Baking keeps skills portable and
confidentiality-safe; the version stamp gives back the "fix once, know who's stale" property a
reference would have given.

## Do not
- Do not let a per-skill need silently weaken a baked guard. Guard changes happen in the uber
  standard (proposed to federation, approved), then propagate by regeneration — never by hand
  editing a generated skill's baked copy.
