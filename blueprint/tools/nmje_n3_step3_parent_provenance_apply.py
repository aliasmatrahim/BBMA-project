#!/usr/bin/env python3
"""Add read-only canonical parent-event provenance to NMJE N1/N2 diagnostics.

This does not change relationship resolution, candidate eligibility, M15/M16, or
execution. It only carries the canonical event identity selected as N1 parent.
"""
from pathlib import Path
import sys

TARGET = Path('blueprint/source/BBMA_EA.mq4')


def once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f'expected one match, got {n}: {old[:100]!r}')
    return text.replace(old, new, 1)


def main():
    if not TARGET.exists():
        print('ERROR: source missing', file=sys.stderr); return 2
    src = TARGET.read_text(encoding='utf-8')
    if 'string                  ParentEventID;' in src:
        print('PASS: parent provenance already materialized'); return 0
    try:
        src = once(src,
'''   datetime                ParentCandleTime;
   ENUM_DIRECTION          StrategicDirection;''',
'''   datetime                ParentCandleTime;
   // N3 provenance-only identity of the exact canonical owner chosen as parent.
   string                  ParentEventID;
   ENUM_DIRECTION          StrategicDirection;''')

        src = once(src,
'''                        ENUM_DIRECTION &direction,
                        datetime &anchor,
                        string &reason)''',
'''                        ENUM_DIRECTION &direction,
                        datetime &anchor,
                        string &eventID,
                        string &reason)''')
        src = once(src,
'''   direction = DIR_NONE;
   anchor = 0;
   reason = "NO_PARENT";''',
'''   direction = DIR_NONE;
   anchor = 0;
   eventID = "";
   reason = "NO_PARENT";''')

        src = once(src,
'''      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      reason = "H4_RE_PARENT";''',
'''      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      eventID = NMJE_ReEntryEventID(state.actual_symbol, selected);
      reason = "H4_RE_PARENT";''')
        src = once(src,
'''      direction = state.h4_direction_owner.Direction;
      anchor = state.h4_direction_owner.SourceCandleTime;
      reason = "H4_OWNER_PARENT";''',
'''      direction = state.h4_direction_owner.Direction;
      anchor = state.h4_direction_owner.SourceCandleTime;
      eventID = NMJE_H4OwnerEventID(state.actual_symbol, state.h4_direction_owner);
      reason = "H4_OWNER_PARENT";''')
        src = once(src,
'''      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      reason = "D1_RE_PARENT";''',
'''      direction = selected.Direction;
      anchor = selected.ConfirmationCandle;
      eventID = NMJE_ReEntryEventID(state.actual_symbol, selected);
      reason = "D1_RE_PARENT";''')
        src = once(src,
'''      direction = state.d1_major_trend_owner.Direction;
      anchor = state.d1_major_trend_owner.SourceCandleTime;
      reason = "D1_OWNER_PARENT";''',
'''      direction = state.d1_major_trend_owner.Direction;
      anchor = state.d1_major_trend_owner.SourceCandleTime;
      eventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      reason = "D1_OWNER_PARENT";''')

        src = once(src,
'''   datetime parentAnchor = 0;
   string parentReason = "";
   bool hasParent = NMJE_ResolveParent(g_pair_states[pairIndex], parentKind, parentTF,
                                       parentSignal, parentDirection, parentAnchor,
                                       parentReason);''',
'''   datetime parentAnchor = 0;
   string parentEventID = "";
   string parentReason = "";
   bool hasParent = NMJE_ResolveParent(g_pair_states[pairIndex], parentKind, parentTF,
                                       parentSignal, parentDirection, parentAnchor,
                                       parentEventID, parentReason);''')

        # Freeze read-only parent provenance wherever the successful parent is frozen.
        src = once(src,
'''   journey.ParentSignal = parentSignal;
   journey.ParentDirection = parentDirection;
   journey.ParentCandleTime = parentAnchor;''',
'''   journey.ParentSignal = parentSignal;
   journey.ParentDirection = parentDirection;
   journey.ParentCandleTime = parentAnchor;
   journey.ParentEventID = parentEventID;''')

        # Main N1 diagnostic: PE is provenance only.
        src = once(src,
'''         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " J=", journey.JourneyID,''',
'''         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " PE=", (journey.ParentEventID == "" ? "-" : journey.ParentEventID),
         " J=", journey.JourneyID,''')

        # N2 decision shadow carries the exact observed parent provenance too.
        src = once(src,
'''         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " J=", journeyId,
         " DID=", decisionToken,''',
'''         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " PE=", (journey.ParentEventID == "" ? "-" : journey.ParentEventID),
         " J=", journeyId,
         " DID=", decisionToken,''')
    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr); return 3

    if 'ParentEventID' not in src or 'parentEventID, parentReason' not in src:
        print('ERROR: provenance materialization incomplete', file=sys.stderr); return 4
    TARGET.write_text(src, encoding='utf-8')
    print('PASS: N3 Step-3 parent provenance materialized')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
