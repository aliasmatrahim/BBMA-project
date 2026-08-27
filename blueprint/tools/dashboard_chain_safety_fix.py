#!/usr/bin/env python3
"""Harden the compact M25 dashboard after the primary materializer.

Display-only fixes:
1. Aggregate every EA-owned live position for a pair instead of returning the
   first selected order.
2. Represent equal-rank opposing BUY/SELL signal chains explicitly as MIX
   instead of arbitrarily preferring BUY.

This script intentionally changes dashboard presentation only. It does not
call or add trade, risk, validation, lifecycle, or execution authorities.
"""
from pathlib import Path
import sys

SRC = Path('blueprint/source/BBMA_EA.mq4')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def main() -> int:
    text = SRC.read_text(encoding='utf-8')

    old_live = '''string DashLivePosition(int pairIndex, ENUM_DIRECTION &direction)
{
   direction = DIR_NONE;
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;
      if(selectedPairIndex != pairIndex) continue;
      int type = OrderType();
      if(type == OP_BUY)
      {
         direction = DIR_BUY;
         return "POS↑";
      }
      if(type == OP_SELL)
      {
         direction = DIR_SELL;
         return "POS↓";
      }
   }
   return "";
}'''

    new_live = '''string DashLivePosition(int pairIndex, ENUM_DIRECTION &direction)
{
   direction = DIR_NONE;
   int buyCount = 0;
   int sellCount = 0;
   int total = OrdersTotal();

   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;
      if(selectedPairIndex != pairIndex) continue;

      int type = OrderType();
      if(type == OP_BUY) buyCount++;
      else if(type == OP_SELL) sellCount++;
   }

   // Display every EA-owned live position for the pair. Never let order
   // enumeration order hide a second position or the opposite direction.
   if(buyCount > 0 && sellCount > 0)
      return "POS↑x" + IntegerToString(buyCount) + "/↓x" + IntegerToString(sellCount);

   if(buyCount > 0)
   {
      direction = DIR_BUY;
      if(buyCount == 1) return "POS↑";
      return "POS↑x" + IntegerToString(buyCount);
   }

   if(sellCount > 0)
   {
      direction = DIR_SELL;
      if(sellCount == 1) return "POS↓";
      return "POS↓x" + IntegerToString(sellCount);
   }

   return "";
}'''

    old_rank = '''   if(buyRank > 0 || sellRank > 0)
   {
      if(buyRank >= sellRank)
      {
         rowDirection = DIR_BUY;
         status = buyStatus;
         setup = buySetup;
         chain = buyChain;
      }
      else
      {
         rowDirection = DIR_SELL;
         status = sellStatus;
         setup = sellSetup;
         chain = sellChain;
      }
   }

   position = DashLivePosition(pairIndex, positionDirection);'''

    new_rank = '''   if(buyRank > 0 || sellRank > 0)
   {
      if(buyRank > sellRank)
      {
         rowDirection = DIR_BUY;
         status = buyStatus;
         setup = buySetup;
         chain = buyChain;
      }
      else if(sellRank > buyRank)
      {
         rowDirection = DIR_SELL;
         status = sellStatus;
         setup = sellSetup;
         chain = sellChain;
      }
      else
      {
         // Equal-rank opposite directions are both material information.
         // Display them explicitly; do not bias the dashboard toward BUY.
         rowDirection = DIR_NONE;
         status = "MIX";
         setup = buySetup + "/" + sellSetup;
         chain = "B:" + buyChain + " | S:" + sellChain;
      }
   }

   position = DashLivePosition(pairIndex, positionDirection);'''

    try:
        text = replace_once(text, old_live, new_live, 'live-position aggregation')
        text = replace_once(text, old_rank, new_rank, 'equal-rank direction handling')
    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 3

    required = [
        'int buyCount = 0;',
        'int sellCount = 0;',
        'POS↑x',
        'POS↓x',
        'status = "MIX";',
        'chain = "B:" + buyChain + " | S:" + sellChain;',
    ]
    for token in required:
        if token not in text:
            print(f'ERROR: required dashboard safety token missing: {token}', file=sys.stderr)
            return 4

    forbidden = [
        'if(buyRank >= sellRank)',
    ]
    for token in forbidden:
        if token in text:
            print(f'ERROR: forbidden biased dashboard token remains: {token}', file=sys.stderr)
            return 5

    SRC.write_text(text, encoding='utf-8')
    print('DASHBOARD_CHAIN_SAFETY_FIX=APPLIED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
