"""Exact-source regression for D1 TPW transition fail-closed authority."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "blueprint/source/BBMA_EA.mq4"


def source_block(source, signature):
    start = source.index(signature)
    brace = source.index("{", start)
    depth = 0
    for end in range(brace, len(source)):
        depth += (source[end] == "{") - (source[end] == "}")
        if depth == 0:
            return source[start:end + 1]
    raise AssertionError(signature)


class D1TPWTransitionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_m15_tpw_requires_confirmed_d1_but_keeps_counter_direction_path(self):
        body = source_block(self.source, "bool IsD1OpportunityCandidateAuthorityReady(")
        branch = re.search(
            r"if\s*\(opportunity\.Family\s*==\s*D1_OPP_EXTREME_TPW\)\s*return\s+([^;]+);",
            body)
        self.assertIsNotNone(branch)
        self.assertEqual(branch.group(1), "IsD1MajorTrendOwnerExecutionReady(pairState)")
        self.assertNotIn("candidate.Direction == pairState.d1_major_trend_owner.Direction",
                         body[branch.start():branch.end()])

    def test_m16_tpw_revalidates_confirmed_d1_without_direction_alignment(self):
        body = source_block(self.source, "bool ValidateDecisionD1OpportunitySnapshot(")
        gate = re.search(
            r"else\s+if\s*\(\s*!IsD1MajorTrendOwnerExecutionReady\(state\)\s*\)\s*return false;",
            body)
        self.assertIsNotNone(gate)
        self.assertIn("if(decision.Direction != owner.Direction) return false;", body)
        tail = body[gate.end():body.index("return true;", gate.end())]
        self.assertNotIn("decision.Direction != owner.Direction", tail)

    def test_confirmed_owner_helper_rejects_transition_and_unresolved(self):
        body = source_block(self.source, "bool IsD1MajorTrendOwnerExecutionReady(")
        returns = re.findall(r"return\s+([^;]+);", body)
        self.assertEqual(returns, [
            "false",
            "(owner.Direction == DIR_BUY)",
            "(owner.Direction == DIR_SELL)",
            "false",
        ])

    def test_build_identifier_is_unique_and_left_aligned(self):
        header = self.source.splitlines()[:5]
        self.assertTrue(any(line.startswith("//| Version 5.2.3 - D1 TPW Transition Fail-Closed Gate")
                            for line in header))
        self.assertIn('#property version   "5.23"', self.source)
        self.assertIn('BBMA_BUILD_TAG      "V523_D1_TPW_TRANSITION_FAIL_CLOSED_20261027"',
                      self.source)


if __name__ == "__main__":
    unittest.main()
