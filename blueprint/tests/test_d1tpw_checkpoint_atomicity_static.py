#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def body(signature):
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:i + 1]
    raise AssertionError(signature)


def main():
    for marker in (
        "Version 4.8.7 - D1TPW Checkpoint Atomicity",
        '#property version   "4.87"',
        'V487_D1TPW_CHECKPOINT_ATOMICITY_20260920',
        'D1TPW_CHECKPOINT_ATOMICITY_210_20260920',
        "EnableD1TPWLifecycle               = false;",
    ):
        assert marker in SRC, marker

    set_exact = body("bool SetTerminalGlobalExact(")
    delete_exact = body("bool DeleteTerminalGlobalExact(")
    assert "GlobalVariableSet(key, value)" in set_exact
    assert "GlobalVariableGet(key) == value" in set_exact
    assert "GlobalVariableDel(key)" in delete_exact

    exists = body("bool D1TPWCheckpointExists(")
    payload = body("bool D1TPWGenerationPayloadExists(")
    assert 'base + "CM"' in exists
    assert "D1TPWGenerationPayloadExists(info, committed)" in exists
    assert 'base + "G"' in payload
    for key in ("D","X","LP","L","XL","F","OT","MG"):
        assert f'"{key}"' in payload

    save = body("bool SaveD1TPWCheckpoint(")
    required = [
        'DeleteTerminalGlobalExact(base + "CM")',
        'SetTerminalGlobalExact(base + "GN", generation)',
        'SetTerminalGlobalExact(base + "D", (double)info.direction)',
        'SetTerminalGlobalExact(base + "G", generation)',
        'D1TPWGenerationPayloadExists(info, generation)',
        'SetTerminalGlobalExact(base + "CM", generation)',
    ]
    for marker in required:
        assert marker in save, marker
    positions = [save.index(marker) for marker in required]
    assert positions == sorted(positions)
    assert "GlobalVariableSet(" not in save

    load = body("bool LoadD1TPWCheckpoint(")
    assert "double committedGeneration" in load
    assert load.count('GlobalVariableGet(base + "CM") != committedGeneration') >= 2
    assert load.count('GlobalVariableGet(base + "G") != committedGeneration') >= 2

    clear = body("void ClearD1TPWCheckpoint(")
    for key in ("G", "GN", "CM"):
        assert f'"{key}"' in clear
    assert "DeleteTerminalGlobalExact" in clear
    assert clear.index('DeleteTerminalGlobalExact(base + "CM")') < clear.index(
        'string keys[10]'
    )

    cdel = body("bool C044DeleteGVExact(")
    cset = body("bool C044SetGVExact(")
    assert "return DeleteTerminalGlobalExact(key);" in cdel
    assert "return SetTerminalGlobalExact(key, value);" in cset
    assert "GlobalVariableDel(" not in cdel
    assert "GlobalVariableSet(" not in cset

    # No authority expansion or accidental execution enablement.
    assert SRC.count("OrderSend(") == 1
    assert "EnableD1TPWLifecycle               = true;" not in SRC
    print("D1TPW_CHECKPOINT_ATOMICITY_STATIC=PASS")


if __name__ == "__main__":
    main()
