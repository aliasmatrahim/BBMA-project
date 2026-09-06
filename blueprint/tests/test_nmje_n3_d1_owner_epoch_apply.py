#!/usr/bin/env python3
"""Synthetic fail-closed selftest for the N3 D1 owner epoch materializer."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util


def load_module():
    path = Path('blueprint/tools/nmje_n3_step5_d1_owner_epoch_apply.py')
    spec = importlib.util.spec_from_file_location('nmje_n3_step5_d1_owner_epoch_apply', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

    fixture = r'''UNRELATED_PREFIX
struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   datetime             LastProcessedD1CandleTime;
};

void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;
   owner.Reason = reason;
   state.d1_major_trend_owner = owner;
}

void UpdateD1OwnerFixture(PairState &state)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;

   if(state.d1_data.close > state.d1_data.ma.EMA50)
   {
      owner.State = D1_OWNER_BUY_CONFIRMED;
      owner.Direction = DIR_BUY;
   }
   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   state.d1_major_trend_owner = owner;
}

string NMJE_D1OwnerEventID(string pair, D1MajorTrendOwner &owner)
{
   if(pair == "" || owner.SourceCandleTime <= 0) return "";
   string raw = "D1OWN|" + pair + "|" + IntegerToString((int)owner.State) + "|" +
                IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.SourceCandleTime);
   return NMJE_IdentityHash(raw);
}
UNRELATED_SUFFIX
'''

    with TemporaryDirectory() as td:
        target = Path(td) / 'BBMA_EA.mq4'
        target.write_text(fixture, encoding='utf-8')
        module.TARGET = target
        rc = module.main()
        assert rc == 0, rc
        out = target.read_text(encoding='utf-8')

    assert 'UNRELATED_PREFIX' in out
    assert 'UNRELATED_SUFFIX' in out
    assert 'datetime             SourceCandleTime;' in out
    assert 'datetime             EpochStartCandleTime;' in out
    assert 'datetime previousEpoch = owner.EpochStartCandleTime;' in out
    assert 'previousState != D1_OWNER_UNRESOLVED' in out
    assert 'owner.State != previousState' in out
    assert 'owner.Direction != previousDirection' in out
    assert 'owner.EpochStartCandleTime = owner.SourceCandleTime;' in out
    assert 'owner.EpochStartCandleTime = previousEpoch;' in out

    start = out.index('string NMJE_D1OwnerEventID(')
    end = out.index('\n}', start) + 2
    event_block = out[start:end]
    assert 'EpochStartCandleTime' in event_block
    assert 'SourceCandleTime' not in event_block

    # The helper must remain provenance-only and not introduce execution gates.
    for marker in (
        'EnableNMJEExecutionGate',
        'EnableNestedExecutionGate',
        'N3_EXECUTION_POLICY',
        'N3_POLICY_ACTIVE',
        'OrderSend(',
        'OrderClose(',
        'OrderModify(',
        'OrderDelete(',
    ):
        assert marker not in out, marker

    print('NMJE_N3_D1_OWNER_EPOCH_APPLY_SELFTEST=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
