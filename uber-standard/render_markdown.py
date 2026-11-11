#!/usr/bin/env python3
"""
render_markdown.py - the audited safe JSON to Markdown primitive (UBER-STANDARD).

Deterministically renders an API JSON response to Markdown, driven by a declarative
presentation mapping. No network, no eval, standard library only. The same input plus
the same mapping always produces the same output.

Usage:
    python render_markdown.py --mapping MAPPING.(json|yaml) --input RESPONSE.json [--out OUT.md]

The mapping schema is schemas/presentation-mapping.schema.yaml. This script NEVER executes
mapping-supplied code; a mapping only selects fields and labels. See output-sanitization.md.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

MAX_NAME = 64
MAX_VALUE = 500
SECRET_RE = re.compile(r"(authorization|api[_-]?key|token|secret|password|set-cookie|bearer)", re.I)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f​-‏  ]")
MD_SPECIAL = re.compile(r"([\\`*_\[\]<>|])")


def load_mapping(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("render_markdown: PyYAML not available; provide the mapping as JSON.")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        sys.exit("render_markdown: mapping must be a JSON or YAML object.")
    return data


def get_path(obj, dotted):
    """Read a dotted JSON path (a.b.c or a.0.b). Returns None if missing. No execution."""
    if not dotted:
        return obj
    cur = obj
    for part in str(dotted).split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return cur


def sanitize(value, is_name=False, redact=False) -> str:
    if redact:
        return "[redacted]"
    if value is None:
        return ""
    if isinstance(value, str):
        s = value
    elif isinstance(value, (dict, list)):
        s = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        s = str(value)
    s = CONTROL_RE.sub("", s)
    limit = MAX_NAME if is_name else MAX_VALUE
    if len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    s = s.replace("\n", " ")
    s = MD_SPECIAL.sub(r"\\\1", s)
    return s


def is_secret(key) -> bool:
    return bool(SECRET_RE.search(key or ""))


def render(mapping: dict, data) -> str:
    out = ["# " + sanitize(mapping.get("title", "API Response")), ""]
    sections = mapping.get("sections", [])
    if not sections:
        return "\n".join(out + ["_No sections defined in mapping._", ""])
    for sec in sections:
        heading = sanitize(sec.get("heading", ""))
        if heading:
            out += ["## " + heading, ""]
        node = get_path(data, sec.get("source"))
        if sec.get("kind") == "table":
            columns = sec.get("columns", [])
            rows = node if isinstance(node, list) else ([] if node is None else [node])
            out.append("| " + " | ".join(sanitize(c.get("label", c.get("path", ""))) for c in columns) + " |")
            out.append("|" + "|".join("---" for _ in columns) + "|")
            for row in rows:
                cells = [
                    sanitize(get_path(row, c.get("path", "")), is_name=bool(c.get("name")),
                             redact=is_secret(c.get("path", "")))
                    for c in columns
                ]
                out.append("| " + " | ".join(cells) + " |")
            out.append("")
        else:
            for f in sec.get("fields", []):
                key = f.get("path", "")
                val = get_path(node, key)
                out.append("- **" + sanitize(f.get("label", key)) + ":** "
                           + sanitize(val, is_name=bool(f.get("name")), redact=is_secret(key)))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Safe deterministic JSON to Markdown renderer (uber-standard).")
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    mapping = load_mapping(Path(a.mapping))
    data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    md = render(mapping, data)
    if a.out:
        Path(a.out).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
