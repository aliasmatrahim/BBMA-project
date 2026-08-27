#!/usr/bin/env python3
"""Fail-closed source-scope guard for the compact dashboard materializer.

Allowed source delta relative to workflow HEAD:
- complete Module 25 replacement; and
- the exact display-only OnDeinit cleanup hook that removes BBMA_DASH_ objects.

Any other source difference fails the guard.
"""
from pathlib import Path
import difflib
import subprocess
import sys

SRC = Path('blueprint/source/BBMA_EA.mq4')

OLD_DEINIT = '''   g_is_scanning = false;
   g_is_managing_trade = false;
   g_dashboard_needs_update = false;
   if(ShowDashboard)
      Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''

NEW_DEINIT = '''   g_is_scanning = false;
   g_is_managing_trade = false;
   g_dashboard_needs_update = false;

   // Display cleanup only. Never leave BBMA_DASH_ labels orphaned after EA
   // removal, recompile or chart shutdown.
   ClearDashboardObjects();
   Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''


def m25_bounds(text: str):
    start_marker = '//| MODULE 25: DASHBOARD ENGINE'
    end_marker = '//| MODULE 26: INITIALIZATION & CLEANUP'
    start = text.index(start_marker)
    end = text.index(end_marker)
    block_start = text.rfind('//+------------------------------------------------------------------+', 0, start)
    block_end = text.rfind('//+------------------------------------------------------------------+', 0, end)
    if block_start < 0 or block_end <= block_start:
        raise RuntimeError('unable to resolve M25 module boundaries')
    return block_start, block_end


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def main() -> int:
    try:
        baseline = subprocess.check_output(
            ['git', 'show', 'HEAD:blueprint/source/BBMA_EA.mq4'],
            text=True,
            encoding='utf-8',
        )
        candidate = SRC.read_text(encoding='utf-8')

        base_start, base_end = m25_bounds(baseline)
        cand_start, cand_end = m25_bounds(candidate)

        # Restore baseline M25 into the candidate, then restore the one allowed
        # OnDeinit display-cleanup hook. The result must be byte-for-text equal
        # to workflow HEAD; otherwise another module was modified.
        normalized = (
            candidate[:cand_start]
            + baseline[base_start:base_end]
            + candidate[cand_end:]
        )
        normalized = replace_once(
            normalized, NEW_DEINIT, OLD_DEINIT, 'allowed OnDeinit cleanup delta'
        )
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'DASHBOARD_SCOPE_GUARD=FAIL reason={exc}', file=sys.stderr)
        return 3

    if normalized != baseline:
        print('DASHBOARD_SCOPE_GUARD=FAIL unexpected source delta outside M25/OnDeinit',
              file=sys.stderr)
        diff = difflib.unified_diff(
            baseline.splitlines(), normalized.splitlines(),
            fromfile='HEAD/BBMA_EA.mq4', tofile='normalized-candidate/BBMA_EA.mq4',
            lineterm=''
        )
        for idx, line in enumerate(diff):
            if idx >= 120:
                print('... diff truncated ...', file=sys.stderr)
                break
            print(line, file=sys.stderr)
        return 4

    print('DASHBOARD_SCOPE_GUARD=PASS allowed=M25+OnDeinitDisplayCleanup')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
