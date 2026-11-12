import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parents[1] / "runtime/custom_mtf/t04be_hfm_h1_seed_probe_20261112.json"
EXPECTED = HERE / "hfm_seed_expected.json"


class NativeSeedEvidenceTests(unittest.TestCase):
    def check_evidence(self, evidence, expected_error=None):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory, "manifest.json")
            output = Path(directory, "result.json")
            manifest.write_text(json.dumps(evidence), encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(HERE / "verify_hfm_seed_evidence.py"),
                 "--manifest", str(manifest), "--expected", str(EXPECTED),
                 "--output", str(output)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(process.returncode, int(expected_error is not None), process.stderr)
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["recovery_acceptance"], "HOLD")
            if expected_error:
                self.assertIn(expected_error, result["errors"])
            else:
                self.assertEqual(result["case_count"], 2)
                self.assertEqual(result["owner_matches"], {"aug": True, "nov": False})

    def setUp(self):
        self.evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_recorded_native_evidence(self):
        self.check_evidence(self.evidence)

    def test_wrong_source_or_binary(self):
        for field in ("source_sha256", "binary_sha256"):
            with self.subTest(field=field):
                evidence = copy.deepcopy(self.evidence)
                evidence[field] = "0" * 64
                self.check_evidence(evidence, "identity_mismatch")

    def test_missing_case(self):
        self.evidence["markers"].pop(1)
        self.check_evidence(self.evidence, "marker_count")

    def test_duplicate_case(self):
        self.evidence["markers"][1] = self.evidence["markers"][0]
        self.check_evidence(self.evidence, "case_results_mismatch")

    def test_changed_owner_result(self):
        self.evidence["markers"][1] = self.evidence["markers"][1].replace("full_exact=false", "full_exact=true")
        self.check_evidence(self.evidence, "case_results_mismatch")

    def test_changed_dataset(self):
        self.evidence["cases"]["aug"]["csv_sha256"] = "0" * 64
        self.check_evidence(self.evidence, "case_inputs_mismatch")

    def test_compile_failure_or_runtime_exit(self):
        for field, value, error in (("compile", "Result: 1 errors, 0 warnings", "compile_failed"),
                                    ("exit", 1, "runtime_failed")):
            with self.subTest(field=field):
                evidence = copy.deepcopy(self.evidence)
                evidence[field] = value
                self.check_evidence(evidence, error)

    def test_order_observed(self):
        self.evidence["markers"][2] = self.evidence["markers"][2].replace("no_orders=true", "no_orders=false")
        self.check_evidence(self.evidence, "end_result_mismatch")

    def test_ambiguous_marker_field(self):
        self.evidence["markers"][0] += " full_exact=true"
        self.check_evidence(self.evidence, "invalid_manifest")


if __name__ == "__main__":
    unittest.main()
