---
name: style-guide
description: Rules with Do / Don't examples for visual style, UI tokens, or brand voice. Use when defining or enforcing a look, a design system, or a voice that many contributors must follow.
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
```markdown
| Area | Rule | Do | Don't |
Tokens / palette (if visual): <name: value>
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
| Voice | Plain over clever | "Ship faster with less glue code" | "Synergize your workflow" |
| Color | Hostile = red family only | enemy AoE #D33 | red player heal |
```

## Quality checks
- [ ] Every rule is checkable
- [ ] Every rule has both a Do and a Don't
- [ ] Contrast-relevant rules meet accessibility minimums
