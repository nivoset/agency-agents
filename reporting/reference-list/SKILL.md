---
name: reference-list
description: Annotated list of precedents and examples, giving the example, its source, what to borrow, and what to avoid. Use before inventing an approach, to bring prior art, competitor examples, internal implementations, or reference art onto the board.
---

# Reference List

Gives the board real examples to argue from, so it doesn't start from first principles.

## When to use
When a role asks "how do others do this?", or before a design or approach is chosen.

## Produced by
- `prior_art_scout`: the repository first, then the outside world.

## Template
```markdown
| Ref | Example | Source | Borrow | Avoid |
| R1 | <what it is> | <path / URL / title, year> | <specific element to reuse> | <specific pitfall> |
```

## Core fields (required)
- **Ref**: `R1`, `R2`, and so on, for citing in notes.
- **Example**: the thing, named concretely.
- **Source**: verifiable. Use a repository path, a URL, or a title and year.
- **Borrow** / **Avoid**: specific elements, not "good UX".

## How to fill it in
1. Search the repository for existing implementations. These outrank outside examples.
2. Collect 3–7 references. Prefer ones that shipped, with known outcomes.
3. Annotate what to borrow and what to avoid from each.

## On the board
Post an `answer` note when a reference resolves an open question, citing `R#`. Other roles cite `R#` as evidence in their notes.

## Example
```markdown
| R1 | Existing note renderer | components/blackboard/note-card.tsx | kind/confidence badges | n/a: reuse directly |
```

## Quality checks
- [ ] Every source is verifiable
- [ ] The repository was searched first
- [ ] Borrow and Avoid are specific
