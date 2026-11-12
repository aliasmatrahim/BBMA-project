import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ANALYZER = Path(__file__).with_name("verify_custom_mtf_trace.py")
BASE = {
    "format": "custom-mtf-fixture-v1",
    "expected_identity": {"build": "fixture-build", "config": "fixture-config"},
    "identity": {"build": "fixture-build", "config": "fixture-config"},
    "required_cases": ["entry", "no-entry"],
    "cases": [
        {
            "id": "entry",
            "expected_sends": 1,
            "witnesses": [{"id": "w1", "trigger_id": "GBPUSD:M15:RE1:900", "closed_at": 900}],
            "sends": [{"witness_id": "w1", "sent_at": 901}],
        },
        {"id": "no-entry", "expected_sends": 0, "witnesses": [], "sends": []},
    ],
}


class TraceFixtureTests(unittest.TestCase):
    def run_fixture(self, fixture, expected_error=None):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp, "manifest.json")
            output = Path(tmp, "summary.json")
            manifest.write_text(json.dumps(fixture), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ANALYZER), "--manifest", str(manifest), "--output", str(output)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, int(expected_error is not None), result.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            if expected_error is None:
                self.assertEqual(summary["counts"], {"cases": 2, "witnesses": 1, "sends": 1})
                self.assertTrue(summary["limitations"])
            else:
                self.assertIn(expected_error, summary["errors"])

    def test_golden(self):
        self.run_fixture(BASE)

    def test_duplicate_physical_trigger(self):
        fixture = copy.deepcopy(BASE)
        case = fixture["cases"][0]
        case["witnesses"].append({**case["witnesses"][0], "id": "w2"})
        case["sends"].append({"witness_id": "w2", "sent_at": 902})
        case["expected_sends"] = 2
        self.run_fixture(fixture, "duplicate_send:entry")

    def test_unmatched_witness(self):
        fixture = copy.deepcopy(BASE)
        fixture["cases"][0]["sends"][0]["witness_id"] = "missing"
        self.run_fixture(fixture, "unmatched_witness:entry")

    def test_wrong_build_and_config(self):
        for key in ("build", "config"):
            with self.subTest(key=key):
                fixture = copy.deepcopy(BASE)
                fixture["identity"][key] = "wrong"
                self.run_fixture(fixture, "identity_mismatch")

    def test_look_ahead(self):
        fixture = copy.deepcopy(BASE)
        fixture["cases"][0]["sends"][0]["sent_at"] = 899
        self.run_fixture(fixture, "look_ahead:entry")

    def test_missing_required_case(self):
        fixture = copy.deepcopy(BASE)
        fixture["cases"].pop()
        self.run_fixture(fixture, "missing_case:no-entry")

    def test_missing_expected_send(self):
        fixture = copy.deepcopy(BASE)
        fixture["cases"][0]["sends"].clear()
        self.run_fixture(fixture, "send_count:entry")

    def test_invalid_timestamp_type(self):
        fixture = copy.deepcopy(BASE)
        fixture["cases"][0]["sends"][0]["sent_at"] = True
        self.run_fixture(fixture, "invalid_manifest")


if __name__ == "__main__":
    unittest.main()
