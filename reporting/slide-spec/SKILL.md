---
name: slide-spec
description: Per-slide design spec covering focal point, layout, build steps, and alt text, plus template tokens. Use when designing or auditing a deck's visuals after the story outline exists.
report_id: slide_spec
title: Slide Spec
version: 1
universal: false
tags: [slides]
produced_by: [slide_designer]
output:
  tag: report:slide_spec
  format: table
  columns: [Slide, Focal point, Layout, Build steps, Alt text]
  min_rows: 1
---

# Slide Spec

Gives every slide one focal point and builds that match what the speaker says.

## When to use
After the [beat chart](../beat-chart/SKILL.md) for a talk is set, and when auditing an existing deck.

## Produced by
- `slide_designer`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:slide_spec role=ROLE_ID board=BOARD_ID -->
Template: grid <n-col> | type scale <body ≥28pt, code ≥24pt> | palette <tokens>
| Slide | Focal point | Layout | Build steps | Alt text |
<!-- /report:slide_spec -->
```

## Core fields (required)
- **Slide**: number plus beat reference.
- **Focal point**: the one thing the eye lands on first.
- **Layout**: e.g. full-bleed image, two-column compare, or diagram.
- **Build steps**: in spoken order, or `none`.
- **Alt text**: for meaningful images in shared decks.

## How to fill it in
1. Take one row per slide from the beat chart.
2. Choose the focal point, then the layout that serves it.
3. Write build steps against the speaker notes, and add alt text.

## On the board
Back-row or contrast failures are `claim` notes. Builds that clash with delivery pace go to `delivery_coach` as `question` notes.

## Example

```markdown
<!-- report:slide_spec role=slide_designer board=BB-DESIGN-REPLAY -->
Template: 12-column grid | body 32pt, code 24pt | palette: ink, chalk, accent
| Slide | Focal point | Layout | Build steps | Alt text |
|---|---|---|---|---|
| 7 (beat 3) | request path arrow | full diagram | 1 request → 2 queue → 3 worker → 4 store | "A request flows through the queue to a worker, then to the store" |
<!-- /report:slide_spec -->
```

## Quality checks
- [ ] One focal point per slide
- [ ] Type meets minimum sizes
- [ ] Builds match the spoken order
