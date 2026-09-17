from pathlib import Path

SRC = Path(__file__).parents[1] / "source" / "BBMA_EA.mq4"
TEXT = SRC.read_text(encoding="utf-8")


def section(start: str, end: str) -> str:
    a = TEXT.index(start)
    b = TEXT.index(end, a)
    return TEXT[a:b]


def test_f7_identity_and_startup_order():
    import re
    match = re.search(r'#property\s+version\s+"([0-9.]+)"', TEXT)
    assert match, "missing MQL4 version identity"
    version = match.group(1)
    assert '#define BBMA_BUILD_TAG' in TEXT
    assert '#define BBMA_SOURCE_REV_TAG' in TEXT
    assert f'[F7-BUILD] EA=BBMA_EA Build={version} BuildTag=' in TEXT
    oninit = section("int OnInit()", "void OnDeinit")
    assert oninit.count("F7BuildIdentityTelemetry();") == 1
    assert oninit.index("F7BuildIdentityTelemetry();") < oninit.index("InitializeEA()")


def test_exact_ticket_execution_telemetry_and_prospective_location():
    entry = section("void ProcessEntry(", "bool RunEntryPreflightAndExecute")
    assert entry.count('OrderOpen=", TimeToString(info.open_time)') == 2
    assert "OrderSelect(ticket, SELECT_BY_TICKET)" in entry
    assert "info.open_time = OrderOpenTime();" in entry
    assert "F7ProspectiveContextTelemetry(pairIdx, decision, ticket);" in entry
    pair = section("void ProcessPair(", "void OnTickMain")
    assert "F7ProspectiveContextTelemetry(pairIndex, decision);" not in pair


def test_c044_generation_writer_is_fail_stop_and_commit_last():
    replay = section("bool SaveC044ReplaySeed", "bool ReadC044ReplayGV")
    checkpoint = section("bool SaveC044Checkpoint", "bool LoadC044Checkpoint")
    assert "GlobalVariableSet(" not in replay
    assert "GlobalVariableSet(" not in checkpoint
    assert "C044ReplayPayloadAbsent(base)" in replay
    assert "C044SetGVExact(base + \"G\", generation)" in replay
    assert "C044DeleteGVExact(base + \"CM\")" in checkpoint
    assert checkpoint.index("ClearC044GenerationPayloadExact(info)") < checkpoint.index("C044SetGVExact(base + \"GN\", generation)")
    assert checkpoint.index("C044SetGVExact(base + \"G\", generation)") < checkpoint.index("C044SetGVExact(base + \"CM\", generation)")


def test_c044_loader_rejects_uncommitted_or_legacy_generation():
    exists = section("bool C044CheckpointExists", "string C044ReplayGVBase")
    replay = section("bool LoadC044ReplaySeed", "void ClearC044Checkpoint")
    load = section("bool LoadC044Checkpoint", "string H4OwnerGVBase")
    assert 'base + "CM"' in exists and 'base + "G"' in exists
    assert '(int)GlobalVariableGet(base + "V") != 2' in replay
    assert 'GlobalVariableGet(base + "G") != expectedGeneration' in replay
    assert load.count('GlobalVariableGet(base + "CM") != committedGeneration') >= 2
    assert load.count('GlobalVariableGet(base + "G") != committedGeneration') >= 2
