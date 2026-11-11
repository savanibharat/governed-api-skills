# Metadata Standard (generated skills)
<!-- UBER-STANDARD — baked into every generated skill. -->

Generated skills carry these keys under frontmatter `metadata:`. Per the Agent Skills spec,
`metadata` is a map from string keys to string values — every value below is a string.

| key | meaning |
|---|---|
| uber_standard_version | version of the uber standard baked in (the drift-check key) |
| generated_by | "governed-api-skills" |
| generated_at | ISO-8601 date of generation |
| source_api | identifier of the API the skill targets |
| provenance | relative path to the traceability report |
| presentation | "on" or "off" (whether JSON to Markdown rendering is enabled) |

Example:

```yaml
metadata:
  uber_standard_version: "1.0.0"
  generated_by: "governed-api-skills"
  generated_at: "2026-11-10"
  source_api: "customer-api"
  provenance: "references/traceability.md"
  presentation: "on"
```

The authoritative version is the single value in `uber-standard/VERSION`; the bake stamps that
value. The drift check compares each skill's `uber_standard_version` against `uber-standard/VERSION`;
skills behind it are flagged for regeneration.
