#!/usr/bin/env python3
"""Bind C1-B price fixtures to exact build-4.71 MQL4 predicate surfaces."""
from pathlib import Path
from hashlib import sha256
import re


SOURCE_PATH = Path("blueprint/source/BBMA_EA.mq4")
SRC = SOURCE_PATH.read_text(encoding="utf-8")
EXPECTED_SOURCE_SHA256 = "c6a87f613495547ee3cf52a8fe041ae6f9a63396075c0c755a7475b9f488a7bb"


def function_body(name: str) -> str:
    declaration = re.search(
        rf"(?m)^[A-Za-z_][^\r\n]*\b{re.escape(name)}\s*\(", SRC
    )
    if declaration is None:
        raise AssertionError(f"missing function: {name}")
    brace = SRC.find("{", declaration.start())
    depth = 0
    for index in range(brace, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:index + 1]
    raise AssertionError(f"unterminated function: {name}")


def require(name: str, *markers: str) -> None:
    body = function_body(name)
    for marker in markers:
        if marker not in body:
            raise AssertionError(f"{name} missing price predicate: {marker}")


def main() -> None:
    digest = sha256(SOURCE_PATH.read_bytes()).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise AssertionError(f"EA source drift: {digest}")

    require(
        "DetectExtreme",
        "ma5High > band.TOP_BB || ma10High > band.TOP_BB",
        "ma5Low < band.LOW_BB || ma10Low < band.LOW_BB",
    )
    require(
        "IsExtremeReversalDirection",
        "data.close < data.open",
        "data.close > data.open",
    )
    require(
        "CandleBodyCrossesLevel",
        "open <= level && close > level",
        "open >= level && close < level",
    )
    require(
        "DetectCSM",
        "currentBand.Width > previousBand.Width",
        "currentBand.MID_BB > previousBand.MID_BB",
        "currentBand.TOP_BB > previousBand.TOP_BB",
        "close > currentBand.TOP_BB",
        "currentBand.MID_BB < previousBand.MID_BB",
        "currentBand.LOW_BB < previousBand.LOW_BB",
        "close < currentBand.LOW_BB",
    )
    require("DetectCSD", "ma.MA5_High", "ma.MA10_High", "band.MID_BB", "ma.MA5_Low", "ma.MA10_Low")
    require("DetectECSD", "ma.MA5_High", "ma.MA10_High", "ma.MA5_Low", "ma.MA10_Low")
    require(
        "HasReEntryMAClusterTouch",
        "data.low <= MathMax(ma5, ma10)",
        "data.close >= ma5 && data.close >= ma10",
        "data.high >= MathMin(ma5, ma10)",
        "data.close <= ma5 && data.close <= ma10",
    )
    require(
        "HasReEntryMA5OrMA50Touch",
        "data.low <= ma5 && data.close >= ma5",
        "data.low <= data.ma[4] && data.close >= data.ma[4]",
        "data.high >= ma5 && data.close <= ma5",
        "data.high >= data.ma[4] && data.close <= data.ma[4]",
    )
    require(
        "IsType1MAClusterCloseSideFailure",
        "data.close < MathMin(ma5, ma10)",
        "data.close > MathMax(ma5, ma10)",
    )
    require(
        "IsType1StructuralRetraceEvidence",
        "HasReEntryMAClusterTouch(data, direction)",
        "data.close < reEntry.Type1PreviousClose",
        "data.close > reEntry.Type1PreviousClose",
    )
    require(
        "IsExtremeRetestStart",
        "data.close > extreme.PreviousClose",
        "data.close < extreme.PreviousClose",
    )
    require(
        "IsExtremeRetestInteraction",
        "data.high >= extreme.FrozenBodyAnchor",
        "data.low <= extreme.FrozenBodyAnchor",
        "data.low <= ma5 && data.high >= ma5",
    )
    require(
        "IsMHVTPWajibCompleted",
        "data.low <= ma5Low || data.low <= ma10Low",
        "data.high >= ma5High || data.high >= ma10High",
    )
    require(
        "IsMHVLossPhaseEligible",
        "data.close < band.LOW_BB || data.close > band.TOP_BB",
        "DetectCSM(pair, data.timeframe, priorMoveDirection, data.barIndex)",
    )
    require(
        "IsMHVFormationMoveAway",
        "data.close > mlv.PreviousClose",
        "data.close < mlv.PreviousClose",
    )
    require(
        "IsMHVRetestInteraction",
        "data.low <= mlv.FrozenMarkedBody",
        "data.high >= mlv.FrozenMarkedBody",
    )

    print("BBMA_CORE_CANDLE_PRICE_SOURCE_STATIC=PASS")


if __name__ == "__main__":
    main()

