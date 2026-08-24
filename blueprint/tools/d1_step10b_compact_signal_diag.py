from pathlib import Path
import argparse

FUNC_NAME = 'PrintSignalBottleneckDiagnostic'
START = 'void PrintSignalBottleneckDiagnostic(int pairIndex, BBMA_Decision &decision)\n{'
END = 'void ProcessPair(int pairIndex)\n{'
MARKERS = ('[D1-10A]', '[D1-10B]', '[D1-10C]')

FUNC = r'''string D10Dir(ENUM_DIRECTION d)
{
   if(d == DIR_BUY) return "B";
   if(d == DIR_SELL) return "S";
   return "-";
}

string D10RE(ENUM_RE_STATE s)
{
   if(s == RE_STATE_CANDIDATE) return "C";
   if(s == RE_STATE_CONFIRMED) return "F";
   if(s == RE_STATE_EXPIRED) return "X";
   return "N";
}

string D10EXT(ENUM_EXTREME_MATURITY s)
{
   if(s == EXT_MAT_RAW) return "R";
   if(s == EXT_MAT_REVERSAL_CONFIRMED) return "REV";
   if(s == EXT_MAT_RETEST_PHASE) return "RT";
   if(s == EXT_MAT_RETEST_READY) return "RDY";
   if(s == EXT_MAT_VOID) return "V";
   if(s == EXT_MAT_SUPERSEDED) return "S";
   return "N";
}

string D10MLV(ENUM_MLV_STATE s)
{
   if(s == MLV_PARENT_READY) return "P";
   if(s == MLV_TP_COMPLETE) return "TP";
   if(s == MLV_LOSS_DEVELOPING) return "L";
   if(s == MLV_FORMATION_ESTABLISHED) return "F";
   if(s == MLV_RETEST_COMPLETE) return "RT";
   if(s == MLV_DIRECTION_TAKEN) return "T";
   if(s == MLV_VOID) return "V";
   if(s == MLV_SUPERSEDED) return "S";
   return "N";
}

string D10D1(ENUM_D1_OWNER_STATE s)
{
   if(s == D1_OWNER_BUY_CONFIRMED) return "B";
   if(s == D1_OWNER_SELL_CONFIRMED) return "S";
   if(s == D1_TRANSITION) return "T";
   return "U";
}

string D10H4(ENUM_H4_OWNER_STATE s, ENUM_DIRECTION d)
{
   if(s == H4_OWNER_ACTIVE) return D10Dir(d);
   if(s == H4_OWNER_RECOVERY_UNRESOLVED) return "U";
   return "N";
}

void PrintSignalBottleneckDiagnostic(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!g_pair_states[pairIndex].pair_enabled) return;

   string pair = g_pair_states[pairIndex].actual_symbol;
   string finalCandidate = "NONE";
   if(decision.Valid)
   {
      finalCandidate = EnumToString(decision.SignalType) + "/" +
                       D10Dir(decision.Direction) + "/" +
                       EnumToString(decision.DecisionState);
      if(decision.RejectionReason != REJ_NONE)
         finalCandidate += "/" + EnumToString(decision.RejectionReason);
   }

   Print("[D1-10A] ", pair,
         " D1=", D10D1(g_pair_states[pairIndex].d1_major_trend_owner.State),
         " H4=", D10H4(g_pair_states[pairIndex].h4_direction_owner.State,
                       g_pair_states[pairIndex].h4_direction_owner.Direction),
         " F=", finalCandidate);

   Print("[D1-10B] ", pair,
         " RE H1=", D10RE(g_pair_states[pairIndex].re_h1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_h1_sell_state.State),
         " H4=", D10RE(g_pair_states[pairIndex].re_h4_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_h4_sell_state.State),
         " D1=", D10RE(g_pair_states[pairIndex].re_d1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_d1_sell_state.State));

   Print("[D1-10C] ", pair,
         " X H1=", D10EXT(g_pair_states[pairIndex].extreme_h1_buy_lifecycle.Maturity), "/",
                    D10EXT(g_pair_states[pairIndex].extreme_h1_sell_lifecycle.Maturity),
         " H4=", D10EXT(g_pair_states[pairIndex].extreme_h4_buy_lifecycle.Maturity), "/",
                    D10EXT(g_pair_states[pairIndex].extreme_h4_sell_lifecycle.Maturity),
         " M15=", D10MLV(g_pair_states[pairIndex].mlv_buy_state.State), "/",
                     D10MLV(g_pair_states[pairIndex].mlv_sell_state.State));
}

'''


def verify(text: str) -> None:
    if text.count('void ' + FUNC_NAME + '(') != 1:
        raise SystemExit('compact diagnostic function missing or duplicated')
    for marker in MARKERS:
        if text.count(marker) != 1:
            raise SystemExit(f'{marker} missing or duplicated')
    if '[D1-10][BOTTLENECK]' in text:
        raise SystemExit('legacy long diagnostic marker still present')
    if text.count(FUNC_NAME + '(pairIndex, decision);') != 1:
        raise SystemExit('diagnostic call missing or duplicated')


def apply(text: str) -> str:
    start = text.find(START)
    if start < 0:
        raise SystemExit('existing diagnostic function start not found')
    end = text.find(END, start)
    if end < 0:
        raise SystemExit('ProcessPair anchor not found after diagnostic function')
    text = text[:start] + FUNC + text[end:]
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
        print('D1-10B compact diagnostic verified.')
        return

    path.write_text(apply(text), encoding='utf-8')
    print('D1-10B compact diagnostic applied.')


if __name__ == '__main__':
    main()
