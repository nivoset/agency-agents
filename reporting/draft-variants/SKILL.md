---
name: draft-variants
description: Alternative drafts of a message, hook, or post (long/short, angles, or per-platform versions), each with its rationale. Use when producing replies, hooks, captions, or platform-native versions for the user to choose from.
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
```markdown
| Variant | <Angle / Platform / Length> | Draft | Rationale |
Recommended: <variant> because <...> | Test: <A vs B on metric> (optional)
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
| Short | reply | "You're right the second outage was preventable, and I'm sorry you were paged. Pair on alert rules tomorrow?" | acknowledge true part; request, not demand |
```

## Quality checks
- [ ] Every variant keeps the non-negotiables
- [ ] Variants differ meaningfully
- [ ] It passes the screenshot test (fine if made public)
