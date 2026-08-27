#!/usr/bin/env python3
"""Materialize read-only canonical event identities for NMJE diagnostics.

No BBMA strategy condition is changed. IDs are deterministic hashes derived only
from existing canonical owner provenance fields. Underlying provenance remains
authoritative; the hash is diagnostic/lineage metadata only.
"""
from pathlib import Path
import sys

TARGET = Path('blueprint/source/BBMA_EA.mq4')


def once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'expected exactly one match, got {count}: {old[:100]!r}')
    return text.replace(old, new, 1)


def main() -> int:
    if not TARGET.exists():
        print(f'ERROR target missing: {TARGET}', file=sys.stderr)
        return 2
    src = TARGET.read_text(encoding='utf-8')
    if 'string               CanonicalEventID;' in src:
        print('PASS: canonical event identity already materialized')
        return 0

    try:
        src = once(src,
'''   bool                 Resolved;
   string               Label;

   // N1.1 coverage-only secondary overlays.''',
'''   bool                 Resolved;
   string               Label;
   // N3 provenance-only deterministic identity. Never strategy authority.
   string               CanonicalEventID;

   // N1.1 coverage-only secondary overlays.''')

        helper_anchor = '''string NMJE_MLVStateText(ENUM_MLV_STATE state)
{
   if(state == MLV_PARENT_READY) return "P";
   if(state == MLV_TP_COMPLETE) return "TP";
   if(state == MLV_LOSS_DEVELOPING) return "L";
   if(state == MLV_FORMATION_ESTABLISHED) return "F";
   if(state == MLV_RETEST_COMPLETE) return "RT";
   if(state == MLV_DIRECTION_TAKEN) return "T";
   if(state == MLV_VOID) return "V";
   if(state == MLV_SUPERSEDED) return "S";
   return "N";
}

'''
        helpers = helper_anchor + '''// N3 Step-2: deterministic provenance identities. These helpers consume
// canonical owner facts only; they do not detect, score, mature or gate signals.
string NMJE_IdentityHash(string raw)
{
   if(raw == "") return "";
   return SHORT_HASH(raw, 16);
}

string NMJE_ReEntryEventID(string pair, ReEntryData &state)
{
   if(pair == "" || state.Timeframe <= 0 || state.StartCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL) ||
      state.Type == RE_NONE)
      return "";
   string raw = "RE|" + pair + "|" + IntegerToString(state.Timeframe) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.Type) + "|" +
                IntegerToString((int)state.StartCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_ExtremeEventID(string pair, ExtremeLifecycleData &state)
{
   if(pair == "" || state.Timeframe <= 0 || state.RawCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL))
      return "";
   string raw = "EXT|" + pair + "|" + IntegerToString(state.Timeframe) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.RawCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_MLVEventID(string pair, MLVData &state)
{
   if(pair == "" || state.Timeframe != PERIOD_M15 ||
      state.ParentRawCandleTime <= 0 || state.ParentConfirmationCandleTime <= 0 ||
      (state.Direction != DIR_BUY && state.Direction != DIR_SELL))
      return "";
   string raw = "MLV|" + pair + "|" + IntegerToString(PERIOD_M15) + "|" +
                IntegerToString((int)state.Direction) + "|" +
                IntegerToString((int)state.ParentRawCandleTime) + "|" +
                IntegerToString((int)state.ParentConfirmationCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_D1OwnerEventID(string pair, D1MajorTrendOwner &owner)
{
   if(pair == "" || owner.SourceCandleTime <= 0) return "";
   string raw = "D1OWN|" + pair + "|" + IntegerToString((int)owner.State) + "|" +
                IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.SourceCandleTime);
   return NMJE_IdentityHash(raw);
}

string NMJE_H4OwnerEventID(string pair, H4DirectionalOwner &owner)
{
   if(pair == "" || owner.SourceCandleTime <= 0 ||
      owner.State != H4_OWNER_ACTIVE ||
      (owner.Direction != DIR_BUY && owner.Direction != DIR_SELL) ||
      owner.SourceSignal == SIGNAL_NONE)
      return "";
   string raw = "H4OWN|" + pair + "|" + IntegerToString((int)owner.Direction) + "|" +
                IntegerToString((int)owner.SourceSignal) + "|" +
                IntegerToString((int)owner.SourceCandleTime);
   return NMJE_IdentityHash(raw);
}

'''
        src = once(src, helper_anchor, helpers)

        src = once(src,
'''   node.Resolved = false;
   node.Label = "-";
}''',
'''   node.Resolved = false;
   node.Label = "-";
   node.CanonicalEventID = "";
}''')

        src = src.replace('void NMJE_SetRENode(NestedTFNode &node, ReEntryData &state, bool resolved)',
                          'void NMJE_SetRENode(string pair, NestedTFNode &node, ReEntryData &state, bool resolved)')
        src = once(src,
'''   node.Resolved = resolved;
   node.Label = "RE:" + NMJE_REStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}''',
'''   node.Resolved = resolved;
   node.CanonicalEventID = NMJE_ReEntryEventID(pair, state);
   node.Label = "RE:" + NMJE_REStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}''')

        src = src.replace('void NMJE_SetExtremeNode(NestedTFNode &node, ExtremeLifecycleData &state)',
                          'void NMJE_SetExtremeNode(string pair, NestedTFNode &node, ExtremeLifecycleData &state)')
        src = once(src,
'''   node.Resolved = false; // Extreme is pre-direction context for N1 lineage.
   node.Label = "EXT:" + NMJE_ExtremeStateText(state.Maturity) + "/" + NMJE_DirText(state.Direction);
}''',
'''   node.Resolved = false; // Extreme is pre-direction context for N1 lineage.
   node.CanonicalEventID = NMJE_ExtremeEventID(pair, state);
   node.Label = "EXT:" + NMJE_ExtremeStateText(state.Maturity) + "/" + NMJE_DirText(state.Direction);
}''')

        src = src.replace('void NMJE_SetMLVNode(NestedTFNode &node, MLVData &state)',
                          'void NMJE_SetMLVNode(string pair, NestedTFNode &node, MLVData &state)')
        src = once(src,
'''   node.Resolved = false; // MHV/MLV is setup/context, not final direction authority.
   node.Label = "MHV:" + NMJE_MLVStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}''',
'''   node.Resolved = false; // MHV/MLV is setup/context, not final direction authority.
   node.CanonicalEventID = NMJE_MLVEventID(pair, state);
   node.Label = "MHV:" + NMJE_MLVStateText(state.State) + "/" + NMJE_DirText(state.Direction);
}''')

        # All node-builder call sites consume PairState.actual_symbol.
        src = src.replace('NMJE_SetRENode(node, selected, true);',
                          'NMJE_SetRENode(state.actual_symbol, node, selected, true);')
        src = src.replace('NMJE_SetRENode(node, selected, false);',
                          'NMJE_SetRENode(state.actual_symbol, node, selected, false);')
        src = src.replace('NMJE_SetExtremeNode(node, state.',
                          'NMJE_SetExtremeNode(state.actual_symbol, node, state.')
        src = src.replace('NMJE_SetMLVNode(node, state.',
                          'NMJE_SetMLVNode(state.actual_symbol, node, state.')

        # D1/H4 owner nodes get deterministic owner identities at owner selection.
        src = src.replace(
'''      node.Resolved = true;
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   if(state.d1_major_trend_owner.State == D1_TRANSITION)''',
'''      node.Resolved = true;
      node.CanonicalEventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }

   if(state.d1_major_trend_owner.State == D1_TRANSITION)''', 1)

        src = once(src,
'''   if(state.d1_major_trend_owner.State == D1_TRANSITION)
   {
      node.Valid = true;
      node.Resolved = true;
      node.Label = "TRANSITION";
      return;
   }''',
'''   if(state.d1_major_trend_owner.State == D1_TRANSITION)
   {
      node.Valid = true;
      node.Resolved = true;
      node.CanonicalEventID = NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner);
      node.Label = "TRANSITION";
      return;
   }''')

        h4_owner_old = '''      node.CandleTime = state.h4_direction_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }'''
        h4_owner_new = '''      node.CandleTime = state.h4_direction_owner.SourceCandleTime;
      node.Valid = true;
      node.Resolved = true;
      node.CanonicalEventID = NMJE_H4OwnerEventID(state.actual_symbol, state.h4_direction_owner);
      node.Label = "OWN/" + NMJE_DirText(node.Direction);
      return;
   }'''
        src = once(src, h4_owner_old, h4_owner_new)

        # Diagnostic exposure: compact IDs only; labels and relationship semantics unchanged.
        src = once(src,
'''         " D1=", journey.D1Node.Label,
         " H4=", journey.H4Node.Label,
         " H1=", journey.H1Node.Label,
         " M15=", journey.M15Node.Label,
         " R=", journey.Reason);''',
'''         " D1=", journey.D1Node.Label, "#", (journey.D1Node.CanonicalEventID == "" ? "-" : journey.D1Node.CanonicalEventID),
         " H4=", journey.H4Node.Label, "#", (journey.H4Node.CanonicalEventID == "" ? "-" : journey.H4Node.CanonicalEventID),
         " H1=", journey.H1Node.Label, "#", (journey.H1Node.CanonicalEventID == "" ? "-" : journey.H1Node.CanonicalEventID),
         " M15=", journey.M15Node.Label, "#", (journey.M15Node.CanonicalEventID == "" ? "-" : journey.M15Node.CanonicalEventID),
         " R=", journey.Reason);''')

    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 3

    required = [
        'CanonicalEventID', 'NMJE_ReEntryEventID(', 'NMJE_ExtremeEventID(',
        'NMJE_MLVEventID(', 'NMJE_D1OwnerEventID(', 'NMJE_H4OwnerEventID('
    ]
    for token in required:
        if token not in src:
            print(f'ERROR required token missing after apply: {token}', file=sys.stderr)
            return 4
    TARGET.write_text(src, encoding='utf-8')
    print('PASS: N3 Step-2 deterministic canonical event identities materialized')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
