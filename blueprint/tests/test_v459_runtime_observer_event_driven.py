#!/usr/bin/env python3
from pathlib import Path

SRC = Path('blueprint/runtime/V459_Runtime_Observer.mq4')


def main() -> int:
    text = SRC.read_text(encoding='utf-8')

    required = [
        '#property version   "1.10"',
        'input int ObserverDebugLevel = 0;',
        'input bool EmitInitialHistoryDetails = false;',
        'string g_last_environment = "";',
        'string g_last_gv_records[];',
        'string g_last_open_records[];',
        'string g_last_history_records[];',
        'string g_last_printed_record = "";',
        'if(record == g_last_printed_record) return;',
        'bool RecordsEqual(string &left[], string &right[])',
        'void EmitNewOrChangedRecords(',
        'bool PollObservableState()',
        'bool verbose = (ObserverDebugLevel > 0);',
        'bool gvChanged = !RecordsEqual(gvRecords, g_last_gv_records);',
        'bool openChanged = !RecordsEqual(openRecords, g_last_open_records);',
        'bool historyChanged = !RecordsEqual(historyRecords, g_last_history_records);',
        'TaggedRecord("OPEN_CHANGE"',
        'TaggedRecord("HIST_CHANGE"',
        'TaggedRecord("BASELINE_END"',
        'TaggedRecord("CHANGE_END"',
        'TaggedRecord("POLL_END"',
        'PollObservableState();',
        '// Event-only mode is silent when environment/GV/open/history state is unchanged.',
        '// Intentionally empty. Observation is timer-polled but event-emitted.',
    ]
    for token in required:
        assert token in text, f'missing OBS-FIX-01 token: {token}'

    forbidden = [
        'void EmitSnapshot()',
        'PrintEnvironment(now);',
        'PrintGlobals(now);',
        'PrintOpenOrders(now);',
        'PrintRecentHistory(now);',
        '[V459-OBS][SNAP_END]',
        'OrderSend(',
        'OrderClose(',
        'OrderModify(',
        'OrderDelete(',
    ]
    for token in forbidden:
        assert token not in text, f'forbidden observer token present: {token}'

    # Timer polling is allowed, but direct tick-driven logging is not.
    tick = text[text.index('void OnTick()'):]
    assert 'Print(' not in tick
    assert 'EmitLine(' not in tick
    assert 'PollObservableState();' not in tick

    # Event-only is the default. Verbose behaviour must be explicit.
    assert 'ObserverDebugLevel = 0' in text
    assert 'else if(verbose)' in text

    # Baseline history detail is opt-in; normal startup must not replay seven
    # days of history records by default.
    assert 'if(verbose || (g_first_poll && EmitInitialHistoryDetails))' in text

    print('V459_OBSERVER_EVENT_DRIVEN_STATIC_GUARD=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
