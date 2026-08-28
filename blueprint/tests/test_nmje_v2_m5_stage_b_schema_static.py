#!/usr/bin/env python3
"""Static Stage-B P1 schema regression retained through later stages."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def function_body(name: str, return_type: str) -> str:
    match = re.search(
        rf"{return_type}\s+{re.escape(name)}\s*\([^)]*\)\s*\{{(.*?)\n\}}",
        SRC,
        re.S,
    )
    if not match:
        raise AssertionError(f"missing helper: {name}")
    return match.group(1)


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing marker: {marker}")


def main() -> None:
    require(
        SRC,
        "struct NMJEM5RefinementState",
        "string               EventID;",
        "string               ParentEventID;",
        "string               JourneyID;",
        "datetime             EventStartCandleTime;",
        "datetime             ClosedCandleTime;",
        "ENUM_NESTED_RELATION Relation;",
        "NMJEM5RefinementState    M5Refinement;",
    )

    identity = function_body("NMJE_M5ContextEventID", "string")
    require(
        identity,
        '"M5CTX|"',
        "IntegerToString(PERIOD_M5)",
        "direction",
        "contextCode",
        "eventStartCandleTime",
        "NMJE_IdentityHash(raw)",
    )
    for forbidden in (
        "TimeCurrent(",
        "TimeLocal(",
        "GetTickCount(",
        "MathRand(",
        "MarketInfo(",
        "iOpen(",
        "iClose(",
    ):
        if forbidden in identity:
            raise AssertionError(f"non-deterministic identity input: {forbidden}")

    validation = function_body("NMJE_M5LineageSnapshotValid", "bool")
    require(
        validation,
        "if(!snapshot.Present) return true;",
        "snapshot.EventID == \"\"",
        "snapshot.ParentEventID == \"\"",
        "snapshot.JourneyID == \"\"",
        "snapshot.ClosedCandleTime < snapshot.EventStartCandleTime",
        "NESTED_UNRESOLVED",
    )

    # Later stages may materialize the schema, but cannot weaken its identity
    # determinism or introduce any M5 authority marker.
    for forbidden in (
        "EnableNMJEM5Execution",
        "M5_PROCESSING_CLOCK",
        "M5_EXECUTION_AUTHORITY",
        "REJ_NMJE_M5",
    ):
        if forbidden in SRC:
            raise AssertionError(f"M5 authority leak: {forbidden}")

    print("NMJE_V2_M5_STAGE_B_SCHEMA_STATIC=PASS")


if __name__ == "__main__":
    main()

