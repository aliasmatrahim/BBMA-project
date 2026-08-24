from pathlib import Path
import argparse

MARKER = '[D1-10][BOTTLENECK]'
FUNC_NAME = 'PrintSignalBottleneckDiagnostic'

FUNC = r'''void PrintSignalBottleneckDiagnostic(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   string finalCandidate = "NONE";
   if(decision.Valid)
   {
      finalCandidate = EnumToString(decision.SignalType) + "/" +
                       EnumToString(decision.Direction) + "/" +
                       EnumToString(decision.DecisionState);
      if(decision.RejectionReason != REJ_NONE)
         finalCandidate += "/" + EnumToString(decision.RejectionReason);
   }

   Print("[D1-10][BOTTLENECK] Pair=", g_pair_states[pairIndex].actual_symbol,
         " D1=", EnumToString(g_pair_states[pairIndex].d1_major_trend_owner.State),
         "/", EnumToString(g_pair_states[pairIndex].d1_major_trend_owner.Direction),
         " H4=", EnumToString(g_pair_states[pairIndex].h4_direction_owner.State),
         "/", EnumToString(g_pair_states[pairIndex].h4_direction_owner.Direction),
         " H1RE=B:", EnumToString(g_pair_states[pairIndex].re_h1_buy_state.State),
         ",S:", EnumToString(g_pair_states[pairIndex].re_h1_sell_state.State),
         " H4RE=B:", EnumToString(g_pair_states[pairIndex].re_h4_buy_state.State),
         ",S:", EnumToString(g_pair_states[pairIndex].re_h4_sell_state.State),
         " D1RE=B:", EnumToString(g_pair_states[pairIndex].re_d1_buy_state.State),
         ",S:", EnumToString(g_pair_states[pairIndex].re_d1_sell_state.State),
         " H1EXT=B:", EnumToString(g_pair_states[pairIndex].extreme_h1_buy_lifecycle.Maturity),
         ",S:", EnumToString(g_pair_states[pairIndex].extreme_h1_sell_lifecycle.Maturity),
         " H4EXT=B:", EnumToString(g_pair_states[pairIndex].extreme_h4_buy_lifecycle.Maturity),
         ",S:", EnumToString(g_pair_states[pairIndex].extreme_h4_sell_lifecycle.Maturity),
         " M15MHV=B:", EnumToString(g_pair_states[pairIndex].mlv_buy_state.State),
         ",S:", EnumToString(g_pair_states[pairIndex].mlv_sell_state.State),
         " Final=", finalCandidate);
}

'''

CALL = '''   PrintSignalBottleneckDiagnostic(pairIndex, decision);\n\n'''

INSERT_ANCHOR = 'void ProcessPair(int pairIndex)\n{'
CALL_ANCHOR = '   g_pair_states[pairIndex].last_decision = decision;'


def verify(text: str) -> None:
    if text.count(MARKER) != 1:
        raise SystemExit(f'expected exactly one diagnostic marker, found {text.count(MARKER)}')
    if text.count('void ' + FUNC_NAME + '(') != 1:
        raise SystemExit('diagnostic function missing or duplicated')
    if text.count(FUNC_NAME + '(pairIndex, decision);') != 1:
        raise SystemExit('diagnostic call missing or duplicated')
    if INSERT_ANCHOR not in text:
        raise SystemExit('ProcessPair anchor missing')
    if CALL_ANCHOR not in text:
        raise SystemExit('last_decision anchor missing')


def apply(text: str) -> str:
    if MARKER in text:
        verify(text)
        return text
    if text.count(INSERT_ANCHOR) != 1:
        raise SystemExit(f'expected one ProcessPair anchor, found {text.count(INSERT_ANCHOR)}')
    if text.count(CALL_ANCHOR) != 1:
        raise SystemExit(f'expected one last_decision anchor, found {text.count(CALL_ANCHOR)}')

    text = text.replace(INSERT_ANCHOR, FUNC + INSERT_ANCHOR, 1)
    text = text.replace(CALL_ANCHOR, CALL + CALL_ANCHOR, 1)
    verify(text)
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()

    path = Path(args.repo_root) / 'blueprint/source/BBMA_EA.mq4'
    text = path.read_text(encoding='utf-8')

    if args.verify:
        verify(text)
        print('D1-10 diagnostic wiring verified.')
        return

    new_text = apply(text)
    path.write_text(new_text, encoding='utf-8')
    print('D1-10 signal bottleneck diagnostic applied.')


if __name__ == '__main__':
    main()
