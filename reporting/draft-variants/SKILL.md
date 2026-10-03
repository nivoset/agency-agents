---
name: draft-variants
description: Alternative drafts of a message, hook, or post (long/short, angles, or per-platform versions), each with its rationale. Use when producing replies, hooks, captions, or platform-native versions for the user to choose from.
report_id: draft_variants
title: Draft Variants
version: 1
universal: false
tags: [copywriting, persuasion]
produced_by: [diplomatic_wordsmith, hook_copywriter, platform_native_editor]
output:
  tag: report:draft_variants
  format: table
  columns: [Variant, Rationale]
  min_rows: 2
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

# Draft Variants

Gives the user real choices, each with the reasoning behind it.

## When to use
Whenever wording matters: conflict replies, hooks, captions, headlines, per-platform copy.

## Produced by
- `diplomatic_wordsmith`: long and short versions of a tense reply, with the principles applied.
- `hook_copywriter`: 3–5 hook variants by angle, with body and CTA.
- `platform_native_editor`: one version per platform, with specs, alt text, links, and timing.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:draft_variants role=ROLE_ID board=BOARD_ID -->
| Variant | <Angle / Platform / Length> | Draft | Rationale |
Recommended: <variant> because <...> | Test: <A vs B on metric> (optional)
<!-- /report:draft_variants -->
```

## Core fields (required)
- **Variant**: a label (Long, Short, A-outcome, LinkedIn).
- **Rationale**: why this draft works, naming the principle, angle, or platform norm.

## How to fill it in
1. Confirm the non-negotiables (from the [boundary brief](../boundary-brief/SKILL.md)) and the goal (from the [content brief](../content-brief/SKILL.md)).
2. Write the variants so they differ meaningfully, not as synonyms.
3. Give each a rationale, and recommend one.

## On the board
Drafts are `answer` notes. `community_response_forecaster` and `brand_voice_guardian` review them before the user chooses.

## Example

```markdown
<!-- report:draft_variants role=diplomatic_wordsmith board=BB-DESIGN-REPLAY -->
| Variant | Draft | Rationale |
|---|---|---|
| Long | "You're right that the second outage was preventable, and I'm sorry you got paged for it. I've focused on the critical paths and missed the alert rules. Could we pair on them tomorrow?" | concede the true part first; a request, not a demand |
| Short | "You're right, the second page was preventable. Sorry. Pair on alert rules tomorrow?" | same concession, sized for chat |
Recommended: Short, because the thread is already long
<!-- /report:draft_variants -->
```

## Quality checks
- [ ] Every variant keeps the non-negotiables
- [ ] Variants differ meaningfully
- [ ] It passes the screenshot test (fine if made public)
