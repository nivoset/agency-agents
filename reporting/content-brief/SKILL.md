---
name: content-brief
description: Social content brief giving goal, audience, platform and format, CTA, success metric with check-in time, and timing. Use before writing any post, thread, carousel, video, or campaign.
---

# Content Brief

Every post gets one job, written down before anyone writes the copy.

## When to use
At the start of every social board.

## Produced by
- `social_strategist`: owns it.

## Template
```markdown
Goal: awareness | engagement | traffic | conversion | community
Audience: <specific segment>
Platform/format: <platform → native format>
CTA: <one action>
Metric: <number + check at T+48h>
Timing: <date/time + reason>
Pillar: <content pillar>
```

## Core fields (required)
- **Goal**: exactly one.
- **Audience**: specific, and present on the chosen platform.
- **Platform**: a native format for each platform.
- **CTA**: exactly one.
- **Metric**: chosen before posting, with a check-in time.

## How to fill it in
1. Choose the goal, then the audience.
2. Choose the platforms where that audience is, and a native format for each.
3. Set the CTA, the metric, and the timing. Check the news cycle for sensitive dates.

## On the board
Post it as round-1 `claim` notes. `hook_copywriter` and `platform_native_editor` write [draft variants](../draft-variants/SKILL.md) against it, and `community_response_forecaster` builds an [objection map](../objection-map/SKILL.md).

## Example
```markdown
Goal: conversion (waitlist) | Audience: eng managers, 20–200 person cos | Platform: LinkedIn carousel + X thread
CTA: join waitlist | Metric: 150 signups, check T+48h | Timing: Tue 9am PT
```

## Quality checks
- [ ] One goal and one CTA
- [ ] The metric is set before posting
- [ ] A native format for each platform
