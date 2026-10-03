#!/usr/bin/env python3
"""Validate tagged report blocks in agent output against reporting/*/SKILL.md specs.

Agents wrap every report they return in an output tag:

  <!-- report:risk_register role=red_team_skeptic board=BB-DESIGN-REPLAY -->
  | # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
  ...
  <!-- /report:risk_register -->

This tool finds those blocks and checks each one against the `output:` spec in the
matching skill's frontmatter: required columns, labels, headings, YAML keys, or
Given/When/Then steps; allowed (enum) values; minimum rows; and that the tagged role
actually produces that report.

Usage:
  python3 scripts/validate_report.py output.md [more.md ...]       # '-' reads stdin
  python3 scripts/validate_report.py --role red_team_skeptic out.md # also require all of the role's reports
  python3 scripts/validate_report.py --require risk_register out.md # require specific reports
  python3 scripts/validate_report.py --json out.md                  # machine-readable result

Exit code 0 when every block is valid (and required reports are present), 1 otherwise.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OPEN_RE = re.compile(r"<!--\s*report:([a-z0-9_]+)((?:\s+[a-z_]+=[^\s>]+)*)\s*-->")
CLOSE_RE = re.compile(r"<!--\s*/report:([a-z0-9_]+)\s*-->")
SEPARATOR_RE = re.compile(r"^:?-+:?$")


def load_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1)) if m else None


def load_specs(root=ROOT):
    specs = {}
    for path in sorted((root / "reporting").glob("*/SKILL.md")):
        fm = load_frontmatter(path)
        if fm and fm.get("report_id"):
            specs[fm["report_id"]] = fm
    return specs


def load_roles(root=ROOT):
    roles = {}
    for path in sorted((root / "blackboard").glob("*/*.md")):
        fm = load_frontmatter(path) or {}
        bb = fm.get("blackboard")
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
                errors.append((current["line"], f"report:{current['id']} is not closed before line {lineno}"))
            attrs = dict(a.split("=", 1) for a in opened.group(2).split())
            current = {"id": opened.group(1), "attrs": attrs, "line": lineno, "body": []}
        elif closed:
            if not current or current["id"] != closed.group(1):
                errors.append((lineno, f"closing tag /report:{closed.group(1)} has no matching open tag"))
            else:
                blocks.append(current)
                current = None
        elif current is not None and not line.strip().startswith("```"):
            current["body"].append(line)
    if current:
        errors.append((current["line"], f"report:{current['id']} is never closed"))
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


def check_block(block, specs, roles):
    rid, errs = block["id"], []
    spec = specs.get(rid)
    if spec is None:
        return [f"unknown report type '{rid}'"]
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
                if val is not None:
                    if not enum_ok(str(val), allowed):
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


def validate_text(text, specs=None, roles=None, require=(), role=None):
    """Validate all report blocks in text. Returns (blocks, [(line, report_id, message)])."""
    specs = load_specs() if specs is None else specs
    roles = load_roles() if roles is None else roles
    blocks, tag_errors = find_blocks(text)
    problems = [(line, None, msg) for line, msg in tag_errors]
    for block in blocks:
        for msg in check_block(block, specs, roles):
            problems.append((block["line"], block["id"], msg))
    required = set(require)
    if role:
        if role not in roles:
            problems.append((0, None, f"unknown role '{role}'"))
        else:
            required |= set(roles[role].get("reports") or [])
            blocks_by_role = [b for b in blocks if b["attrs"].get("role") == role]
            required_present = {b["id"] for b in blocks_by_role}
            for rid in sorted(required - required_present):
                problems.append((0, rid, f"role '{role}' did not return required report '{rid}'"))
            required = set()
    present = {b["id"] for b in blocks}
    for rid in sorted(required - present):
        problems.append((0, rid, f"required report '{rid}' not found"))
    return blocks, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+", help="output files to check ('-' for stdin)")
    ap.add_argument("--role", help="require every report this role declares in blackboard.reports")
    ap.add_argument("--require", default="", help="comma-separated report ids that must be present")
    ap.add_argument("--json", action="store_true", help="print machine-readable results")
    args = ap.parse_args(argv)

    specs, roles = load_specs(), load_roles()
    require = [r for r in args.require.split(",") if r]
    results, failed = [], False
    for name in args.files:
        text = sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")
        blocks, problems = validate_text(text, specs, roles, require, args.role)
        failed |= bool(problems)
        results.append({
            "file": name,
            "reports": [{"id": b["id"], "line": b["line"], **b["attrs"]} for b in blocks],
            "errors": [{"line": l, "report": r, "message": m} for l, r, m in problems],
        })
        if not args.json:
            for line, rid, msg in problems:
                where = f"{name}:{line}" if line else name
                print(f"ERROR {where}: {'[' + rid + '] ' if rid else ''}{msg}")
            if not problems:
                print(f"OK {name}: {len(blocks)} report block(s) valid")
    if args.json:
        print(json.dumps(results, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
