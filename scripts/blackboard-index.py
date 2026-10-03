#!/usr/bin/env python3
"""Validate blackboard role files and (optionally) regenerate blackboard/index.json.

Usage:
  python3 scripts/blackboard-index.py           # validate only
  python3 scripts/blackboard-index.py --write   # validate and write blackboard/index.json

See blackboard/SCHEMA.md for the frontmatter contract.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BOARD_DIR = ROOT / "blackboard"
DOMAINS = {"software", "game", "presentation", "conflict", "social", "visual"}
DIVISIONS = {"core", "product", "quality", "software", "game", "visual", "presentation", "conflict", "social"}
AUTHORITIES = {"propose-only", "review-only", "implement"}
NOTE_KINDS = {"claim", "question", "answer"}
TOP_REQUIRED = ["name", "description", "color", "emoji", "vibe", "blackboard"]
LIST_KEYS = [
    "summon_when", "skip_when", "key_pushes", "pushes_back_on", "blind_spots",
    "signature_questions", "evidence", "pairs_with", "based_on",
]
STR_KEYS = ["speciality", "why_template", "deliverable", "done_when"]
REQUIRED_SECTIONS = ["Identity", "Core Mission", "Critical Rules", "Board", "Deliverable", "Completeness"]

errors = []


def err(path, msg):
    errors.append(f"ERROR {path.relative_to(ROOT)}: {msg}")


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        err(path, "missing or malformed frontmatter")
        return None, ""
    try:
        return yaml.safe_load(m.group(1)), m.group(2)
    except yaml.YAMLError as e:
        err(path, f"YAML error: {e}")
        return None, ""


def check_role(path, fm, body):
    for key in TOP_REQUIRED:
        if key not in fm:
            err(path, f"missing top-level '{key}'")
    bb = fm.get("blackboard") or {}
    expected_id = path.stem.replace("-", "_")
    if bb.get("id") != expected_id:
        err(path, f"blackboard.id must be '{expected_id}' (got {bb.get('id')!r})")
    if bb.get("division") != path.parent.name or bb.get("division") not in DIVISIONS:
        err(path, f"blackboard.division must be '{path.parent.name}'")
    domains = bb.get("domains")
    if not isinstance(domains, list) or not domains or not set(domains) <= DOMAINS:
        err(path, f"blackboard.domains must be a non-empty subset of {sorted(DOMAINS)}")
    for key in STR_KEYS:
        if not isinstance(bb.get(key), str) or not bb.get(key).strip():
            err(path, f"blackboard.{key} must be a non-empty string")
    for key in LIST_KEYS:
        if not isinstance(bb.get(key), list) or not bb.get(key):
            err(path, f"blackboard.{key} must be a non-empty list")
    pushes = bb.get("key_pushes") or []
    if not 3 <= len(pushes) <= 5:
        err(path, "blackboard.key_pushes must have 3-5 entries")
    bias = bb.get("note_bias")
    if not isinstance(bias, list) or not bias or not set(bias) <= NOTE_KINDS:
        err(path, f"blackboard.note_bias must be a subset of {sorted(NOTE_KINDS)}")
    if bb.get("authority") not in AUTHORITIES:
        err(path, f"blackboard.authority must be one of {sorted(AUTHORITIES)}")
    tensions = bb.get("tensions")
    if not isinstance(tensions, list) or not tensions:
        err(path, "blackboard.tensions must be a non-empty list")
    else:
        for t in tensions:
            if not isinstance(t, dict) or not t.get("with") or not t.get("over"):
                err(path, "each tension needs 'with' and 'over'")
    for ref in bb.get("based_on") or []:
        if not (ROOT / ref).exists():
            err(path, f"based_on path does not exist: {ref}")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##.*{section}", body, re.M | re.I):
            err(path, f"missing body section containing '{section}'")
    return bb


def main():
    write = "--write" in sys.argv
    roles = {}
    files = sorted(p for p in BOARD_DIR.glob("*/*.md"))
    for path in files:
        fm, body = parse(path)
        if fm is None:
            continue
        bb = check_role(path, fm, body)
        rid = bb.get("id")
        if rid in roles:
            err(path, f"duplicate id '{rid}' (also {roles[rid]['path']})")
            continue
        roles[rid] = {
            "path": str(path.relative_to(ROOT)),
            "name": fm.get("name"),
            "description": fm.get("description"),
            "emoji": fm.get("emoji"),
            "vibe": fm.get("vibe"),
            **bb,
        }

    for rid, role in roles.items():
        path = ROOT / role["path"]
        for t in role.get("tensions") or []:
            if isinstance(t, dict) and t.get("with") not in roles:
                err(path, f"tension with unknown role '{t.get('with')}'")
        for other in role.get("pairs_with") or []:
            if other not in roles:
                err(path, f"pairs_with unknown role '{other}'")

    panels_path = BOARD_DIR / "panels.yaml"
    panels = yaml.safe_load(panels_path.read_text(encoding="utf-8")) if panels_path.exists() else {}
    if not panels:
        err(panels_path, "missing or empty panels.yaml")
    for domain, entries in (panels or {}).get("panels", {}).items():
        for panel in entries:
            core = panel.get("core") or []
            if not 2 <= len(core) <= 5:
                err(panels_path, f"panel '{panel.get('id')}' must have 2-5 core roles")
            for rid in core + (panel.get("optional") or []):
                if rid not in roles:
                    err(panels_path, f"panel '{panel.get('id')}' references unknown role '{rid}'")
            if set(core) & set(panel.get("optional") or []):
                err(panels_path, f"panel '{panel.get('id')}' lists a role as both core and optional")
    facilitator = (panels or {}).get("facilitator")
    if facilitator and facilitator not in roles:
        err(panels_path, f"facilitator '{facilitator}' is not a role")
    seated = {facilitator}
    for entries in (panels or {}).get("panels", {}).values():
        for panel in entries:
            seated |= set(panel.get("core") or []) | set(panel.get("optional") or [])
    for rid in sorted(set(roles) - seated):
        err(ROOT / roles[rid]["path"], "role is not seated in any panel (core or optional)")

    if errors:
        print("\n".join(errors))
        print(f"\nFAILED: {len(errors)} error(s) across {len(files)} role files.")
        return 1

    print(f"PASSED: {len(roles)} roles, {sum(len(v) for v in panels['panels'].values())} panels.")
    if write:
        index = {
            "schema": "blackboard/SCHEMA.md",
            "facilitator": panels.get("facilitator"),
            "roles": dict(sorted(roles.items())),
            "panels": panels["panels"],
        }
        out = BOARD_DIR / "index.json"
        out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
