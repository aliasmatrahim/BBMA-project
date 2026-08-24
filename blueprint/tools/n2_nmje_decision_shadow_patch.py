from pathlib import Path
import subprocess

SRC = Path('blueprint/source/BBMA_EA.mq4')
EXPECTED_BLOB = 'e1329219e8fad10e4242f7cf2769593cdf09063e'


def git_blob(path: Path) -> str:
    return subprocess.check_output(['git', 'hash-object', str(path)], text=True).strip()


def extract_function(text: str, name: str) -> str:
    needle = name + '('
    pos = text.find(needle)
    if pos < 0:
        raise RuntimeError(f'function not found: {name}')
    line_start = text.rfind('\n', 0, pos) + 1
    brace = text.find('{', pos)
    if brace < 0:
        raise RuntimeError(f'opening brace not found: {name}')
    depth = 0
    i = brace
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return text[line_start:i + 1]
        i += 1
    raise RuntimeError(f'unterminated function: {name}')


if not SRC.exists():
    raise SystemExit('source missing')

actual = git_blob(SRC)
if actual != EXPECTED_BLOB:
    raise SystemExit(f'unexpected baseline source blob: {actual}')

text = SRC.read_text(encoding='utf-8')
if '[N2-NMJE-DEC]' in text:
    raise SystemExit('N2 decision shadow already present')

critical_names = [
    'BuildPossibleCombinations',
    'ValidateSequence',
    'PriorityEngine_Atomic',
    'InvalidationEngine_Atomic',
    'ResolveApprovedInitialSLTP',
    'RunEntryPreflightAndExecute',
]
critical_before = {name: extract_function(text, name) for name in critical_names}
append_count_before = text.count('AppendValidatedCandidate(')
order_send_before = text.count('OrderSend(')

module13_pos = text.find('//| MODULE 13:')
if module13_pos < 0:
    raise SystemExit('MODULE 13 marker missing')
module13_start = text.rfind('//+------------------------------------------------------------------+', 0, module13_pos)
if module13_start < 0:
    raise SystemExit('MODULE 13 heading start missing')

shadow_fn = r'''// N2-01: post-M16 shadow tag for validated decisions only.
// Observation metadata only. It does not mutate decision, candidate, risk or execution state.
string NMJE_LogIdentityToken(string value)
{
   // DecisionID contains a human-readable TimeToString() component with a space.
   // Encode whitespace so the diagnostic remains a deterministic single token.
   string token = value;
   StringReplace(token, " ", "~");
   StringReplace(token, "\t", "~");
   return token;
}

void NMJE_PrintValidatedDecisionShadow(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   if(!decision.Valid || decision.DecisionState != DEC_VALIDATED) return;

   NestedJourneyState journey = g_nested_journeys[pairIndex];
   string journeyId = journey.JourneyID;
   if(journeyId == "") journeyId = "-";

   string decisionToken = NMJE_LogIdentityToken(decision.DecisionID);
   string decisionHash = SHORT_HASH(decision.DecisionID);

   Print("[N2-NMJE-DEC] ", decision.Pair,
         " SIG=", EnumToString(decision.SignalType),
         " DIR=", NMJE_DirText(decision.Direction),
         " REL=", NMJE_RelationText(journey.Relation),
         " P=", NMJE_ParentText(journey.ParentKind), "/", NMJE_DirText(journey.ParentDirection),
         " J=", journeyId,
         " DID=", decisionToken,
         " DIDH=", decisionHash);
}

'''
text = text[:module13_start] + shadow_fn + text[module13_start:]

call_anchor = '''   if(decision.DecisionState == DEC_VALIDATED)\n      RunEntryPreflightAndExecute(decision, actual);\n'''
if text.count(call_anchor) != 1:
    raise SystemExit(f'validated execution anchor count={text.count(call_anchor)}')
call_replacement = '''   if(decision.DecisionState == DEC_VALIDATED)\n   {\n      // N2-01 shadow metadata only; execution path remains unchanged.\n      NMJE_PrintValidatedDecisionShadow(pairIndex, decision);\n      RunEntryPreflightAndExecute(decision, actual);\n   }\n'''
text = text.replace(call_anchor, call_replacement, 1)

text = text.replace('Version 4.5.1 - N1-03 NMJE Observer',
                    'Version 4.5.1 - N2-01 NMJE Decision Shadow', 1)
text = text.replace('BBMA EA V4.5.1 N1-03 initialized successfully',
                    'BBMA EA V4.5.1 N2-01 initialized successfully', 1)

for name in critical_names:
    after = extract_function(text, name)
    if after != critical_before[name]:
        raise SystemExit(f'critical function changed unexpectedly: {name}')

if text.count('AppendValidatedCandidate(') != append_count_before:
    raise SystemExit('candidate append count changed')
if text.count('OrderSend(') != order_send_before:
    raise SystemExit('OrderSend call count changed')
if text.count('NMJE_PrintValidatedDecisionShadow(pairIndex, decision);') != 1:
    raise SystemExit('decision shadow call must appear exactly once')
if 'DIDH=' not in text:
    raise SystemExit('decision shadow persisted-hash field missing')
if 'NMJE_LogIdentityToken' not in text:
    raise SystemExit('decision identity token encoder missing')

block_start = text.find('//| MODULE 12N: NESTED MTF JOURNEY ENGINE')
block_end = text.find('//| MODULE 13:', block_start)
if block_start < 0 or block_end < 0:
    raise SystemExit('M12N bounds missing')
block = text[block_start:block_end]
for forbidden in [
    'OrderSend(', 'RunEntryPreflightAndExecute(', 'BuildPossibleCombinations(',
    'ValidateSequence(', 'PriorityEngine_Atomic(', 'InvalidationEngine_Atomic(',
    'DetectExtreme(', 'DetectMHV(', 'UpdateReEntryState('
]:
    if forbidden in block:
        raise SystemExit(f'forbidden M12N ownership call: {forbidden}')

SRC.write_text(text, encoding='utf-8', newline='\n')
print('N2-01A NMJE validated-decision shadow patch applied')
print('baseline_blob=', actual)
print('new_blob=', git_blob(SRC))
