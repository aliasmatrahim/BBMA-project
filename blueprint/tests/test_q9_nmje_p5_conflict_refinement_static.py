#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace + 1:i]
    raise AssertionError(signature)

def main() -> None:
    assert "V495_Q9_P11_LINEAGE_REFINEMENT_20260920" in SRC
    assert '#property version   "4.95"' in SRC
    build = body("void NMJE_BuildM5Refinement(")
    assert 'snapshot.Relation = NESTED_UNRESOLVED;\n         snapshot.Reason = "M5_OPPOSITE_CONFIRMED_RE_UNRESOLVED";' in build
    assert 'snapshot.Relation = NESTED_BUILDING;\n         snapshot.Reason = "M5_OPPOSITE_EXTREME_BUILDING";' in build
    assert "M5_TEMPORARY_CONFIRMED_RE_OPPOSES_PARENT" not in build
    assert "M5_TEMPORARY_EXTREME_OPPOSES_PARENT" not in build
    assert "snapshot.Relation = NESTED_CONFLICT;" not in build
    comparator = body("int CompareCanonicalCandidates(")
    priority = body("void PriorityEngine_Atomic(")
    invalidation = body("void InvalidationEngine_Atomic(")
    for segment in (comparator, priority, invalidation):
        for marker in ("M5_OPPOSITE_CONFIRMED_RE_UNRESOLVED", "M5_OPPOSITE_EXTREME_BUILDING"):
            assert marker not in segment
    for marker in ("NMJE_PassExecutionGate", "REJ_NMJE_RELATION", "REJ_NMJE_M5", "M5_EXECUTION_AUTHORITY"):
        assert marker not in SRC
    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_NMJE_P5_CONFLICT_REFINEMENT_STATIC=PASS")

if __name__ == "__main__":
    main()
