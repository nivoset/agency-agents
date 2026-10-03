#!/usr/bin/env python3
"""Validate blackboard roles, panels, tags, and reporting skills, and (optionally)
regenerate blackboard/index.json.

Usage:
  python3 scripts/blackboard-index.py           # validate only
  python3 scripts/blackboard-index.py --write   # validate and write blackboard/index.json

See blackboard/SCHEMA.md for the role contract and reporting/README.md for reports.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BOARD_DIR = ROOT / "blackboard"
REPORTING_DIR = ROOT / "reporting"
TAGS = yaml.safe_load((BOARD_DIR / "tags.yaml").read_text(encoding="utf-8")) or {}
REGISTRY = yaml.safe_load((REPORTING_DIR / "reports.yaml").read_text(encoding="utf-8")) or {}
REPORTS = REGISTRY.get("reports") or {}
UNIVERSAL = REGISTRY.get("universal") or {}
SKILL_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
DOMAINS = {"software", "game", "presentation", "conflict", "social", "visual"}
DIVISIONS = {"core", "product", "quality", "software", "game", "visual", "presentation", "conflict", "social"}
AUTHORITIES = {"propose-only", "review-only", "implement"}
NOTE_KINDS = {"claim", "question", "answer"}
TOP_REQUIRED = ["name", "description", "color", "emoji", "vibe", "blackboard"]
LIST_KEYS = [
    "summon_when", "skip_when", "key_pushes", "pushes_back_on", "blind_spots",
    "signature_questions", "evidence", "pairs_with", "based_on", "tags", "reports",
]
STR_KEYS = ["speciality", "why_template", "deliverable", "done_when"]
REQUIRED_SECTIONS = ["Identity", "Core Mission", "Critical Rules", "Board", "Deliverable", "Completeness"]

errors = []


def err(path, msg):
    errors.append(f"ERROR {path.relative_to(ROOT)}: {msg}")


def skill_dir(report_id):
    return report_id.replace("_", "-")


def sections(body):
    """Map each level-2 heading (outside code fences) to its text."""
    out, current, in_fence = {}, None, False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            current = line[3:].strip()
            out[current] = ""
            continue
        if current is not None:
            out[current] += line + "\n"
    return out


def section(body, name):
    for heading, text in sections(body).items():
        if name.lower() in heading.lower():
            return text
    return None


def missing_fields(text, fields):
    low = (text or "").lower()
    return [f for f in fields if f.lower() not in low]


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
    for name in REQUIRED_SECTIONS:
        if not re.search(rf"^##.*{name}", body, re.M | re.I):
            err(path, f"missing body section containing '{name}'")
    for tag in bb.get("tags") or []:
        if tag not in TAGS:
            err(path, f"tag '{tag}' is not in blackboard/tags.yaml")
    deliverable = section(body, "Deliverable")
    for rid in bb.get("reports") or []:
        if rid in UNIVERSAL:
            err(path, f"report '{rid}' is universal; don't list it in reports")
            continue
        if rid not in REPORTS:
            err(path, f"report '{rid}' is not in reporting/reports.yaml")
            continue
        if f"reporting/{skill_dir(rid)}/SKILL.md" not in (deliverable or ""):
            err(path, f"Deliverable section must link reporting/{skill_dir(rid)}/SKILL.md")
        missing = missing_fields(deliverable, REPORTS[rid].get("core_fields") or [])
        if missing:
            err(path, f"Deliverable template lacks {rid} core fields: {missing}")
    return bb


def check_reporting(producers):
    registry_path = REPORTING_DIR / "reports.yaml"
    entries = {**UNIVERSAL, **REPORTS}
    if set(UNIVERSAL) & set(REPORTS):
        err(registry_path, "a report cannot be both universal and role-specific")
    expected_dirs = {skill_dir(r) for r in entries}
    for d in sorted(p.name for p in REPORTING_DIR.iterdir() if p.is_dir()):
        if d not in expected_dirs:
            err(REPORTING_DIR / d, "skill folder has no entry in reports.yaml")
    for rid, entry in entries.items():
        for key in ("title", "tags", "core_fields"):
            if not entry.get(key):
                err(registry_path, f"{rid}: missing '{key}'")
        for tag in entry.get("tags") or []:
            if tag not in TAGS:
                err(registry_path, f"{rid}: tag '{tag}' is not in blackboard/tags.yaml")
        path = REPORTING_DIR / skill_dir(rid) / "SKILL.md"
        if not path.exists():
            err(path, "missing skill file for registered report")
            continue
        fm, body = parse(path)
        if fm is None:
            continue
        if fm.get("name") != skill_dir(rid):
            err(path, f"name must be '{skill_dir(rid)}'")
        if not isinstance(fm.get("description"), str) or len(fm["description"]) < 40:
            err(path, "description must say what the report is and when to use it")
        extra = set(fm) - SKILL_KEYS
        if extra:
            err(path, f"unsupported SKILL.md frontmatter keys {sorted(extra)}; put report metadata in reports.yaml")
        if not body.lstrip().startswith(f"# {entry.get('title')}"):
            err(path, f"first heading must be '# {entry.get('title')}'")
        for name in ("When to use", "Produced by", "Template", "Core fields", "How to fill it in",
                     "On the board", "Example", "Quality checks"):
            if section(body, name) is None:
                err(path, f"missing section '## {name}'")
        missing = missing_fields(section(body, "Template"), entry.get("core_fields") or [])
        if missing:
            err(path, f"Template lacks core fields {missing}")
        listed = set(re.findall(r"^- `([a-z0-9_]+)`", section(body, "Produced by") or "", re.M))
        if rid in UNIVERSAL:
            if listed:
                err(path, "universal report should say 'All roles', not list role ids")
            continue
        actual = producers.get(rid, set())
        if not actual:
            err(path, "no role lists this report in blackboard.reports")
        if listed != actual:
            err(path, f"Produced by {sorted(listed)} does not match roles listing it {sorted(actual)}")


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

    producers = {}
    for rid, role in roles.items():
        for rep in role.get("reports") or []:
            producers.setdefault(rep, set()).add(rid)
    check_reporting(producers)

    used_tags = {t for r in roles.values() for t in r.get("tags") or []}
    used_tags |= {t for e in list(REPORTS.values()) + list(UNIVERSAL.values()) for t in e.get("tags") or []}
    for tag in sorted(set(TAGS) - used_tags):
        err(BOARD_DIR / "tags.yaml", f"tag '{tag}' is not used by any role or report")

    if errors:
        print("\n".join(errors))
        print(f"\nFAILED: {len(errors)} error(s) across {len(files)} role files.")
        return 1

    print(f"PASSED: {len(roles)} roles, {sum(len(v) for v in panels['panels'].values())} panels, "
          f"{len(REPORTS) + len(UNIVERSAL)} reporting skills, {len(TAGS)} tags.")
    if write:
        index = {
            "schema": "blackboard/SCHEMA.md",
            "facilitator": panels.get("facilitator"),
            "roles": dict(sorted(roles.items())),
            "panels": panels["panels"],
            "tags": {t: {"description": TAGS[t],
                         "roles": sorted(r for r, v in roles.items() if t in (v.get("tags") or []))}
                     for t in sorted(TAGS)},
            "reports": {rid: {**entry,
                              "skill": f"reporting/{skill_dir(rid)}/SKILL.md",
                              "universal": rid in UNIVERSAL,
                              "produced_by": "all" if rid in UNIVERSAL else sorted(producers.get(rid, []))}
                        for rid, entry in sorted({**UNIVERSAL, **REPORTS}.items())},
        }
        out = BOARD_DIR / "index.json"
        out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
