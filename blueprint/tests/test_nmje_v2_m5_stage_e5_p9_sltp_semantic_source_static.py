#!/usr/bin/env python3
"""Stage-E5 P9 SL/TP semantic-source audit firewall."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def function_body(name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\([^)]*\)\s*\{{", SRC, re.S)
    if not match:
        raise AssertionError(f"missing function: {name}")
    start = match.end() - 1
    depth = 0
    for index in range(start, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start + 1:index]
    raise AssertionError(f"unterminated function: {name}")


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing marker: {marker}")


def main() -> None:
    resolver = function_body("ResolveSelectedSLTPSourceComponent")
    require(
        resolver,
        "selected.SequenceType == SIGNAL_RE_ENTRY && selected.UsesD1Opportunity",
        "int preferredTf = (pass == 0) ? PERIOD_H1 : PERIOD_M15;",
        "component.Timeframe != preferredTf",
        "selected.SequenceType == SIGNAL_RE_ENTRY",
        "expectedTf = PERIOD_H1;",
        "selected.SequenceType == SIGNAL_REM",
        "expectedTf = PERIOD_H4;",
        "selected.SequenceType == SIGNAL_RRE",
        "selected.SequenceType == SIGNAL_REE",
        "expectedTf = PERIOD_D1;",
        "component.Timeframe != expectedTf",
        "component.Direction != selected.Direction",
        "component.CandleTime <= 0",
    )
    if resolver.index("PERIOD_H1 : PERIOD_M15") > resolver.index(
        "component.Timeframe != preferredTf"
    ):
        raise AssertionError("D1-opportunity semantic preference is not explicit")
    for forbidden in (
        "GetCandidateAnchorTime",
        "CompareCanonicalCandidates",
        "SequenceStartTime",
        "SequenceHash",
        "Latest",
        "newest",
    ):
        if forbidden in resolver:
            raise AssertionError(f"semantic source depends on accidental order: {forbidden}")

    # M15 freezes the semantic owner exactly once, after canonical selection.
    priority = function_body("PriorityEngine_Atomic")
    require(
        priority,
        "decision.HasSLTPSourceComponent =",
        "ResolveSelectedSLTPSourceComponent(selected, decision.SLTPSourceComponent);",
        "FreezeNMJEShadowSnapshot(pairState, decision);",
    )
    if priority.index("ResolveSelectedSLTPSourceComponent") > priority.index(
        "FreezeNMJEShadowSnapshot"
    ):
        raise AssertionError("SL/TP owner is not frozen before shadow attribution")
    if SRC.count("ResolveSelectedSLTPSourceComponent(") != 2:
        raise AssertionError("semantic owner is re-resolved outside definition/M15 selection")

    approved = function_body("IsApprovedSLTPSourceComponent")
    require(
        approved,
        "source.ComponentType != SIGNAL_RE_ENTRY",
        "source.Direction != decision.Direction",
        "decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY",
        "source.Timeframe == PERIOD_H1 || source.Timeframe == PERIOD_M15",
        "return (source.Timeframe == PERIOD_H1);",
        "decision.SignalType == SIGNAL_REM",
        "return (source.Timeframe == PERIOD_H4);",
        "decision.SignalType == SIGNAL_RRE",
        "decision.SignalType == SIGNAL_REE",
        "return (source.Timeframe == PERIOD_D1);",
    )

    lifecycle = function_body("ResolveMatchingReEntryLifecycle")
    require(
        lifecycle,
        "reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid",
        "reEntry.Direction != source.Direction",
        "reEntry.Timeframe != source.Timeframe",
        "reEntry.ConfirmationCandle != source.CandleTime",
        "reEntry.StartCandleTime > reEntry.ConfirmationCandle",
        "re_h1_buy_state",
        "re_h4_buy_state",
        "re_d1_buy_state",
        "re_m15_buy_state",
    )

    anchor = function_body("ResolveSourceOwnedStructuralAnchor")
    require(
        anchor,
        "ResolveMatchingReEntryLifecycle(pair, source, reEntry)",
        "startTime = reEntry.StartCandleTime;",
        "confirmationTime = reEntry.ConfirmationCandle;",
        "for(int shift = confirmationShift; shift <= startShift; shift++)",
        "iLow(pair, source.Timeframe, shift)",
        "iHigh(pair, source.Timeframe, shift)",
        "IsCandleClosed(barTime, tfSeconds)",
    )
    destination = function_body("ResolveApprovedBBDestination")
    require(
        destination,
        "ResolveClosedSourceShift(pair, source)",
        "iBands(pair, source.Timeframe",
        "MODE_UPPER",
        "MODE_LOWER",
    )

    initial = function_body("ResolveApprovedInitialSLTP")
    require(
        initial,
        "IsApprovedSLTPSourceComponent",
        "ResolveSourceOwnedStructuralAnchor",
        "ResolveApprovedBBDestination",
        "decision.SLTPSourceComponent",
        "double safetyBuffer = snapshot.Point;",
    )
    for name, body in (
        ("semantic resolver", resolver),
        ("approved-source validator", approved),
        ("source-owned anchor", anchor),
        ("BB destination", destination),
        ("initial SL/TP", initial),
    ):
        for forbidden in (
            "iATR",
            "ATR(",
            "Volatility",
            "FixedStop",
            "RiskReward",
            "Random",
        ):
            if forbidden in body:
                raise AssertionError(f"non-BBMA geometry in {name}: {forbidden}")

    require(
        SRC,
        '#property version   "4.71"',
        "Version 4.7.1 - D1TPW Restart-Safe Checkpoint Hardening",
    )
    for gate in ("EnableD1TPWLifecycle", "EnableC044Lifecycle"):
        if not re.search(rf"\bbool\s+{gate}\s*=\s*false\s*;", SRC):
            raise AssertionError(f"disabled lifecycle gate changed: {gate}")
    for forbidden in (
        "EnableP9SLSourceOverride",
        "P9AlternativeSLSource",
        "REJ_P9_SL_SOURCE",
        "NMJESLSourceScore",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P9 activation marker present: {forbidden}")

    print("NMJE_V2_M5_STAGE_E5_P9_SLTP_SEMANTIC_SOURCE_STATIC=PASS")


if __name__ == "__main__":
    main()

