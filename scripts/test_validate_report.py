#!/usr/bin/env python3
"""Tests for scripts/validate_report.py. Run: python3 scripts/test_validate_report.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_report import load_roles, load_specs, validate_text  # noqa: E402

SPECS, ROLES = load_specs(), load_roles()


def problems(text, **kw):
    return [msg for _, _, msg in validate_text(text, SPECS, ROLES, **kw)[1]]


RISKS = """<!-- report:risk_register role=red_team_skeptic board=BB-1 -->
| # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | If X then Y | M | H | test Z | qa | {status} |
<!-- /report:risk_register -->"""


class ValidateReportTests(unittest.TestCase):
    def test_valid_table_report(self):
        self.assertEqual(problems(RISKS.format(status="mitigated")), [])

    def test_enum_violation(self):
        self.assertTrue(any("Status='kinda done'" in p for p in problems(RISKS.format(status="kinda done"))))

    def test_role_that_does_not_produce_report(self):
        text = RISKS.format(status="open").replace("red_team_skeptic", "hook_copywriter")
        self.assertTrue(any("does not produce risk_register" in p for p in problems(text)))

    def test_unknown_role_and_report(self):
        self.assertTrue(any("unknown role" in p for p in problems(RISKS.format(status="open").replace("red_team_skeptic", "nobody"))))
        self.assertTrue(any("unknown report type" in p for p in problems("<!-- report:nope role=red_team_skeptic -->\nx\n<!-- /report:nope -->")))

    def test_missing_column(self):
        text = RISKS.format(status="open").replace("| Mitigation ", "| Plan ")
        self.assertTrue(any("no table with columns" in p for p in problems(text)))

    def test_unclosed_and_mismatched_tags(self):
        self.assertTrue(any("never closed" in p for p in problems("<!-- report:risk_register role=red_team_skeptic -->\n| Risk |")))
        self.assertTrue(any("no matching open tag" in p for p in problems("<!-- /report:risk_register -->")))

    def test_role_must_return_all_declared_reports(self):
        # qa_test_strategist declares test_plan and risk_register
        text = RISKS.format(status="open").replace("red_team_skeptic", "qa_test_strategist")
        self.assertTrue(any("did not return required report 'test_plan'" in p for p in problems(text, role="qa_test_strategist")))

    def test_require_flag(self):
        self.assertTrue(any("required report 'findings_table'" in p for p in problems(RISKS.format(status="open"), require=["findings_table"])))

    def test_fields_report_labels_and_enum(self):
        good = """<!-- report:boundary_brief role=boundary_keeper -->
Non-negotiables: keep the bug report
Risk: high (threats in replies)
Boundary statements: "I'll step away."
Escalation: block and report
<!-- /report:boundary_brief -->"""
        self.assertEqual(problems(good), [])
        self.assertTrue(any("missing 'Escalation:'" in p for p in problems(good.replace("Escalation: block and report\n", ""))))
        self.assertTrue(any("Risk:" in p for p in problems(good.replace("Risk: high", "Risk: spicy"))))

    def test_yaml_board_note(self):
        good = """<!-- report:board_note role=end_user_advocate -->
kind: claim
body: "Tool rail buttons have no handler."
confidence: high
refersTo: null
<!-- /report:board_note -->"""
        self.assertEqual(problems(good), [])
        self.assertTrue(any("kind='rant'" in p for p in problems(good.replace("kind: claim", "kind: rant"))))
        self.assertTrue(any("missing key 'confidence'" in p for p in problems(good.replace("confidence: high\n", ""))))

    def test_gherkin_steps(self):
        good = """<!-- report:acceptance_cases role=end_user_advocate -->
Scenario: works
  Given a state
  When an action
  Then a result
<!-- /report:acceptance_cases -->"""
        self.assertEqual(problems(good), [])
        self.assertTrue(any("missing 'Then'" in p for p in problems(good.replace("  Then a result\n", ""))))

    def test_min_rows(self):
        one = """<!-- report:draft_variants role=hook_copywriter -->
| Variant | Hook | Rationale |
|---|---|---|
| A | "Hook" | outcome angle |
<!-- /report:draft_variants -->"""
        self.assertTrue(any("at least 2 row(s)" in p for p in problems(one)))

    def test_tags_inside_code_fences_are_found(self):
        fenced = "```markdown\n" + RISKS.format(status="accepted") + "\n```"
        blocks, probs = validate_text(fenced, SPECS, ROLES)
        self.assertEqual([b["id"] for b in blocks], ["risk_register"])
        self.assertEqual(probs, [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
