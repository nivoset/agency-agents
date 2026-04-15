# Bug Bash

Systematic multi-inspector code review that produces user-facing test expectations and validated resolution options.

## Quick Start

```
Run a bug bash on [scope]
Focus: security, performance (or: all)
Depth: standard
```

## What You Get

Every finding includes:
- **Test expectation** in user language (not implementation details)
- **File:line evidence** with code snippet
- **1-3 resolution options** with effort/risk/breaking assessment
- **Extractable test name** for QA checklist

## Inspectors

### Core Inspectors
| Inspector | Focus |
|-----------|-------|
| **Security** | Injection, auth, secrets, validation |
| **Code Quality** | Error handling, resource leaks, logic bugs |
| **Performance** | N+1 queries, unbounded fetches, loops |
| **Accessibility** | Screen readers, keyboard, forms |
| **Data Integrity** | Validation, consistency, contracts |
| **Concurrency** | Races, double-submit, TOCTOU |

### Specialized Inspectors
| Inspector | Focus |
|-----------|-------|
| **Naming** | Variable clarity, test names as user expectations |
| **i18n** | Hardcoded strings, locale formatting, RTL |
| **Dependency** | CVEs, outdated packages, supply chain |
| **Documentation** | API docs vs code, outdated comments |

## Output Format

```markdown
## SEC-001: SQL Injection in Search

**Severity**: Critical

### Test Expectation
**As a** site visitor
**I expect** searching cannot execute database commands
**So that** the database stays secure

**Test Name**: `search_cannot_execute_sql_commands`

### Location
`src/api/search.js:42`

### Resolution Options
1. **Parameterized queries** — Effort: Low | Risk: None
2. **ORM query builder** — Effort: Medium | Risk: Low
```

## Depth Settings

| Depth | Time | Coverage |
|-------|------|----------|
| quick | ~2min/inspector | Surface scan, obvious issues |
| standard | ~5min/inspector | Thorough review |
| deep | ~10min/inspector | Exhaustive, edge cases |

## Workflow

1. **Intake**: Scope + focus areas + depth
2. **Dispatch**: Run inspectors in parallel via Task tool
3. **Collect**: Validate findings against schema
4. **Report**: Dedupe, sort by severity, generate roadmap

## Naming Inspector (Special)

The Naming Inspector has two modes:

**Variable Names**: Checks clarity, repo style consistency
```
NAME-001: Unclear Variable Name
Current: `d` → Suggested: `date`, `inputDate`, `dateToFormat`
```

**Test Names**: Ensures user behavior focus, no implementation details
```
NAME-002: Implementation-Focused Test Name
Current: `test_validatePassword_returns_false`
Suggested: `user_sees_error_for_password_under_8_characters`
```

### Bad Test Names (Rejected)
- `test_getUserById_returns_user` — implementation detail
- `test_login_works` — vague assertion
- `test_handleSubmit_calls_API` — technical jargon

### Good Test Names (Expected)
- `user_cannot_access_others_documents`
- `expired_session_redirects_to_login`
- `cart_total_updates_when_quantity_changes`

## Full Reference

See `bug-bash-orchestrator.md` for:
- Complete inspector profiles (10 total)
- Finding schema specification
- Report template
- Example findings for each category
