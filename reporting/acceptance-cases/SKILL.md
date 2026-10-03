---
name: acceptance-cases
description: Given/When/Then scenarios that define done, including failure, recovery, and preservation cases. Use when writing acceptance criteria, listing missing scenarios, or handing behavior to QA.
---

# Acceptance Cases

Behavior written as checks a tester or a test can run.

## When to use
For every must-have item, and whenever a reviewer finds a missing scenario.

## Produced by
- `end_user_advocate`: missing failure, recovery, accessibility, and preservation scenarios.
- `product_manager`: the primary success scenarios for each must-have.

## Template
```gherkin
Scenario: <short name>                 # tag: @happy @failure @recovery @a11y @preserve
  Given <starting state>
  When <user action or event>
  Then <observable result>
```

## Core fields (required)
- **Given**: concrete state, including data and the user's position.
- **When**: one action or event.
- **Then**: an observable outcome. Never "works correctly".

## How to fill it in
1. Write the happy path.
2. Add one failure scenario and one recovery scenario for each step that can fail.
3. Add `@preserve` scenarios for existing behavior the change must not break.
4. Add `@a11y` scenarios for keyboard and screen-reader paths.

## On the board
Post a missing scenario as a `claim` note. The [test plan](../test-plan/SKILL.md) maps each scenario to a test, and the [ticket drafts](../ticket-drafts/SKILL.md) cite them as acceptance evidence.

## Example
```gherkin
Scenario: Arrow keys don't steal textarea input   @preserve
  Given the replay is at v5 and the risk textarea is focused
  When the user presses ArrowLeft
  Then the selected version is still v5
```

## Quality checks
- [ ] Every Then is observable
- [ ] Failure and recovery are covered for every risky step
- [ ] Existing flows have `@preserve` cases
