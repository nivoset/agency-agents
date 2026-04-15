# Diplomatic Response Crafter Agent — Strategic Plan

## Executive Summary

Create a channel-agnostic communication specialist agent that applies Dale Carnegie's "How to Win Friends and Influence People" principles to rewrite replies to negative comments. The agent produces two versions (thoughtful long, concise short) plus a tactical explanation of principles applied.

**Methodology**: Single vertical slice (one agent file with complete functionality)
**Critical Path**: Research → Draft Agent → Validate → Integrate
**Division Placement**: `specialized/` (channel-agnostic influence craft)

---

## Phase 1: Foundation

**Goal**: Verify prerequisites and confirm placement
**Entry criteria**: User request to create agent
**Exit criteria**: Confirmed file path, no duplicates, structure understood

### Epic 1.1: Repository Analysis

**Depends on**: None
**Blocks**: Agent creation
**Parallelizable**: Yes

#### Scope Items
1. Verify `specialized/` directory exists and naming patterns
2. Confirm no existing diplomatic/Carnegie-based agent
3. Review similar agents (Support Responder, Reddit Community Builder, Cultural Intelligence Strategist)

#### Requirements (Done-when)
- [x] Directory structure confirmed
- [x] No duplicate agent exists
- [x] YAML frontmatter format documented
- [x] Similar agent patterns reviewed

---

## Phase 2: Agent Definition

**Goal**: Create complete, production-ready agent file
**Entry criteria**: Phase 1 complete
**Exit criteria**: Agent file passes all guardrail checks

### Epic 2.1: Core Agent Structure

**Depends on**: 1.1
**Blocks**: Integration
**Parallelizable**: No

#### Scope Items
1. YAML frontmatter (name, description, color, emoji, vibe)
2. Identity & Memory section
3. Core Mission section
4. Critical Rules (addressing adversarial findings)

#### Requirements (Done-when)
- [ ] Frontmatter follows repo pattern
- [ ] Identity establishes Carnegie expertise
- [ ] Mission scopes to "rewrite replies" not "own all comms"
- [ ] Rules address: no escalation, preserve intent, no fake agreement, dash rule

### Epic 2.2: Workflow Definition

**Depends on**: 2.1
**Blocks**: Deliverables
**Parallelizable**: Partial

#### Scope Items
1. Input contract (what user must provide)
2. Analysis phase (concern extraction, principle selection)
3. Drafting phase (long then short)
4. Verification phase (guardrail checks)
5. Output phase (tactical explanation)

#### Requirements (Done-when)
- [ ] Input fields explicitly defined
- [ ] Principle selection rubric documented
- [ ] Long/short consistency rule stated
- [ ] Verification includes dash hunting
- [ ] Tactical explanation structure defined

### Epic 2.3: Guardrails & Safety

**Depends on**: 2.1
**Blocks**: None (can be parallel with 2.2)
**Parallelizable**: Yes

#### Scope Items
1. No escalation rule WITH safety exceptions
2. Carnegie vs fake agreement distinction
3. Intent preservation mechanism
4. Dash rule enforcement
5. Human-in-the-loop requirement

#### Requirements (Done-when)
- [ ] Safety exceptions documented (abuse, threats, legal)
- [ ] "Validate emotion vs validate claim" distinction clear
- [ ] Intent bullets required before drafting
- [ ] Dash rule includes verification step and forbidden patterns
- [ ] Explicit "human reviews before sending" statement

### Epic 2.4: Differentiation & Integration Notes

**Depends on**: 2.1
**Blocks**: Documentation
**Parallelizable**: Yes

#### Scope Items
1. "When to use this agent" section
2. "When to use Support Responder instead" section
3. Optional CQ (Cultural Intelligence) integration note

#### Requirements (Done-when)
- [ ] Clear use-case boundaries defined
- [ ] Overlap with Support Responder addressed
- [ ] Cross-reference to Cultural Intelligence Strategist for global contexts

---

## Phase 3: Integration

**Goal**: Ensure agent works with repo tooling
**Entry criteria**: Agent file complete
**Exit criteria**: Agent discoverable and usable

### Epic 3.1: Validation & Testing

**Depends on**: 2.1, 2.2, 2.3, 2.4
**Blocks**: None
**Parallelizable**: No

#### Scope Items
1. Verify YAML frontmatter parses correctly
2. Run convert.sh to generate tool integrations
3. Verify agent appears in listings

#### Requirements (Done-when)
- [ ] No YAML syntax errors
- [ ] convert.sh completes without errors
- [ ] Agent appears in the-agency listings

---

## Dependency Graph

```
1.1 Repository Analysis
     │
     ▼
2.1 Core Agent Structure
     │
     ├──────────┬──────────┐
     ▼          ▼          ▼
2.2 Workflow  2.3 Safety  2.4 Differentiation
     │          │          │
     └──────────┴──────────┘
                │
                ▼
        3.1 Validation
```

---

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Carnegie principles misapplied as manipulation | CRITICAL | Explicit "no fake agreement" rule with examples |
| "No escalation" blocks safety responses | CRITICAL | Document exceptions for abuse/threats/legal |
| Dash rule ignored by model | RISK | Verification step with forbidden patterns |
| Overlap with Support Responder | RISK | "When to use" section with clear boundaries |
| Short version drops commitments | RISK | Explicit "short is compression, not different deal" rule |

---

## Adversarial Findings Addressed

### CRITICAL Issues
1. **Carnegie vs fake agreement**: Added explicit distinction between "validate emotion" vs "validate claim"
2. **No escalation safety exceptions**: Documented that abuse, threats, and legal matters bypass warm tone
3. **Human-in-the-loop**: Explicitly stated in agent purpose

### RISK Issues
1. **Input contract**: Defined required fields in workflow
2. **Support Responder overlap**: Added differentiation section
3. **Dash enforcement**: Verification step with forbidden Unicode characters
4. **Short/long consistency**: Explicit rule that short cannot add or remove commitments

---

## Implementation Checklist

- [ ] Create `specialized/specialized-diplomatic-response-crafter.md`
- [ ] Verify YAML frontmatter
- [ ] Run `./scripts/convert.sh` 
- [ ] Verify agent appears in `the-agency specialized` listing
- [ ] Remove `htwfaip.txt` (book content not needed in repo)
