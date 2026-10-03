---
name: reference-list
description: Annotated list of precedents and examples, giving the example, its source, what to borrow, and what to avoid. Use before inventing an approach, to bring prior art, competitor examples, internal implementations, or reference art onto the board.
report_id: reference_list
title: Reference List
version: 1
universal: false
tags: [research, evidence]
produced_by: [prior_art_scout]
output:
  tag: report:reference_list
  format: table
  columns: [Ref, Example, Source, Borrow, Avoid]
  min_rows: 1
validation:
  script: scripts/validate.py
  command: uv run --script <dir>/scripts/validate.py --format json <file>
  command_for_role: uv run --script <dir>/scripts/validate.py --format json --role <role> --board <board> <file>
  fallback_command: python3 <dir>/scripts/validate.py --format json <file>
  placeholders:
    <dir>: Absolute path of this skill's folder (the one containing SKILL.md)
    <file>: Path to the agent output to validate; '-' reads stdin
    <role>: Role id that produced the output (blackboard.id of the role)
    <board>: Board id the output belongs to (board= attribute on the report tag)
  requires: [uv]
  fallback_requires: [python3>=3.9, pyyaml>=6.0]
  dependencies: PEP 723 inline metadata in scripts/validate.py (uv installs them on first run)
  output: json
  exit_codes:
    0: valid
    1: invalid
    2: usage_error
---

# Reference List

Gives the board real examples to argue from, so it doesn't start from first principles.

## When to use
When a role asks "how do others do this?", or before a design or approach is chosen.

## Produced by
- `prior_art_scout`: the repository first, then the outside world.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:reference_list role=ROLE_ID board=BOARD_ID -->
| Ref | Example | Source | Borrow | Avoid |
| R1 | <what it is> | <path / URL / title, year> | <specific element to reuse> | <specific pitfall> |
<!-- /report:reference_list -->
```

## Core fields (required)
- **Ref**: `R1`, `R2`, and so on, for citing in notes.
- **Example**: the thing, named concretely.
- **Source**: verifiable. Use a repository path, a URL, or a title and year.
- **Borrow** / **Avoid**: specific elements, not "good UX".

## How to fill it in
1. Search the repository for existing implementations. These outrank outside examples.
2. Collect 3–7 references. Prefer ones that shipped, with known outcomes.
3. Annotate what to borrow and what to avoid from each.

## On the board
Post an `answer` note when a reference resolves an open question, citing `R#`. Other roles cite `R#` as evidence in their notes.

## Example

```markdown
<!-- report:reference_list role=prior_art_scout board=BB-DESIGN-REPLAY -->
| Ref | Example | Source | Borrow | Avoid |
|---|---|---|---|---|
| R1 | Existing note renderer | components/blackboard/note-card.tsx | kind and confidence badges | writing a second renderer |
| R2 | Document version history panels | Google Docs / Figma version history | named versions with author and time | no rationale per version |
<!-- /report:reference_list -->
```

## Quality checks
- [ ] Every source is verifiable
- [ ] The repository was searched first
- [ ] Borrow and Avoid are specific
