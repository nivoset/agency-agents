---
name: asset-manifest
description: Per-asset production list giving asset, spec, and status, plus role-specific columns. Use for sprites, illustrations, 3D models, animation clips, VFX, and sound events, or anything produced and tracked as discrete assets.
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
```markdown
| Asset | Spec | <role columns> | Owner | Status |
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
| sfx_parry_window | Spec: rising tone 100ms, priority 1, 3 variations | visual: rim flash | game_audio_designer | rough |
```

## Quality checks
- [ ] Names follow convention
- [ ] Specs are measurable
- [ ] Gameplay-critical audio has a visual equivalent
