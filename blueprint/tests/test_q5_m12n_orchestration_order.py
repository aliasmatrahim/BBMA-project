from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def function_body(name: str) -> str:
    marker = f"void {name}("
    start = SRC.index(marker)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:i + 1]
    raise AssertionError(f"unterminated function {name}")


def test_m12n_runs_once_after_owner_updates_before_combination_assembly():
    body = function_body("ProcessPair")
    assert body.count("UpdateNestedJourneyObservation(pairIndex);") == 1
    nmje = body.index("UpdateNestedJourneyObservation(pairIndex);")
    assert nmje > body.rindex("UpdateReEntryState(", 0, nmje)
    assert nmje > body.rindex("UpdateCanonicalMLVState(", 0, nmje)
    assert nmje < body.index("BuildPossibleCombinations(")
    assert nmje < body.index("BuildConfirmedReEntryCandidate(")
    assert nmje < body.index("ValidateSequence(")

def test_integrated_build_identity_is_consistent_for_485():
    assert "Version 4.85 - M12N Orchestration Order Repair" in SRC
    assert '#property version   "4.85"' in SRC
    assert '#define BBMA_BUILD_TAG      "V485_M12N_ORDER_20260917"' in SRC
    assert '#define BBMA_SOURCE_REV_TAG "Q5_M12N_ORDER_174_20260917"' in SRC
    assert '[F7-BUILD] EA=BBMA_EA Build=4.85 BuildTag=' in SRC
    assert 'BBMA EA V4.8.5 M12N Orchestration Order Repair initialized successfully' in SRC