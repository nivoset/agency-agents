#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Validate one report type's tagged blocks in agent output against its SKILL.md spec.

Canonical source: scripts/skill_validate.py. Every reporting skill ships a byte-identical
copy at <skill dir>/scripts/validate.py (written by `scripts/blackboard-index.py --write`),
so a copied skill folder validates on its own. The PEP 723 block above lets uv
install PyYAML on demand (`uv run --script <dir>/scripts/validate.py ...`). Plain
`python3` also works when PyYAML is already installed.

A skill handler runs the command template from the skill's frontmatter
(`validation.command` / `validation.command_for_role`) after substituting:

  <dir>    absolute path of the skill folder (contains SKILL.md)
  <file>   agent output to validate ('-' reads stdin)
  <role>   role id that produced the output
  <board>  board id the output belongs to

Usage:
  python3 <dir>/scripts/validate.py [--format text|json] [--role R] [--board B]
                                    [--roles-dir D] [--skill DIR] [--allow-missing] <file>

Only blocks tagged <!-- report:<this report_id> ... --> are checked; other report tags
are left to their own skills.

Exit codes: 0 valid, 1 invalid output, 2 usage or environment error.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    yaml = None

OPEN_RE = re.compile(r"<!--\s*report:([a-z0-9_]+)((?:\s+[a-z_]+=[^\s>]+)*)\s*-->")
CLOSE_RE = re.compile(r"<!--\s*/report:([a-z0-9_]+)\s*-->")
SEPARATOR_RE = re.compile(r"^:?-+:?$")
EXIT_VALID, EXIT_INVALID, EXIT_USAGE = 0, 1, 2


def load_frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else None


def load_roles_dir(roles_dir):
    """Map role id -> blackboard block for every role .md under roles_dir (recursive)."""
    roles = {}
    for path in sorted(Path(roles_dir).rglob("*.md")):
        fm = load_frontmatter(path) or {}
        bb = fm.get("blackboard") if isinstance(fm, dict) else None
        if isinstance(bb, dict) and bb.get("id"):
            roles[bb["id"]] = bb
    return roles


def find_blocks(text):
    """Return (blocks, errors). Each block: id, attrs, line, body (list of lines)."""
    blocks, errors, current = [], [], None
    for lineno, line in enumerate(text.splitlines(), 1):
        opened, closed = OPEN_RE.search(line), CLOSE_RE.search(line)
        if opened:
            if current:
                errors.append((current["line"], current["id"],
                               f"report:{current['id']} is not closed before line {lineno}"))
            attrs = dict(a.split("=", 1) for a in opened.group(2).split())
            current = {"id": opened.group(1), "attrs": attrs, "line": lineno, "body": []}
        elif closed:
            if not current or current["id"] != closed.group(1):
                errors.append((lineno, closed.group(1),
                               f"closing tag /report:{closed.group(1)} has no matching open tag"))
            else:
                blocks.append(current)
                current = None
        elif current is not None and not line.strip().startswith("```"):
            current["body"].append(line)
    if current:
        errors.append((current["line"], current["id"], f"report:{current['id']} is never closed"))
    return blocks, errors


def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip())
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]


def tables(lines):
    """Yield (header, rows) for each run of consecutive markdown table lines."""
    run = []
    for line in lines + [""]:
        if line.strip().startswith("|"):
            run.append(split_row(line))
            continue
        if run:
            header, rows = run[0], [r for r in run[1:] if not all(SEPARATOR_RE.match(c) for c in r if c)]
            yield header, rows
            run = []


def column_index(header, name):
    name = name.lower()
    return next((i for i, h in enumerate(header) if h.lower().startswith(name)), None)


def enum_ok(value, allowed):
    v = value.strip().strip("`*\"'").lower()
    return any(v == a or (v.startswith(a) and not v[len(a)].isalnum()) for a in allowed)


def label_value(text, label):
    m = re.search(
        rf"(?:^|\|)\s*(?:[-*]\s+)?(?:\*\*)?{re.escape(label)}[^:|\n]{{0,40}}?(?:\*\*)?\s*:\s*([^|\n]*)",
        text, re.I | re.M)
    return None if m is None else m.group(1).strip()


