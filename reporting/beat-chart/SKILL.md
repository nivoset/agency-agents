---
name: beat-chart
description: Ordered beats with purpose, timing, and intensity. One shared format for level pacing, narrative beats, talk outlines, and motion storyboards. Use whenever a sequence's pacing matters.
report_id: beat_chart
title: Beat Chart
version: 1
universal: false
tags: [storytelling, level-design, narrative, motion]
produced_by: [level_designer, motion_designer, narrative_designer, presentation_story_architect]
output:
  tag: report:beat_chart
  format: table
  columns: [Beat, Purpose, Timing, Intensity]
  enums:
    Intensity: ['1', '2', '3', '4', '5']
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

# Beat Chart

A sequence laid out beat by beat, so pacing problems show up before production.

## When to use
For levels, quests, story arcs, talks, trailers, explainers, and storyboards: anything experienced in order over time.

## Produced by
- `level_designer`: spatial beats and the intensity curve, adding mechanic and wayfinding columns.
- `narrative_designer`: story beats mapped to gameplay moments.
- `presentation_story_architect`: talk sections with minutes, slide ideas, and speaker-note gist.
- `motion_designer`: shots and builds with duration, easing, and on-screen text.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:beat_chart role=ROLE_ID board=BOARD_ID -->
| # | Beat | Purpose | Timing | Intensity (1–5) | <role columns> |
<!-- /report:beat_chart -->
```

## Core fields (required)
- **Beat**: a short label, in order.
- **Purpose**: what this beat does for the audience or player (teach, test, rest, reveal, hook, ask).
- **Timing**: minutes, seconds, or estimated play time. All timings must sum to fit the slot.
- **Intensity**: 1–5, so the curve can be eyeballed. Use 1–2 beats for rest.

## How to fill it in
1. List the beats in order and give each a purpose. Cut beats that have no purpose.
2. Add timing and check the total against the slot or the target session length.
3. Rate intensity, read the curve, and add rest beats after peaks.

## On the board
Pacing disagreements (story vs. pace, builds vs. speaker rhythm) appear as `question` notes between the producers. The chart is the place to resolve them.

## Example

```markdown
<!-- report:beat_chart role=presentation_story_architect board=BB-DESIGN-REPLAY -->
| # | Beat | Purpose | Timing | Intensity | Slide idea |
|---|---|---|---|---|---|
| 1 | Cold open: the failed launch | hook | 1.5 min | 4 | outage graph |
| 2 | Why it happened | insight | 4 min | 3 | timeline |
| 3 | Audience poll | rest | 1 min | 1 | poll |
<!-- /report:beat_chart -->
```

## Quality checks
- [ ] Every beat has a purpose
- [ ] Timing fits the slot with 10% buffer
- [ ] A rest beat follows each intensity peak
