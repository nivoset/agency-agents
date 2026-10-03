---
name: style-guide
description: Rules with Do / Don't examples for visual style, UI tokens, or brand voice. Use when defining or enforcing a look, a design system, or a voice that many contributors must follow.
report_id: style_guide
title: Style Guide
version: 1
universal: false
tags: [art-direction, ui, brand]
produced_by: [art_director, brand_voice_guardian, ui_visual_designer]
output:
  tag: report:style_guide
  format: table
  columns: [Rule, Do, Don't]
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

# Style Guide

The rulebook that keeps many hands consistent.

## When to use
At the start of any multi-asset, multi-screen, or multi-post effort, and whenever drift appears.

## Produced by
- `art_director`: shape language, palette, value, line or material, lighting.
- `ui_visual_designer`: design tokens and component-state rules.
- `brand_voice_guardian`: voice traits and tone flex, with is / is-not examples.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:style_guide role=ROLE_ID board=BOARD_ID -->
| Area | Rule | Do | Don't |
Tokens / palette (if visual): <name: value>
<!-- /report:style_guide -->
```

## Core fields (required)
- **Rule**: one enforceable statement ("Enemies use sharp angular shapes").
- **Do**: a concrete example that follows it.
- **Don't**: a concrete counter-example.

## How to fill it in
1. Derive the rules from the brief and references (a [reference list](../reference-list/SKILL.md)).
2. Make every rule checkable, and give it one Do and one Don't.
3. Version the guide, and log changes when rules evolve.

## On the board
Reviews cite rules by area and number in [findings tables](../findings-table/SKILL.md). Contested rules (novelty vs. consistency, contrast vs. mood) are `question` notes involving `accessibility_inclusion_reviewer` where relevant.

## Example

```markdown
<!-- report:style_guide role=brand_voice_guardian board=BB-DESIGN-REPLAY -->
| Area | Rule | Do | Don't |
|---|---|---|---|
| Voice | Plain over clever | "Ship faster with less glue code" | "Synergize your workflow" |
| Tone | No emoji in incident posts | "We're sorry. Here's what happened." | "Oops 😅 we broke it" |
<!-- /report:style_guide -->
```

## Quality checks
- [ ] Every rule is checkable
- [ ] Every rule has both a Do and a Don't
- [ ] Contrast-relevant rules meet accessibility minimums
