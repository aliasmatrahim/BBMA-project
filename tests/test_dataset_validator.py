from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from tools.bbma_orchestrator.dataset_validator import validate_dataset_file


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _manifest(text: str, basis: str = "BID_ASK_BARS") -> dict:
    return {
        "run_id": "EXP-G1-001",
        "build": {"build_id": "BUILD-G1"},
        "hypothesis": {"parameter_sha256": _sha("parameters")},
        "dataset": {
            "sha256": _sha(text),
            "timeframe": "M15",
            "price_basis": basis,
            "start": "2026-01-01T00:00:00Z",
            "end": "2026-01-01T00:30:00Z",
            "warmup_start": "2026-01-01T00:00:00Z",
            "evaluation_start": "2026-01-01T00:00:00Z",
            "evaluation_end": "2026-01-01T00:30:00Z",
            "data_as_of": "2026-01-01T00:45:00Z",
            "closed_candles_only": True,
            "allowed_gap_windows": [],
        },
    }


def _bar(ts: str, bid: tuple[float, float, float, float], ask: tuple[float, float, float, float]) -> str:
    values = [ts, *map(str, bid), *map(str, ask)]
    return ",".join(values)


class DatasetValidatorTests(unittest.TestCase):
    def test_valid_closed_bid_ask_bars_pass(self):
        header = "timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close\n"
        body = (
            _bar("2026-01-01T00:00:00Z", (1.1000, 1.1010, 1.0990, 1.1005), (1.1002, 1.1012, 1.0992, 1.1007)) + "\n"
            + _bar("2026-01-01T00:15:00Z", (1.1005, 1.1020, 1.1000, 1.1015), (1.1007, 1.1022, 1.1002, 1.1017)) + "\n"
        )
        text = header + body
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, _manifest(text))
        self.assertEqual(result["dataset_status"], "VALID", result["errors"])
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["gap_count"], 0)

    def test_duplicate_timestamp_and_non_monotonic_rows_fail(self):
        header = "timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close\n"
        row = _bar("2026-01-01T00:00:00Z", (1.1, 1.11, 1.09, 1.105), (1.1002, 1.1102, 1.0902, 1.1052))
        text = header + row + "\n" + row + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, _manifest(text))
        self.assertEqual(result["duplicate_timestamps"], 1)
        self.assertTrue(any("duplicate timestamp" in error for error in result["errors"]))

    def test_gap_is_reported_and_fails_without_explicit_closure_window(self):
        header = "timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close\n"
        rows = [
            _bar("2026-01-01T00:00:00Z", (1.1, 1.11, 1.09, 1.105), (1.1002, 1.1102, 1.0902, 1.1052)),
            _bar("2026-01-01T00:30:00Z", (1.105, 1.115, 1.10, 1.11), (1.1052, 1.1152, 1.1002, 1.1102)),
        ]
        text = header + "\n".join(rows) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, _manifest(text))
        self.assertEqual(result["gap_count"], 1)
        self.assertTrue(any("timestamp gap" in error for error in result["errors"]))

    def test_inconsistent_ohlc_and_ask_below_bid_fail(self):
        header = "timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close\n"
        text = header + _bar(
            "2026-01-01T00:00:00Z",
            (1.1, 1.09, 1.08, 1.105),
            (1.099, 1.10, 1.07, 1.104),
        ) + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, _manifest(text))
        self.assertTrue(any("inconsistent" in error for error in result["errors"]))
        self.assertTrue(any("Ask OHLC is below" in error for error in result["errors"]))

    def test_tick_timestamps_need_not_align_to_candle_boundary(self):
        text = (
            "timestamp,bid,ask\n"
            "2026-01-01T00:00:01Z,1.1000,1.1002\n"
            "2026-01-01T00:14:59Z,1.1010,1.1012\n"
        )
        manifest = _manifest(text, "BID_ASK_TICKS")
        manifest["dataset"]["end"] = "2026-01-01T00:15:00Z"
        manifest["dataset"]["evaluation_end"] = "2026-01-01T00:15:00Z"
        manifest["dataset"]["data_as_of"] = "2026-01-01T00:30:00Z"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ticks.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, manifest, max_gap_seconds=900)
        self.assertEqual(result["dataset_status"], "VALID", result["errors"])

    def test_tick_gap_above_declared_threshold_fails(self):
        text = (
            "timestamp,bid,ask\n"
            "2026-01-01T00:00:01Z,1.1000,1.1002\n"
            "2026-01-01T00:14:59Z,1.1010,1.1012\n"
        )
        manifest = _manifest(text, "BID_ASK_TICKS")
        manifest["dataset"]["end"] = "2026-01-01T00:15:00Z"
        manifest["dataset"]["evaluation_end"] = "2026-01-01T00:15:00Z"
        manifest["dataset"]["data_as_of"] = "2026-01-01T00:30:00Z"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ticks.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, manifest, max_gap_seconds=60)
        self.assertTrue(any("timestamp gap" in error for error in result["errors"]))

    def test_incomplete_candle_window_and_data_as_of_fail(self):
        text = (
            "timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close\n"
            + _bar("2026-01-01T00:00:00Z", (1.1, 1.11, 1.09, 1.105), (1.1002, 1.1102, 1.0902, 1.1052)) + "\n"
        )
        manifest = _manifest(text)
        manifest["dataset"]["data_as_of"] = "2026-01-01T00:10:00Z"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bars.csv"
            path.write_text(text, encoding="utf-8")
            result = validate_dataset_file(path, manifest)
        self.assertTrue(any("data_as_of" in error for error in result["errors"]))
        self.assertTrue(any("does not cover through" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
