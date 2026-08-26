from pathlib import Path
import re

SRC = Path('blueprint/source/BBMA_EA.mq4')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, got {n}')
    return text.replace(old, new, 1)


def regex_replace_once(text: str, pattern: str, repl: str, label: str) -> str:
    out, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 regex match, got {n}')
    return out


def main() -> None:
    text = SRC.read_text(encoding='utf-8')

    text = replace_once(
        text,
        '//| Version 4.5.8 - D1 TP-Wajib Lifecycle Stage                 |',
        '//| Version 4.5.9 - P0 Execution Identity Persistence Fix        |',
        'build header')
    text = replace_once(text, '#property version   "4.58"', '#property version   "4.59"', 'property version')

    # Broker comment is transport metadata only. Keep it compact enough for MT4
    # servers that truncate or discard long comments.
    text = regex_replace_once(
        text,
        r'string CreateOrderComment\(string decisionID, string pair,\s*'
        r'ENUM_DIRECTION direction, ENUM_SIGNAL_TYPE signalType,\s*'
        r'double intendedEntry, double intendedSL,\s*'
        r'double intendedLot, double intendedRisk,\s*'
        r'string sequenceHash, datetime candleTime\)\s*\{.*?\n\}\n\nbool ParseOrderCommentFull',
        '''string CreateOrderComment(string decisionID, string pair, 
                          ENUM_DIRECTION direction, ENUM_SIGNAL_TYPE signalType,
                          double intendedEntry, double intendedSL, 
                          double intendedLot, double intendedRisk,
                          string sequenceHash, datetime candleTime)
{
   // P0: broker comments are not an authoritative persistence store.
   // Keep only the compact execution hash for secondary/fallback evidence.
   return "BBMA|H:" + SHORT_HASH(decisionID);
}

bool ParseOrderCommentFull''',
        'compact broker comment')

    helper_anchor = '''bool ExtractExecutionHash(string comment, string &executionHash)
{
   executionHash = "";
   string prefix = "BBMA|H:";
   if(StringFind(comment, prefix) != 0) return false;

   int start = StringLen(prefix);
   int end = StringFind(comment, "|", start);
   if(end < 0) end = StringLen(comment);
   if(end <= start) return false;

   executionHash = StringSubstr(comment, start, end - start);
   return (executionHash != "");
}
'''

    helper_block = helper_anchor + r'''

// P0 durable execution identity persistence.
// MT4 terminal GlobalVariables are authoritative; OrderComment is fallback only.
string ExecutionHashGVBase(string executionHash)
{
   return "BBXH|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|H" + executionHash + "|";
}

string ExecutionTicketGVBase(int ticket)
{
   return "BBXT|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(ticket) + "|";
}

int HexDigitValue(string digit)
{
   string hex = "0123456789ABCDEF";
   return StringFind(hex, digit);
}

double Hex4ToNumber(string chunk)
{
   if(StringLen(chunk) != 4) return -1.0;
   int value = 0;
   for(int i = 0; i < 4; i++)
   {
      int nibble = HexDigitValue(StringSubstr(chunk, i, 1));
      if(nibble < 0) return -1.0;
      value = value * 16 + nibble;
   }
   return (double)value;
}

string NumberToHex4(double encoded)
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
}

bool LoadPersistedExecutionHashForTicket(int ticket, string pair,
                                         ENUM_DIRECTION direction, int magic,
                                         datetime openTime, string &executionHash)
{
   executionHash = "";
   if(ticket <= 0 || pair == "" || magic <= 0 || openTime <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return false;

   string base = ExecutionTicketGVBase(ticket);
   string keys[7] = {"H0","H1","H2","H3","M","O","D"};
   for(int i = 0; i < 7; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   int storedMagic = (int)GlobalVariableGet(base + "M");
   datetime storedOpen = (datetime)((int)GlobalVariableGet(base + "O"));
   ENUM_DIRECTION storedDirection =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   if(storedMagic != magic || storedOpen != openTime || storedDirection != direction)
      return false;

   string h0 = NumberToHex4(GlobalVariableGet(base + "H0"));
   string h1 = NumberToHex4(GlobalVariableGet(base + "H1"));
   string h2 = NumberToHex4(GlobalVariableGet(base + "H2"));
   string h3 = NumberToHex4(GlobalVariableGet(base + "H3"));
   if(h0 == "" || h1 == "" || h2 == "" || h3 == "") return false;
   executionHash = h0 + h1 + h2 + h3;

   string hashBase = ExecutionHashGVBase(executionHash);
   string hashKeys[4] = {"T","M","O","D"};
   for(int k = 0; k < 4; k++)
      if(!GlobalVariableCheck(hashBase + hashKeys[k]))
      {
         executionHash = "";
         return false;
      }

   if((int)GlobalVariableGet(hashBase + "T") != ticket ||
      (int)GlobalVariableGet(hashBase + "M") != magic ||
      (datetime)((int)GlobalVariableGet(hashBase + "O")) != openTime ||
      (ENUM_DIRECTION)((int)GlobalVariableGet(hashBase + "D")) != direction)
   {
      executionHash = "";
      return false;
   }
   return true;
}

bool SaveExecutionIdentityHash(string executionHash, int ticket, string pair,
                               ENUM_DIRECTION direction, int magic,
                               datetime openTime)
{
   if(StringLen(executionHash) != 16 || ticket <= 0 || pair == "" ||
      magic <= 0 || openTime <= 0 ||
      (direction != DIR_BUY && direction != DIR_SELL))
      return false;

   double h0 = Hex4ToNumber(StringSubstr(executionHash, 0, 4));
   double h1 = Hex4ToNumber(StringSubstr(executionHash, 4, 4));
   double h2 = Hex4ToNumber(StringSubstr(executionHash, 8, 4));
   double h3 = Hex4ToNumber(StringSubstr(executionHash, 12, 4));
   if(h0 < 0 || h1 < 0 || h2 < 0 || h3 < 0) return false;

   string hashBase = ExecutionHashGVBase(executionHash);
   string ticketBase = ExecutionTicketGVBase(ticket);

   if(GlobalVariableSet(hashBase + "T", (double)ticket) == 0) return false;
   if(GlobalVariableSet(hashBase + "M", (double)magic) == 0) return false;
   if(GlobalVariableSet(hashBase + "O", (double)openTime) == 0) return false;
   if(GlobalVariableSet(hashBase + "D", (double)direction) == 0) return false;

   if(GlobalVariableSet(ticketBase + "H0", h0) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H1", h1) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H2", h2) == 0) return false;
   if(GlobalVariableSet(ticketBase + "H3", h3) == 0) return false;
   if(GlobalVariableSet(ticketBase + "M", (double)magic) == 0) return false;
   if(GlobalVariableSet(ticketBase + "O", (double)openTime) == 0) return false;
   if(GlobalVariableSet(ticketBase + "D", (double)direction) == 0) return false;
   GlobalVariablesFlush();

   string verifyHash = "";
   return LoadPersistedExecutionHashForTicket(ticket, pair, direction, magic,
                                              openTime, verifyHash) &&
          verifyHash == executionHash;
}

int FindPersistedExecutionTicket(string decisionID, string pair, int orderType,
                                 int magicNumber)
{
   if(decisionID == "" || pair == "" || magicNumber <= 0 ||
      (orderType != OP_BUY && orderType != OP_SELL))
      return -1;

   string executionHash = SHORT_HASH(decisionID);
   string base = ExecutionHashGVBase(executionHash);
   string keys[4] = {"T","M","O","D"};
   for(int i = 0; i < 4; i++)
      if(!GlobalVariableCheck(base + keys[i])) return -1;

   int ticket = (int)GlobalVariableGet(base + "T");
   int storedMagic = (int)GlobalVariableGet(base + "M");
   datetime storedOpen = (datetime)((int)GlobalVariableGet(base + "O"));
   ENUM_DIRECTION storedDirection =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   ENUM_DIRECTION expectedDirection =
      (orderType == OP_BUY) ? DIR_BUY : DIR_SELL;

   if(ticket <= 0 || storedMagic != magicNumber || storedOpen <= 0 ||
      storedDirection != expectedDirection)
      return -1;
   if(!OrderSelect(ticket, SELECT_BY_TICKET)) return -1;
   if(OrderCloseTime() != 0 || OrderSymbol() != pair ||
      OrderMagicNumber() != magicNumber || OrderType() != orderType ||
      OrderOpenTime() != storedOpen)
      return -1;

   string ticketHash = "";
   if(!LoadPersistedExecutionHashForTicket(ticket, pair, expectedDirection,
                                           magicNumber, storedOpen, ticketHash))
      return -1;
   if(ticketHash != executionHash) return -1;
   return ticket;
}
'''

    text = replace_once(text, helper_anchor, helper_block, 'durable identity helpers')

    text = replace_once(
        text,
        'return (error == 135 || error == 138 || error == 128 || error == 146);',
        'return (error == 135 || error == 138 || error == 146);',
        'timeout retry classification')
    text = replace_once(
        text,
        'return (error == 4 || error == 6 || error == 141);',
        'return (error == 4 || error == 6 || error == 128 || error == 141);',
        'timeout ambiguous classification')

    text = regex_replace_once(
        text,
        r'int FindExistingExecutionTicket\(string pair, int direction, int magicNumber,\s*'
        r'string decisionID\)\s*\{.*?\n\}\n\nbool IsSignalAllowed',
        r'''int FindExistingExecutionTicket(string pair, int direction, int magicNumber,
                                string decisionID)
{
   if(pair == "" || magicNumber <= 0 || decisionID == "") return -1;

   // P0: durable terminal identity is authoritative.
   int persistedTicket = FindPersistedExecutionTicket(decisionID, pair,
                                                       direction, magicNumber);
   if(persistedTicket > 0) return persistedTicket;

   // Secondary fallback for legacy/current brokers that preserve the compact tag.
   string executionTag = "BBMA|H:" + SHORT_HASH(decisionID);
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      if(OrderCloseTime() != 0) continue;
      if(OrderSymbol() != pair) continue;
      if(OrderMagicNumber() != magicNumber) continue;
      if(OrderType() != direction) continue;

      if(StringFind(OrderComment(), executionTag) == 0)
         return OrderTicket();
   }

   return -1;
}

bool IsSignalAllowed''',
        'local-first existing execution lookup')

    old_rebuild = '''         string executionHash;
         if(!ExtractExecutionHash(OrderComment(), executionHash)) continue;

         ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
         UpsertExecutionHashTombstone(executionHash, OrderTicket(), symbol,
                                      liveDirection, OrderOpenTime());'''
    new_rebuild = '''         ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;
         string executionHash = "";
         bool localIdentity = LoadPersistedExecutionHashForTicket(
            OrderTicket(), symbol, liveDirection, magic, OrderOpenTime(), executionHash);
         if(!localIdentity)
         {
            if(!ExtractExecutionHash(OrderComment(), executionHash)) continue;
            // Migrate legacy/comment-backed identity into the durable terminal store.
            SaveExecutionIdentityHash(executionHash, OrderTicket(), symbol,
                                      liveDirection, magic, OrderOpenTime());
         }

         UpsertExecutionHashTombstone(executionHash, OrderTicket(), symbol,
                                      liveDirection, OrderOpenTime());'''
    text = replace_once(text, old_rebuild, new_rebuild, 'rebuild local identity first')

    old_recovery_head = '''      int magic = OrderMagicNumber();
      string pair = OrderSymbol();
      string comment = OrderComment();
      string executionHash = "";
      bool hasExecutionHash = ExtractExecutionHash(comment, executionHash);

      ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;'''
    new_recovery_head = '''      int magic = OrderMagicNumber();
      string pair = OrderSymbol();
      string comment = OrderComment();
      ENUM_DIRECTION liveDirection = (OrderType() == OP_BUY) ? DIR_BUY : DIR_SELL;

      string executionHash = "";
      bool localIdentity = LoadPersistedExecutionHashForTicket(
         OrderTicket(), pair, liveDirection, magic, OrderOpenTime(), executionHash);
      string brokerExecutionHash = "";
      bool brokerHashFound = ExtractExecutionHash(comment, brokerExecutionHash);
      if(!localIdentity && brokerHashFound)
      {
         executionHash = brokerExecutionHash;
         localIdentity = SaveExecutionIdentityHash(executionHash, OrderTicket(), pair,
                                                   liveDirection, magic, OrderOpenTime());
      }
      bool hasExecutionHash = (executionHash != "");'''
    text = replace_once(text, old_recovery_head, new_recovery_head, 'recovery local identity first')

    text = replace_once(
        text,
        '''      bool fullMetadata = hasExecutionHash &&
                          ParseOrderCommentFull(comment, decisionHash, parsedPair,''',
        '''      bool fullMetadata = brokerHashFound &&
                          ParseOrderCommentFull(comment, decisionHash, parsedPair,''',
        'legacy full metadata parser source')

    text = replace_once(
        text,
        '''      if(fullMetadata &&
         (decisionHash != executionHash || parsedPair != pair ||
          parsedDirection != liveDirection))''',
        '''      if(fullMetadata &&
         (decisionHash != brokerExecutionHash || parsedPair != pair ||
          parsedDirection != liveDirection))''',
        'full metadata broker hash self-check')

    text = replace_once(
        text,
        '''      else if(targetless && !fullMetadata)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_FULL_METADATA_REQUIRED";
      }''',
        '''      else if(targetless && !hasExecutionHash)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_DURABLE_IDENTITY_REQUIRED";
      }''',
        'targetless durable identity recovery')

    old_persist = '''         string expectedExecutionHash = SHORT_HASH(decision.DecisionID);
         string persistedExecutionHash = "";
         string persistedComment = OrderComment();
         bool persistedHashFound = ExtractExecutionHash(persistedComment, persistedExecutionHash);
         bool persistedHashMatch = (persistedHashFound &&
                                    persistedExecutionHash == expectedExecutionHash);
         info.execution_hash = persistedHashMatch ? persistedExecutionHash : "";
         info.recovery_state = lifecycleStateReady ? REC_NORMAL : REC_IDENTITY_MISSING_FROZEN;
         if(info.d1_tpw_lifecycle_managed && lifecycleStateReady &&
            !SaveD1TPWCheckpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "D1TPW checkpoint persist failed ticket=" + IntegerToString(ticket));
         }
         else if(info.c044_lifecycle_managed && lifecycleStateReady &&
                 !SaveC044Checkpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "C044 checkpoint persist failed ticket=" + IntegerToString(ticket));
         }

         Print("[P3S5][EXEC_ID] Ticket=", IntegerToString(ticket),
               " Pair=", pair,
               " Persist=", persistedHashMatch ? "PASS" : "FAIL",
               " HashFound=", persistedHashFound ? "Y" : "N",
               " HashMatch=", persistedHashMatch ? "Y" : "N",
               " ExpectedHash=", expectedExecutionHash,
               " PersistedHash=", persistedExecutionHash,
               " RawLen=", IntegerToString(StringLen(persistedComment)),
               " RawComment=<", persistedComment, ">");'''
    new_persist = '''         string expectedExecutionHash = SHORT_HASH(decision.DecisionID);
         bool localIdentityPersisted = SaveExecutionIdentityHash(
            expectedExecutionHash, ticket, pair, decision.Direction, magic, OrderOpenTime());

         string persistedComment = OrderComment();
         string brokerExecutionHash = "";
         bool brokerHashFound = ExtractExecutionHash(persistedComment, brokerExecutionHash);
         bool brokerHashMatch = (brokerHashFound &&
                                 brokerExecutionHash == expectedExecutionHash);

         info.execution_hash = localIdentityPersisted
            ? expectedExecutionHash
            : (brokerHashMatch ? brokerExecutionHash : "");
         info.recovery_state = (localIdentityPersisted && lifecycleStateReady)
            ? REC_NORMAL : REC_IDENTITY_MISSING_FROZEN;

         if(!localIdentityPersisted)
            Log(DBG_ERROR, "Execution identity persistence failed ticket=" + IntegerToString(ticket));

         if(info.d1_tpw_lifecycle_managed && lifecycleStateReady &&
            !SaveD1TPWCheckpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "D1TPW checkpoint persist failed ticket=" + IntegerToString(ticket));
         }
         else if(info.c044_lifecycle_managed && lifecycleStateReady &&
                 !SaveC044Checkpoint(info))
         {
            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
            Log(DBG_ERROR, "C044 checkpoint persist failed ticket=" + IntegerToString(ticket));
         }

         Print("[P3S5][EXEC_ID] Ticket=", IntegerToString(ticket),
               " Pair=", pair,
               " Persist=", localIdentityPersisted ? "PASS" : "FAIL",
               " Local=", localIdentityPersisted ? "Y" : "N",
               " BrokerHashFound=", brokerHashFound ? "Y" : "N",
               " BrokerHashMatch=", brokerHashMatch ? "Y" : "N",
               " ExpectedHash=", expectedExecutionHash,
               " BrokerHash=", brokerExecutionHash,
               " RawLen=", IntegerToString(StringLen(persistedComment)),
               " RawComment=<", persistedComment, ">");'''
    text = replace_once(text, old_persist, new_persist, 'post-send durable identity persistence')

    required = [
        'Version 4.5.9 - P0 Execution Identity Persistence Fix',
        '#property version   "4.59"',
        'return "BBMA|H:" + SHORT_HASH(decisionID);',
        'SaveExecutionIdentityHash',
        'LoadPersistedExecutionHashForTicket',
        'FindPersistedExecutionTicket',
        'Persist=", localIdentityPersisted ? "PASS" : "FAIL"',
        'return (error == 4 || error == 6 || error == 128 || error == 141);',
        'TARGETLESS_DURABLE_IDENTITY_REQUIRED',
    ]
    for marker in required:
        if marker not in text:
            raise SystemExit(f'missing P0 invariant after patch: {marker}')

    forbidden = [
        'return (error == 135 || error == 138 || error == 128 || error == 146);',
        'TARGETLESS_FULL_METADATA_REQUIRED',
    ]
    for marker in forbidden:
        if marker in text:
            raise SystemExit(f'stale P0-incompatible marker remains: {marker}')

    SRC.write_text(text, encoding='utf-8')
    print('P0_EXEC_ID_PERSISTENCE_PATCH=PASS')


if __name__ == '__main__':
    main()
