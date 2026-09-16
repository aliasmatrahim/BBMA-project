from pathlib import Path

SRC_PATH = Path(__file__).resolve().parents[1] / "source" / "BBMA_EA.mq4"
SRC = SRC_PATH.read_text(encoding="utf-8")


def function_body(name: str) -> str:
    marker = name + "("
    start = SRC.index(marker)
    brace = SRC.index("{", start)
    depth = 0
    for idx in range(brace, len(SRC)):
        if SRC[idx] == "{":
            depth += 1
        elif SRC[idx] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace : idx + 1]
    raise AssertionError(f"unterminated function {name}")


def update_type_block(type_name: str, next_type: str | None) -> str:
    body = function_body("UpdateReEntryState")
    start = body.index(f"if(reEntry.Type == {type_name})")
    end = body.index(f"if(reEntry.Type == {next_type})", start) if next_type else len(body)
    return body[start:end]


def test_general_close_side_helper_exists_and_uses_full_cluster():
    assert "bool IsReEntryMAClusterCloseSideFailure" in SRC
    assert "bool IsType1MAClusterCloseSideFailure" not in SRC
    helper = function_body("IsReEntryMAClusterCloseSideFailure")
    assert "data.close < MathMin(ma5, ma10)" in helper
    assert "data.close > MathMax(ma5, ma10)" in helper


def test_type3_requires_ma5_or_ma50_touch_then_full_cluster_close_side():
    block = update_type_block("RE_TYPE_3_CSM", "RE_TYPE_4_CSD")
    touch = block.index("HasReEntryMA5OrMA50Touch(data, direction)")
    guard = block.index("IsReEntryMAClusterCloseSideFailure(data, direction)")
    confirm = block.index("ConfirmReEntryState(reEntry, data")
    assert touch < guard < confirm
    assert "return RE_STATE_CANDIDATE" in block[guard:confirm]


def test_type3_precursor_and_retrace_semantics_are_preserved():
    detect = function_body("DetectReEntry_Type3")
    assert "DetectCSM(pair, data.timeframe, direction, data.barIndex)" in detect
    block = update_type_block("RE_TYPE_3_CSM", "RE_TYPE_4_CSD")
    assert "HasReEntryMA5OrMA50Touch(data, direction)" in block


def test_type2_and_type4_confirmation_contracts_are_unchanged():
    type2 = update_type_block("RE_TYPE_2", "RE_TYPE_3_CSM")
    type4 = update_type_block("RE_TYPE_4_CSD", None)
    assert "HasReEntryMAClusterTouch(data, direction)" in type2
    assert "HasReEntryMAClusterTouch(data, direction)" in type4
    assert "IsReEntryMAClusterCloseSideFailure" not in type2
    assert "IsReEntryMAClusterCloseSideFailure" not in type4


def test_build_identity_is_unique_v487():
    assert "//| Version 4.8.7 - Type3 Re-Entry Close-Side Repair" in SRC
    assert '#property version   "4.87"' in SRC


def test_type1_structural_contract_survives_shared_helper_rename():
    body = function_body("UpdateReEntryState")
    assert "IsType1StructuralRetraceEvidence(reEntry, data, direction)" in body
    assert body.count("IsReEntryMAClusterCloseSideFailure(data, direction)") >= 4
    assert "HasReEntryMAClusterTouch(data, direction)" in body
