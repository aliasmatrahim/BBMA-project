from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p0_exec_id_persistence_fix as base

SRC = Path('blueprint/source/BBMA_EA.mq4')


def main() -> None:
    base.main()
    text = SRC.read_text(encoding='utf-8')

    old = '''string NumberToHex4(double encoded)
{
   int value = (int)MathRound(encoded);
   if(value < 0 || value > 65535) return "";
   string hex = "0123456789ABCDEF";
   string result = "0000";
   for(int pos = 3; pos >= 0; pos--)
   {
      int nibble = value % 16;
      result = StringSetChar(result, pos, StringGetChar(hex, nibble));
      value /= 16;
   }
   return result;
}'''
    new = '''string NumberToHex4(double encoded)
{
   int value = (int)MathRound(encoded);
   if(value < 0 || value > 65535) return "";
   string hex = "0123456789ABCDEF";
   string result = "";
   int divisor = 4096;
   for(int pos = 0; pos < 4; pos++)
   {
      int nibble = value / divisor;
      result += StringSubstr(hex, nibble, 1);
      value = value % divisor;
      if(divisor > 1) divisor /= 16;
   }
   return result;
}'''
    if text.count(old) != 1:
        raise SystemExit(f'NumberToHex4 correction: expected 1 match, got {text.count(old)}')
    text = text.replace(old, new, 1)

    required = [
        'Version 4.5.9 - P0 Execution Identity Persistence Fix',
        'return "BBMA|H:" + SHORT_HASH(decisionID);',
        'bool SaveExecutionIdentityHash(',
        'bool LoadPersistedExecutionHashForTicket(',
        'int FindPersistedExecutionTicket(',
        'Persist=", localIdentityPersisted ? "PASS" : "FAIL"',
        'BrokerHashFound=',
        'TARGETLESS_DURABLE_IDENTITY_REQUIRED',
        'error == 128 || error == 141',
    ]
    for marker in required:
        if marker not in text:
            raise SystemExit(f'missing P0 V2 invariant: {marker}')
    if 'StringSetChar' in text:
        raise SystemExit('stale StringSetChar remains')
    if 'error == 138 || error == 128 || error == 146' in text:
        raise SystemExit('timeout still classified retryable')

    SRC.write_text(text, encoding='utf-8')
    print('P0_EXEC_ID_PERSISTENCE_PATCH_V2=PASS')


if __name__ == '__main__':
    main()
