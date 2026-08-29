#!/usr/bin/env python3
"""Lock C1-A golden fixtures to the canonical current-source boundaries."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")
CONTRACT = Path(
    "blueprint/contracts/BBMA_CORE_CANONICAL_TRUTH_TABLE_CONTRACT.md"
).read_text(encoding="utf-8")
QUEUE = Path(
    "blueprint/implementation/BBMA_CORE_PERFECTION_QUEUE_20260829.md"
).read_text(encoding="utf-8")


def function_body(name: str) -> str:
    declaration = re.search(
        rf"(?m)^[A-Za-z_][^\r\n]*\b{re.escape(name)}\s*\(", SRC
    )
    if declaration is None:
        raise AssertionError(f"missing function: {name}")
    start = declaration.start()
    brace = SRC.find("{", start)
    if brace < 0:
        raise AssertionError(f"missing function body: {name}")
    depth = 0
    for index in range(brace, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:index + 1]
    raise AssertionError(f"unterminated function: {name}")


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing canonical marker: {marker}")


def require_in_order(text: str, *markers: str) -> None:
    cursor = -1
    for marker in markers:
        found = text.find(marker, cursor + 1)
        if found < 0:
            raise AssertionError(f"missing/ordered canonical marker: {marker}")
        cursor = found


def main() -> None:
    require(
        SRC,
        "Version 4.7.2 - Offline Tester Symbol Compatibility",
        '#property version   "4.72"',
        "bool           EnableC044Lifecycle                = false;",
        "bool           EnableD1TPWLifecycle               = false;",
    )

    clock = function_body("IsNewCandle")
    require(clock, "GetLatestClosedCandleTime(pair, PERIOD_M15)")
    for forbidden in ("PERIOD_M1", "PERIOD_M5", "PERIOD_M30", "PERIOD_W1"):
        if re.search(rf"\b{forbidden}\b", clock):
            raise AssertionError(f"processing clock escaped M15: {forbidden}")

    extreme = function_body("UpdateExtremeLifecycle")
    require(
        extreme,
        "IsExtremeLifecycleInvalidation(pair, direction, data, band)",
        "EXT_MAT_REVERSAL_CONFIRMED",
        "EXT_MAT_RETEST_PHASE",
        "EXT_MAT_RETEST_READY",
    )
    if extreme.find("IsExtremeLifecycleInvalidation") > extreme.find("if(extreme.Maturity == EXT_MAT_RAW)"):
        raise AssertionError("Extreme invalidation no longer precedes maturity promotion")

    mhv = function_body("UpdateCanonicalMLVState")
    require(
        mhv,
        "MLV_PARENT_READY",
        "MLV_TP_COMPLETE",
        "MLV_LOSS_DEVELOPING",
        "MLV_FORMATION_ESTABLISHED",
        "MLV_RETEST_COMPLETE",
        "MLV_DIRECTION_TAKEN",
        "TryAdvanceMHVSupersessionFromCanonicalParent",
    )
    require(SRC, "M09 NEVER detects, resets, promotes or mutates", "M08 owns the canonical parent lifecycle completely")

    csm = function_body("DetectCSM")
    require(csm, "currentBand.Width > previousBand.Width", "close > currentBand.TOP_BB", "close < currentBand.LOW_BB")
    csd = function_body("DetectCSD")
    require(csd, "ma.MA5_High", "ma.MA10_High", "band.MID_BB", "ma.MA5_Low", "ma.MA10_Low")
    ecsd = function_body("DetectECSD")
    if "MID_BB" in ecsd:
        raise AssertionError("eCSD unexpectedly acquired MID-BB authority")

    re_start = function_body("TryStartSpecificReEntry")
    require_in_order(re_start, "DetectReEntry_Type3", "DetectReEntry_Type4", "DetectReEntry_Type2")
    re_update = function_body("UpdateReEntryState")
    require(
        re_update,
        "IsReEntryIntrinsicExpired",
        "IsType1StructuralRetraceEvidence",
        "HasReEntryMAClusterTouch",
        "HasReEntryMA5OrMA50Touch",
        "RE_TYPE_4_CSD",
    )

    combinations = function_body("BuildPossibleCombinations")
    for marker in (
        "FinalizeCombinationCandidate(rem, SIGNAL_REM)",
        "FinalizeCombinationCandidate(rre, SIGNAL_RRE)",
        "FinalizeCombinationCandidate(ree, SIGNAL_REE)",
        "PERIOD_D1",
        "PERIOD_H4",
        "PERIOD_H1",
        "PERIOD_M15",
    ):
        require(combinations, marker)
    validation = function_body("ValidateSequence")
    require(validation, "ValidateCombinationSignature", "ValidateDirectionConsistency")

    process_pair = function_body("ProcessPair")
    require(process_pair, "PriorityEngine_Atomic(", "NMJE_PrintValidatedDecisionShadow")
    if "OrderSend(" in process_pair:
        raise AssertionError("ProcessPair unexpectedly owns OrderSend")
    if SRC.count("OrderSend(") != 1:
        raise AssertionError("M22 is no longer the sole OrderSend source owner")

    for marker in (
        "C1-A AUDIT LOCK / NO SOURCE OR STRATEGY CHANGE",
        "M15 is the sole processing and final-decision clock",
        "RAW is not exportable",
        "Specific ownership precedence is Type 3",
        "M13 may collect these signatures. M14 may validate them",
        "No daily-loss limit or gate may be added",
    ):
        require(CONTRACT, marker)
    require(QUEUE, "C1 — Canonical BBMA truth tables and golden fixtures")

    print("BBMA_CORE_CANONICAL_SOURCE_STATIC=PASS")


if __name__ == "__main__":
    main()
