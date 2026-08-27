#!/usr/bin/env python3
"""Materialize stable D1 owner epoch provenance for NMJE.

Engineering-only provenance hardening. The D1 owner strategy formula is not
changed. SourceCandleTime remains the latest closed-D1 snapshot; a new
EpochStartCandleTime advances only when canonical owner State/Direction changes.
"""
from pathlib import Path
import sys

TARGET = Path('blueprint/source/BBMA_EA.mq4')


def once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'expected exactly one match, got {count}: {old[:120]!r}')
    return text.replace(old, new, 1)


def main() -> int:
    src = TARGET.read_text(encoding='utf-8')
    if 'datetime             EpochStartCandleTime;' in src:
        print('PASS: D1 owner epoch identity already materialized')
        return 0

    try:
        src = once(src,
'''struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   datetime             LastProcessedD1CandleTime;''',
'''struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   // N3 provenance-only epoch anchor. Changes only when canonical owner
   // State/Direction changes; never changes the D1 strategy formula.
   datetime             EpochStartCandleTime;
   datetime             LastProcessedD1CandleTime;''')

        src = once(src,
'''void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;''',
'''void SetD1OwnerUnresolved(PairState &state, string reason)
{
   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   ENUM_D1_OWNER_STATE previousState = owner.State;
   ENUM_DIRECTION previousDirection = owner.Direction;
   datetime previousEpoch = owner.EpochStartCandleTime;

   owner.State = D1_OWNER_UNRESOLVED;
   owner.Direction = DIR_NONE;
   owner.SourceCandleTime = state.d1_data.candle_time;
   if(previousEpoch <= 0 || previousState != D1_OWNER_UNRESOLVED ||
      previousDirection != DIR_NONE)
      owner.EpochStartCandleTime = owner.SourceCandleTime;
   else
      owner.EpochStartCandleTime = previousEpoch;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;''')

        src = once(src,
'''   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;''',
'''   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   ENUM_D1_OWNER_STATE previousState = owner.State;
   ENUM_DIRECTION previousDirection = owner.Direction;
   datetime previousEpoch = owner.EpochStartCandleTime;

   owner.SourceCandleTime = state.d1_data.candle_time;
   owner.LastProcessedD1CandleTime = state.d1_data.candle_time;''')

        src = once(src,
'''   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   state.d1_major_trend_owner = owner;''',
'''   else
   {
      owner.State = D1_TRANSITION;
      owner.Direction = DIR_NONE;
      owner.Reason =
         "Closed D1 price-side and MA50 slope do not confirm one direction";
   }

   // N3 owner epoch is provenance only: same canonical State/Direction keeps
   // the prior epoch while a transition starts a new deterministic epoch.
   if(previousEpoch <= 0 || owner.State != previousState ||
      owner.Direction != previousDirection)
      owner.EpochStartCandleTime = owner.SourceCandleTime;
   else
      owner.EpochStartCandleTime = previousEpoch;

   state.d1_major_trend_owner = owner;''')

        src = once(src,
'''string NMJE_D1OwnerEventID(string pair, D1MajorTrendOwner &owner)
{
   if(pair == "" || owner.SourceCandleTime <= 0) return "";
   string raw = "D1OWN|" + pair + "|" + IntegerToString((int)owner.State) + "|" +
                IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.SourceCandleTime);
   return NMJE_IdentityHash(raw);
}''',
'''string NMJE_D1OwnerEventID(string pair, D1MajorTrendOwner &owner)
{
   if(pair == "" || owner.EpochStartCandleTime <= 0) return "";
   string raw = "D1OWN|" + pair + "|" + IntegerToString((int)owner.State) + "|" +
                IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.EpochStartCandleTime);
   return NMJE_IdentityHash(raw);
}''')

    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 3

    required = [
        'EpochStartCandleTime',
        'previousEpoch',
        'owner.State != previousState',
        'owner.Direction != previousDirection',
        'IntegerToString((int)owner.EpochStartCandleTime)',
    ]
    for token in required:
        if token not in src:
            print(f'ERROR required token missing: {token}', file=sys.stderr)
            return 4

    TARGET.write_text(src, encoding='utf-8')
    print('PASS: N3 Step-5 stable D1 owner epoch identity materialized')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
