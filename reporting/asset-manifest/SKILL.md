---
name: asset-manifest
description: Per-asset production list giving asset, spec, and status, plus role-specific columns. Use for sprites, illustrations, 3D models, animation clips, VFX, and sound events, or anything produced and tracked as discrete assets.
report_id: asset_manifest
title: Asset Manifest
version: 1
universal: false
tags: [2d, 3d, animation, audio, vfx]
produced_by: [animator_2d, animator_3d, game_audio_designer, illustrator_2d, modeler_3d, vfx_artist]
output:
  tag: report:asset_manifest
  format: table
  columns: [Asset, Spec, Status]
  enums:
    Status: [planned, thumbnail, rough, final, in-engine, approved]
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

# Asset Manifest

One row per deliverable asset, so production, review, and import can be tracked.

## When to use
When a board's output includes art, animation, effects, or audio assets.

## Produced by
- `illustrator_2d`: 2D artwork with display size, format, palette, and source file.
- `animator_2d`: 2D animations with technique, frames@fps, key poses, and loops.
- `modeler_3d`: 3D assets with tris per LOD, texel density, materials, and collision.
- `animator_3d`: clips with loop, root motion, cancels, and blends.
- `vfx_artist`: effects with telegraph, impact, aftermath, color code, and LOD.
- `game_audio_designer`: sound events with priority, variations, and visual equivalent.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:asset_manifest role=ROLE_ID board=BOARD_ID -->
| Asset | Spec | <role columns> | Owner | Status |
<!-- /report:asset_manifest -->
```

## Core fields (required)
- **Asset**: a convention-correct name (`chr_knight_attack_01`).
- **Spec**: the measurable spec for this asset type (size or format, frames@fps, tris, duration).
- **Status**: `planned`, `thumbnail`, `rough`, `final`, `in-engine`, or `approved`.

## How to fill it in
1. List the assets from the design (the [mechanic sheet](../mechanic-sheet/SKILL.md), [beat chart](../beat-chart/SKILL.md), or brief).
2. Fill each spec from the [style guide](../style-guide/SKILL.md) and the [budget sheet](../budget-sheet/SKILL.md).
3. Update status at each review checkpoint.

## On the board
`art_director` reviews against the manifest using a [findings table](../findings-table/SKILL.md). `technical_artist` checks specs against budgets.

## Example

```markdown
<!-- report:asset_manifest role=game_audio_designer board=BB-DESIGN-REPLAY -->
| Asset | Spec | Visual equivalent | Owner | Status |
|---|---|---|---|---|
| sfx_parry_window | rising tone 100ms, priority 1, 3 variations | rim flash | game_audio_designer | rough |
| sfx_dash | whoosh 150ms, priority 2, 4 variations | motion trail | game_audio_designer | final |
<!-- /report:asset_manifest -->
```

## Quality checks
- [ ] Names follow convention
- [ ] Specs are measurable
- [ ] Gameplay-critical audio has a visual equivalent
