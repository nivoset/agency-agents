#!/usr/bin/env python3
"""Validate blackboard roles, panels, tags, and reporting skills, and (optionally)
regenerate blackboard/index.json.

Usage:
  uv run scripts/blackboard-index.py           # validate only
  uv run scripts/blackboard-index.py --write   # validate and write blackboard/index.json

See blackboard/SCHEMA.md for the role contract and reporting/README.md for reports.
"""
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BOARD_DIR = ROOT / "blackboard"
REPORTING_DIR = ROOT / "reporting"
TAGS = yaml.safe_load((BOARD_DIR / "tags.yaml").read_text(encoding="utf-8")) or {}
sys.path.insert(0, str(ROOT / "scripts"))
from validate_report import load_specs, validate_text  # noqa: E402

SPECS = load_specs(ROOT)
REPORTS = {k: v for k, v in SPECS.items() if not v.get("universal")}
UNIVERSAL = {k: v for k, v in SPECS.items() if v.get("universal")}
SKILL_REQUIRED = ["name", "description", "report_id", "title", "version", "universal", "tags", "output",
                  "validation"]
CANONICAL_VALIDATOR = ROOT / "scripts" / "skill_validate.py"
VALIDATION_KEYS = ["script", "command", "command_for_role", "fallback_command", "placeholders", "requires",
                   "fallback_requires", "dependencies", "output", "exit_codes"]
COMMAND_KEYS = ["command", "command_for_role", "fallback_command"]
PLACEHOLDER_RE = re.compile(r"<[a-z_]+>")


def render_command(template, values):
    """Reference skill-handler substitution: split the template into argv, then replace
    each <placeholder> inside each token. Values never get re-split, so paths with spaces
    are safe."""
    argv = []
    for token in shlex.split(template):
        for key, value in values.items():
            token = token.replace(key, value)
        argv.append(token)
    return argv
OUTPUT_FORMATS = {"table", "fields", "sections", "yaml", "gherkin"}
OUTPUT_FIELD_KEYS = ["columns", "labels", "headings", "keys", "steps"]
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


warnings = []


def warn(path, msg):
    if msg not in [w.split(": ", 1)[1] for w in warnings]:
        warnings.append(f"WARN  {path.relative_to(ROOT)}: {msg}")


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


def core_fields(spec):
    out = spec.get("output") or {}
    return [f for key in OUTPUT_FIELD_KEYS for f in out.get(key) or []]


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
            err(path, f"report '{rid}' has no skill in reporting/ (report_id not found)")
            continue
        if f"reporting/{skill_dir(rid)}/SKILL.md" not in (deliverable or ""):
            err(path, f"Deliverable section must link reporting/{skill_dir(rid)}/SKILL.md")
        missing = missing_fields(deliverable, core_fields(REPORTS[rid]))
        if missing:
            err(path, f"Deliverable template lacks {rid} core fields: {missing}")
    return bb


def check_validation(path, fm, example, attrs):
    """Check the skill's `validation` block, its bundled script, and run its commands."""
    v = fm.get("validation") or {}
    for key in VALIDATION_KEYS:
        if key not in v:
            err(path, f"validation.{key} is required")
    if any(k not in v for k in ["script", "placeholders"] + COMMAND_KEYS):
        return
    script = path.parent / v["script"]
    if not script.is_file():
        err(path, f"validation.script {v['script']} does not exist (run --write)")
        return
    if script.read_bytes() != CANONICAL_VALIDATOR.read_bytes():
        err(script, "differs from scripts/skill_validate.py (run --write)")
    if not os.access(script, os.X_OK):
        err(script, "is not executable (run --write)")
    declared = set(v["placeholders"])
    used = set(PLACEHOLDER_RE.findall(" ".join(v[k] for k in COMMAND_KEYS)))
    if used - declared:
        err(path, f"validation commands use undeclared placeholders {sorted(used - declared)}")
    if declared - used:
        err(path, f"validation.placeholders declares unused {sorted(declared - used)}")
    for key in COMMAND_KEYS:
        if f"<dir>/{v['script']}" not in v[key]:
            err(path, f"validation.{key} must run <dir>/{v['script']}")
    if sorted(map(str, v.get("exit_codes") or {})) != ["0", "1", "2"]:
        err(path, "validation.exit_codes must define 0, 1, and 2")

    # Simulate the skill handler: copy the skill folder somewhere else (with a space in the
    # path), substitute placeholders, and run. Example must pass; empty output must fail.
    with tempfile.TemporaryDirectory() as tmp:
        skill_copy = Path(tmp) / "installed skills" / path.parent.name
        shutil.copytree(path.parent, skill_copy)
        good, empty = Path(tmp) / "example output.md", Path(tmp) / "empty.md"
        good.write_text(example, encoding="utf-8")
        empty.write_text("No report here.\n", encoding="utf-8")
        base = {"<dir>": str(skill_copy), "<role>": attrs.get("role", ""), "<board>": attrs.get("board", "")}
        cases = [("command", good, 0), ("command_for_role", good, 0), ("command", empty, 1),
                 ("fallback_command", good, 0)]
        if shutil.which("uv") is None:
            warn(path, "uv not found; skipping uv commands and checking only fallback_command")
            cases = [c for c in cases if c[0] == "fallback_command"]
        for key, target, expected in cases:
            argv = render_command(v[key], {**base, "<file>": str(target)})
            proc = subprocess.run(argv, capture_output=True, text=True, cwd=tmp)
            if proc.returncode != expected:
                err(path, f"validation.{key} on {target.name} exited {proc.returncode}, expected {expected}: "
                          f"{(proc.stdout + proc.stderr).strip()[:300]}")
                continue
            try:
                result = json.loads(proc.stdout)
            except json.JSONDecodeError:
                err(path, f"validation.{key} did not print JSON")
                continue
            if result.get("valid") is not (expected == 0) or result.get("report_id") != fm.get("report_id"):
                err(path, f"validation.{key} JSON result is inconsistent: {result}")


