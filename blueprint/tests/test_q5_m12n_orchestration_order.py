from pathlib import Path
import re

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

def test_m12n_repair_survives_later_build_identity():
    match = re.search(r'#property\s+version\s+"([0-9.]+)"', SRC)
    assert match
    version = match.group(1)
    assert float(version) >= 4.85
    assert f'[F7-BUILD] EA=BBMA_EA Build={version} BuildTag=' in SRC
    assert '#define BBMA_BUILD_TAG' in SRC
    assert '#define BBMA_SOURCE_REV_TAG' in SRC
