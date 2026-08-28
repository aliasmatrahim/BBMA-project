#!/usr/bin/env python3
"""Stage-A contract, baseline, and authority firewall for Issue #101."""
from pathlib import Path


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")
CONTRACT = Path(
    "blueprint/contracts/NMJE_V2_M5_ACCURACY_HARDENING_CONTRACT.md"
).read_text(encoding="utf-8")
PLAN = Path(
    "blueprint/implementation/NMJE_V2_M5_WORKSTREAM_PLAN_20260828.md"
).read_text(encoding="utf-8")


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing marker: {marker}")


def main() -> None:
    require(
        SRC,
        "Version 4.6.5 - NMJE v2 Conflict Subtype Telemetry",
        '#property version   "4.65"',
        "datetime             EpochStartCandleTime;",
        "NMJE_BuildD1Node(",
        "NMJE_BuildH4Node(",
        "NMJE_BuildH1Node(",
        "NMJE_BuildM15Node(",
        "MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)",
        "MODULE 16: CONFLICT & INVALIDATION ENGINE",
        "MODULE 22: ORDER EXECUTION ENGINE (DUMB EXECUTOR)",
    )

    require(
        CONTRACT,
        "D1 -> H4 -> H1 -> M15 -> M5",
        "M15: sole processing and final decision clock",
        "M5: closed-candle lower-TF confirmation/refinement context only",
        "execution_policy = NONE",
        "automatic_policy_authorized = false",
        "m5_execution_authority = false",
        "m5_processing_clock_authority = false",
        "source_modification_authorized = stage_e1_p5_conflict_metadata",
        "activation_authorized = false",
    )
    require(
        PLAN,
        "No source edit occurs in this preparation commit",
        "temporary M5 conflict cannot reject the sole valid M15 candidate",
        "native MT4 MetaEditor 0E0W",
    )

    # Stage C2 permits shadow materialization but no execution/rejection/clock
    # authority marker.
    for forbidden in (
        "NMJE_BuildM5Node(",
        "EnableNMJEM5Execution",
        "EnableNMJEExecutionGate",
        "EnableNestedExecutionGate",
        "M5_PROCESSING_CLOCK",
        "M5_EXECUTION_AUTHORITY",
        "REJ_NMJE_M5",
        "N3_POLICY_ACTIVE",
    ):
        if forbidden in SRC:
            raise AssertionError(f"Stage-A authority/source leak: {forbidden}")

    # Existing lifecycle switches must remain fail-safe off.
    require(
        SRC,
        "bool           EnableC044Lifecycle                = false;",
        "bool           EnableD1TPWLifecycle               = false;",
    )

    print("NMJE_V2_M5_STAGE_A_STATIC=PASS")


if __name__ == "__main__":
    main()