def sync_validators():
    """Copy the canonical validator into every skill folder as its validation.script."""
    for path in sorted(REPORTING_DIR.glob("*/SKILL.md")):
        fm, _ = parse(path)
        script = (fm or {}).get("validation", {}).get("script")
        if not script:
            continue
        target = path.parent / script
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != CANONICAL_VALIDATOR.read_bytes():
            shutil.copyfile(CANONICAL_VALIDATOR, target)
        target.chmod(0o755)


def check_reporting(producers, roles):
    seen = set()
    for path in sorted(REPORTING_DIR.glob("*/SKILL.md")):
        fm, body = parse(path)
        if fm is None:
            continue
        rid = fm.get("report_id")
        for key in SKILL_REQUIRED:
            if key not in fm:
                err(path, f"missing frontmatter key '{key}'")
        if not rid:
            continue
        if rid in seen:
            err(path, f"duplicate report_id '{rid}'")
        seen.add(rid)
        if path.parent.name != skill_dir(rid) or fm.get("name") != skill_dir(rid):
            err(path, f"folder and name must both be '{skill_dir(rid)}'")
        if not isinstance(fm.get("description"), str) or len(fm["description"]) < 40:
            err(path, "description must say what the report is and when to use it")
        if not isinstance(fm.get("version"), int):
            err(path, "version must be an integer")
        for tag in fm.get("tags") or []:
            if tag not in TAGS:
                err(path, f"tag '{tag}' is not in blackboard/tags.yaml")
        if not fm.get("tags"):
            err(path, "tags must be a non-empty list")

        out = fm.get("output") or {}
        if out.get("tag") != f"report:{rid}":
            err(path, f"output.tag must be 'report:{rid}'")
        if out.get("format") not in OUTPUT_FORMATS:
            err(path, f"output.format must be one of {sorted(OUTPUT_FORMATS)}")
        if not core_fields(fm):
            err(path, f"output must define at least one of {OUTPUT_FIELD_KEYS}")
        if not isinstance(out.get("min_rows", 1), int) or out.get("min_rows", 1) < 1:
            err(path, "output.min_rows must be a positive integer")
        for key, vals in (out.get("enums") or {}).items():
            if not isinstance(vals, list) or not vals:
                err(path, f"output.enums.{key} must be a non-empty list")

        if not body.lstrip().startswith(f"# {fm.get('title')}"):
            err(path, f"first heading must be '# {fm.get('title')}'")
        for name in ("When to use", "Produced by", "Template", "Core fields", "How to fill it in",
                     "On the board", "Example", "Quality checks"):
            if section(body, name) is None:
                err(path, f"missing section '## {name}'")
        template = section(body, "Template") or ""
        if f"<!-- report:{rid} " not in template or f"<!-- /report:{rid} -->" not in template:
            err(path, f"Template must be wrapped in <!-- report:{rid} ... --> / <!-- /report:{rid} -->")
        missing = missing_fields(template, core_fields(fm))
        if missing:
            err(path, f"Template lacks core fields {missing}")

        example = section(body, "Example") or ""
        blocks, problems = validate_text(example, SPECS, roles)
        if [b["id"] for b in blocks] != [rid]:
            err(path, f"Example must contain exactly one tagged report:{rid} block")
        for line, _, msg in problems:
            err(path, f"Example fails output validation: {msg}")
        if blocks:
            check_validation(path, fm, example, blocks[0]["attrs"])

        listed = set(re.findall(r"^- `([a-z0-9_]+)`", section(body, "Produced by") or "", re.M))
        if fm.get("universal"):
            if listed or fm.get("produced_by"):
                err(path, "universal report should say 'All roles' and have no produced_by")
            continue
        actual = producers.get(rid, set())
        if not actual:
            err(path, "no role lists this report in blackboard.reports")
        if set(fm.get("produced_by") or []) != actual:
            err(path, f"produced_by {sorted(fm.get('produced_by') or [])} does not match roles listing it {sorted(actual)}")
        if listed != actual:
            err(path, f"Produced by section {sorted(listed)} does not match roles listing it {sorted(actual)}")
    for d in sorted(p.name for p in REPORTING_DIR.iterdir() if p.is_dir()):
        if not (REPORTING_DIR / d / "SKILL.md").exists():
            err(REPORTING_DIR / d, "folder has no SKILL.md")
        extras = {p.relative_to(REPORTING_DIR / d).as_posix() for p in (REPORTING_DIR / d).rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts} - {"SKILL.md", "scripts/validate.py"}
        if extras:
            err(REPORTING_DIR / d, f"unexpected files {sorted(extras)}")


