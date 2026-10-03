---
name: slide-spec
description: Per-slide design spec covering focal point, layout, build steps, and alt text, plus template tokens. Use when designing or auditing a deck's visuals after the story outline exists.
---

# Slide Spec

Gives every slide one focal point and builds that match what the speaker says.

## When to use
After the [beat chart](../beat-chart/SKILL.md) for a talk is set, and when auditing an existing deck.

## Produced by
- `slide_designer`: owns it.

## Template
```markdown
Template: grid <n-col> | type scale <body ≥28pt, code ≥24pt> | palette <tokens>
| Slide | Focal point | Layout | Build steps | Alt text |
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
| 7 (beat 3) | request path arrow | full diagram | 1 request → 2 queue → 3 worker → 4 store | "Request flows through queue to worker, then store" |
```

## Quality checks
- [ ] One focal point per slide
- [ ] Type meets minimum sizes
- [ ] Builds match the spoken order