def check_block(block, spec, roles=None):
    """Return error messages for one tagged block against one skill spec."""
    rid, errs = block["id"], []
    role = block["attrs"].get("role")
    if not role:
        errs.append("missing role= attribute on the report tag")
    elif roles is not None and role not in roles:
        errs.append(f"unknown role '{role}'")
    elif not spec.get("universal") and role not in (spec.get("produced_by") or []):
        errs.append(f"role '{role}' does not produce {rid} (produced_by: {spec.get('produced_by')})")

    out = spec.get("output") or {}
    lines = block["body"]
    text = "\n".join(lines)
    min_rows = out.get("min_rows", 1)
    enums = {str(k): [str(v).lower() for v in vals] for k, vals in (out.get("enums") or {}).items()}

    if out.get("keys"):
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            return errs + [f"body is not valid YAML: {str(e).splitlines()[0]}"]
        items = data if isinstance(data, list) else [data]
        if len(items) < min_rows:
            errs.append(f"expected at least {min_rows} item(s), got {len(items)}")
        for n, item in enumerate(items, 1):
            if not isinstance(item, dict):
                errs.append(f"item {n} is not a mapping")
                continue
            for key in out["keys"]:
                if key not in item:
                    errs.append(f"item {n}: missing key '{key}'")
            for key, allowed in enums.items():
                val = next((v for k, v in item.items() if k.lower() == key.lower()), None)
                if val is not None and not enum_ok(str(val), allowed):
                    errs.append(f"item {n}: {key}={val!r} not in {allowed}")
        return errs

    if out.get("steps"):
        scenarios = re.split(r"^\s*Scenario[^:\n]*:", text, flags=re.M)[1:]
        if len(scenarios) < min_rows:
            errs.append(f"expected at least {min_rows} scenario(s), got {len(scenarios)}")
        for n, sc in enumerate(scenarios, 1):
            starts = {l.strip().split(" ", 1)[0].lower() for l in sc.splitlines() if l.strip()}
            for step in out["steps"]:
                if step.lower() not in starts:
                    errs.append(f"scenario {n}: missing '{step}' step")
        return errs

    if out.get("columns"):
        match = None
        for header, rows in tables(lines):
            if all(column_index(header, c) is not None for c in out["columns"]):
                match = (header, rows)
                break
        if match is None:
            errs.append(f"no table with columns {out['columns']}")
        else:
            header, rows = match
            if len(rows) < min_rows:
                errs.append(f"table needs at least {min_rows} row(s), got {len(rows)}")
            for n, row in enumerate(rows, 1):
                if len(row) != len(header):
                    errs.append(f"row {n}: {len(row)} cells but header has {len(header)}")
            for key, allowed in enums.items():
                j = column_index(header, key)
                if j is None:
                    continue
                for n, row in enumerate(rows, 1):
                    if j < len(row) and not enum_ok(row[j], allowed):
                        errs.append(f"row {n}: {header[j]}={row[j]!r} not in {allowed}")

    for label in out.get("labels") or []:
        if label_value(text, label) is None:
            errs.append(f"missing '{label}:' line")
    for key, allowed in enums.items():
        if out.get("columns") and any(column_index(h, key) is not None for h, _ in tables(lines)):
            continue
        value = label_value(text, key)
        if value and not enum_ok(value, allowed):
            errs.append(f"{key}: {value!r} not in {allowed}")

    for heading in out.get("headings") or []:
        if not re.search(rf"^#{{1,6}}\s.*{re.escape(heading)}", text, re.I | re.M):
            errs.append(f"missing heading containing '{heading}'")
    return errs


def validate_skill_output(text, spec, role=None, board=None, roles=None, allow_missing=False):
    """Validate the blocks for spec's report_id in text. Returns (blocks, [(line, message)])."""
    rid = spec["report_id"]
    all_blocks, tag_errors = find_blocks(text)
    problems = [(line, msg) for line, block_id, msg in tag_errors if block_id == rid]
    blocks = [b for b in all_blocks if b["id"] == rid]
    if role is not None:
        if not spec.get("universal") and role not in (spec.get("produced_by") or []):
            problems.append((0, f"role '{role}' does not produce {rid} (produced_by: {spec.get('produced_by')})"))
        if roles is not None and role not in roles:
            problems.append((0, f"unknown role '{role}'"))
    for block in blocks:
        if role is not None and block["attrs"].get("role") != role:
            problems.append((block["line"], f"block is tagged role={block['attrs'].get('role')!r}, expected {role!r}"))
        if board is not None and block["attrs"].get("board") != board:
            problems.append((block["line"], f"block is tagged board={block['attrs'].get('board')!r}, expected {board!r}"))
        for msg in check_block(block, spec, roles):
            problems.append((block["line"], msg))
    if not blocks and not allow_missing:
        problems.append((0, f"no <!-- report:{rid} --> block found"))
    return blocks, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate one report type's tagged output blocks.")
    ap.add_argument("file", help="agent output to validate ('-' reads stdin)")
    ap.add_argument("--skill", help="skill folder containing SKILL.md (default: this script's skill)")
    ap.add_argument("--role", help="role id that produced the output; blocks must carry this role")
    ap.add_argument("--board", help="board id; blocks must carry this board")
    ap.add_argument("--roles-dir", help="directory of blackboard role .md files, to check role ids exist")
    ap.add_argument("--allow-missing", action="store_true", help="exit 0 when no block of this type is present")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    def fail_usage(message):
        if args.format == "json":
            print(json.dumps({"valid": False, "usage_error": message}))
        else:
            print(f"USAGE ERROR: {message}", file=sys.stderr)
        return EXIT_USAGE

    if yaml is None:
        return fail_usage("PyYAML is required (pip install pyyaml)")
    skill_dir = Path(args.skill) if args.skill else Path(__file__).resolve().parent.parent
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return fail_usage(f"no SKILL.md in {skill_dir}")
    spec = load_frontmatter(skill_md) or {}
    if not spec.get("report_id") or not isinstance(spec.get("output"), dict):
        return fail_usage(f"{skill_md} has no report_id/output spec")
    if args.file == "-":
        text = sys.stdin.read()
    elif Path(args.file).is_file():
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        return fail_usage(f"output file not found: {args.file}")
    roles = None
    if args.roles_dir:
        if not Path(args.roles_dir).is_dir():
            return fail_usage(f"roles dir not found: {args.roles_dir}")
        roles = load_roles_dir(args.roles_dir)

    blocks, problems = validate_skill_output(text, spec, args.role, args.board, roles, args.allow_missing)
    if args.format == "json":
        print(json.dumps({
            "skill": spec.get("name"),
            "report_id": spec["report_id"],
            "version": spec.get("version"),
            "file": args.file,
            "valid": not problems,
            "blocks": [{"line": b["line"], **b["attrs"]} for b in blocks],
            "errors": [{"line": line, "message": msg} for line, msg in problems],
        }, indent=2))
    else:
        for line, msg in problems:
            print(f"ERROR {args.file}{':' + str(line) if line else ''}: [{spec['report_id']}] {msg}")
        if not problems:
            print(f"OK {args.file}: {len(blocks)} {spec['report_id']} block(s) valid")
    return EXIT_INVALID if problems else EXIT_VALID


if __name__ == "__main__":
    sys.exit(main())