BEGIN_MARK = "<!-- BEGIN GENERATED: python3 scripts/blackboard-index.py --write -->"
END_MARK = "<!-- END GENERATED -->"


def render_readme(text, index):
    """Replace the generated block of reporting/README.md with current report and role tables."""
    def spec_cell(out):
        parts = [f"{k}: {', '.join(map(str, out[k]))}" for k in OUTPUT_FIELD_KEYS if out.get(k)]
        if out.get("enums"):
            parts.append("enums: " + "; ".join(f"{k}={'/'.join(map(str, v))}" for k, v in out["enums"].items()))
        if out.get("min_rows", 1) > 1:
            parts.append(f"min_rows: {out['min_rows']}")
        return "<br>".join(parts)

    lines = ["", "## Report types", "",
             "| Report | Output tag | Format | Required output | Tags | Produced by |",
             "|---|---|---|---|---|---|"]
    for rid, rep in index["reports"].items():
        out = rep["output"]
        prod = "all roles" if rep["universal"] else ", ".join(f"`{p}`" for p in rep["produced_by"])
        lines.append(f"| [{rep['title']}]({skill_dir(rid)}/SKILL.md) | `{out['tag']}` | {out['format']} | "
                     f"{spec_cell(out)} | {', '.join(rep['tags'])} | {prod} |")
    lines += ["", "## Roles → tags and reports", "", "| Role | Tags | Reports |", "|---|---|---|"]
    for rid, role in sorted(index["roles"].items(), key=lambda kv: kv[1]["path"]):
        lines.append(f"| [{role['name']}](../{role['path']}) | {', '.join(role['tags'])} | "
                     f"{', '.join('`' + r + '`' for r in role['reports'])} |")
    start, end = text.index(BEGIN_MARK) + len(BEGIN_MARK), text.index(END_MARK)
    return text[:start] + "\n".join(lines) + "\n\n" + text[end:]


def main():
    write = "--write" in sys.argv
    if write:
        sync_validators()
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
    check_reporting(producers, roles)

    used_tags = {t for r in roles.values() for t in r.get("tags") or []}
    used_tags |= {t for e in list(REPORTS.values()) + list(UNIVERSAL.values()) for t in e.get("tags") or []}
    for tag in sorted(set(TAGS) - used_tags):
        err(BOARD_DIR / "tags.yaml", f"tag '{tag}' is not used by any role or report")

    if warnings:
        print(warnings[0] if len(warnings) == 1 else f"{warnings[0]} (and {len(warnings) - 1} more)")
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
            "reports": {rid: {"title": spec.get("title"),
                              "skill": f"reporting/{skill_dir(rid)}/SKILL.md",
                              "description": spec.get("description"),
                              "version": spec.get("version"),
                              "universal": bool(spec.get("universal")),
                              "tags": spec.get("tags"),
                              "produced_by": "all" if spec.get("universal") else spec.get("produced_by"),
                              "output": spec.get("output")}
                        for rid, spec in sorted(SPECS.items())},
        }
        out = BOARD_DIR / "index.json"
        out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")
        readme = REPORTING_DIR / "README.md"
        readme.write_text(render_readme(readme.read_text(encoding="utf-8"), index), encoding="utf-8")
        print(f"Wrote generated tables in {readme.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
