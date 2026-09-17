from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "blueprint" / "source" / "BBMA_EA.mq4"


def function_body(text: str, signature: str) -> str:
    start = text.index(signature)
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1 : i]
    raise AssertionError(f"unterminated function: {signature}")


def test_nmje_cannot_reject_validated_entry():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    body = function_body(text, "bool RunEntryPreflightAndExecute")

    assert "NMJE_PassExecutionGate" not in body
    assert "REJ_NMJE_RELATION" not in body
    assert "[NMJE-GATE]" not in body


def test_nmje_gate_has_no_execution_blocking_logic_if_retained():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    signature = "bool NMJE_PassExecutionGate"
    if signature not in text:
        return

    body = function_body(text, signature)
    assert "BlockNMJEConflict" not in body
    assert "BlockNMJEBuilding" not in body
    assert "NESTED_CONFLICT" not in body
    assert "NESTED_BUILDING" not in body
    assert "return false" not in body


def test_nmje_observation_telemetry_is_preserved():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    assert "[N1-NMJE]" in text
    assert "[N2-NMJE-DEC]" in text
    assert "[N2-NMJE-OUT]" in text


def test_candidate_uses_unique_post_482_build_identity():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'#property\s+version\s+"([0-9.]+)"', text)
    assert match, "missing MQL4 version identity"
    assert match.group(1) == "4.83"

def test_integrated_f7_build_identity_matches_483():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    assert '#define BBMA_BUILD_TAG      "V483_NMJE_READONLY_20260917"' in text
    assert '#define BBMA_SOURCE_REV_TAG "NMJE_READONLY_Q1_20260917"' in text
    assert '[F7-BUILD] EA=BBMA_EA Build=4.83 BuildTag=' in text


def test_visible_runtime_identity_matches_483():
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    assert "V4.8.3 NMJE Read-Only Authority Restore initialized successfully" in text
    assert "V4.8.2 Post-Freeze F7 Infrastructure initialized successfully" not in text
