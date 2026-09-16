from pathlib import Path

SRC_PATH = Path(__file__).resolve().parents[1] / "source" / "BBMA_EA.mq4"
SRC = SRC_PATH.read_text(encoding="utf-8")


def function_body(name: str) -> str:
    marker = name + "("
    start = SRC.index(marker)
    brace = SRC.index("{", start)
    depth = 0
    for idx in range(brace, len(SRC)):
        ch = SRC[idx]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace : idx + 1]
    raise AssertionError(f"unterminated function {name}")


def test_extreme_component_validity_has_no_fixed_age_authority():
    assert "IsExtremeStateExpired(" not in SRC
    update = function_body("UpdatePersistentExtremeState")
    validate = function_body("IsPersistentExtremeComponentValid")
    assert "MaxWaitBars_Extreme" not in update
    assert "MaxWaitBars_Extreme" not in validate


def test_specific_reentry_has_no_fixed_age_lifetime():
    start = function_body("StartSpecificReEntryCandidate")
    update = function_body("UpdateReEntryState")
    assert "MaxWaitBars_ReEntry" not in start
    assert "ExpiryBar = 0" in start
    assert "ExpiryCandleTime = 0" in start
    assert "IsReEntryIntrinsicExpired" not in update
    assert '"MaxWaitBars_ReEntry expired"' not in update


def test_reentry_downstream_authority_ignores_expiry_metadata():
    for name in (
        "BuildConfirmedReEntryCandidate",
        "IsFreshOpportunityReEntry",
        "IsPersistentReEntryComponentValid",
    ):
        assert "ExpiryCandleTime" not in function_body(name), name
    opportunity = function_body("BuildD1OpportunityCandidate")
    assert "MinPositiveExpiry" not in opportunity
    assert "candidate.Expiry = 0" in opportunity


def test_specific_reentry_retains_structural_invalidation():
    update = function_body("UpdateReEntryState")
    assert "oppositeSignal != SIGNAL_NONE" in update
    assert "reEntry.State == RE_STATE_CANDIDATE" in update
    assert "reEntry.State == RE_STATE_CONFIRMED" in update
    assert "IsReEntryMAClusterCloseSideFailure" in update


def test_build_identity_is_unique_v486():
    assert '//| Version 4.8.6 - Structural Lifetime Authority Repair' in SRC
    assert '#property version   "4.86"' in SRC
