from pathlib import Path
import re

SRC = Path(__file__).parents[1] / "source" / "BBMA_EA.mq4"
TEXT = SRC.read_text(encoding="utf-8")


def body(name: str) -> str:
    marker = f"{name}("
    start = TEXT.index(marker)
    brace = TEXT.index("{", start)
    depth = 0
    for i in range(brace, len(TEXT)):
        if TEXT[i] == "{":
            depth += 1
        elif TEXT[i] == "}":
            depth -= 1
            if depth == 0:
                return TEXT[brace : i + 1]
    raise AssertionError(f"unterminated function: {name}")


def test_mode2_admits_only_retest_ready_h1_standalone_extreme():
    mode = body("IsEntryModeCandidateAllowed")
    build = body("BuildStandaloneExtremeCandidate")
    assert "candidate.SequenceType == SIGNAL_EXTREME" in mode
    assert "EntryMode != MODE_2_ALL_VALIDATED_BBMA" in build
    assert "extreme.Maturity != EXT_MAT_RETEST_READY" in build
    assert "extreme.Timeframe != PERIOD_H1" in build
    assert "extreme.RetestCompletionCandleTime" in build

def test_m16_revalidates_exact_retest_ready_lifecycle_identity():
    fn = body("IsPersistentExtremeComponentValid")
    assert "EXT_MAT_RETEST_READY" in fn
    assert "RetestCompletionCandleTime == component.CandleTime" in fn
    assert "RawCandleTime" in fn


def test_m17_extreme_sl_uses_locked_raw_to_retest_window_and_three_pips():
    assert re.search(r"EXTREME_WICK_BUFFER_PIPS\s+3\.0", TEXT)
    fn = body("ResolveStandaloneExtremeStructuralAnchor")
    assert "startTime = extreme.RawCandleTime" in fn
    assert "completionTime = extreme.RetestCompletionCandleTime" in fn
    assert "for(int shift = completionShift; shift <= rawShift; shift++)" in fn
    resolver = body("ResolveApprovedInitialSLTP")
    assert "EXTREME_WICK_BUFFER_PIPS * pipValue" in resolver


def test_extreme_tp_targets_first_edge_of_opposite_ma5_ma10_area():
    fn = body("ResolveStandaloneExtremeTPWajib")
    assert "BBMAHighMA" in fn
    assert "BBMALowMA" in fn
    assert "MathMin(ma5, ma10)" in fn
    assert "MathMax(ma5, ma10)" in fn


def test_build_identity_is_unique_for_q5_implementation():
    assert "Version 4.84 - Q5 Standalone Extreme Execution" in TEXT
    assert '#property version   "4.84"' in TEXT
