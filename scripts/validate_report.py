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
actually produces that report. It checks every report type at once. To check a single
report type, run that skill's own `<dir>/scripts/validate.py` (see `validation:` in its
SKILL.md). Both use the same checks from scripts/skill_validate.py.

Usage:
  python3 scripts/validate_report.py output.md [more.md ...]       # '-' reads stdin
  python3 scripts/validate_report.py --role red_team_skeptic out.md # also require all of the role's reports
  python3 scripts/validate_report.py --require risk_register out.md # require specific reports
  python3 scripts/validate_report.py --json out.md                  # machine-readable result

Exit code 0 when every block is valid (and required reports are present), 1 otherwise.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_validate import check_block as _check_block  # noqa: E402
from skill_validate import find_blocks as _find_blocks  # noqa: E402
from skill_validate import load_frontmatter, load_roles_dir  # noqa: E402,F401


def load_specs(root=ROOT):
    specs = {}
    for path in sorted((root / "reporting").glob("*/SKILL.md")):
        fm = load_frontmatter(path)
        if fm and fm.get("report_id"):
            specs[fm["report_id"]] = fm
    return specs


def load_roles(root=ROOT):
    return load_roles_dir(root / "blackboard")


def find_blocks(text):
    blocks, errors = _find_blocks(text)
    return blocks, [(line, msg) for line, _, msg in errors]


def check_block(block, specs, roles):
    spec = specs.get(block["id"])
    if spec is None:
        return [f"unknown report type '{block['id']}'"]
    return _check_block(block, spec, roles)


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
