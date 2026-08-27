#!/usr/bin/env python3
"""Static regression for NMJE N3 canonical identity domain separation.

This test does not assert statistical collision resistance of SHORT_HASH. It
asserts that each canonical owner family is built from a distinct domain prefix
and the expected immutable provenance fields before hashing. That is the part
controlled by the EA source and prevents accidental cross-family identity aliasing.
"""
from pathlib import Path
import re

SRC = Path('blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8')


def body(name: str) -> str:
    m = re.search(rf'string\s+{re.escape(name)}\s*\([^)]*\)\s*\{{(.*?)\n\}}', SRC, re.S)
    if not m:
        raise AssertionError(f'missing helper: {name}')
    return m.group(1)


def require(text: str, *tokens: str) -> None:
    for token in tokens:
        if token not in text:
            raise AssertionError(f'missing token {token!r}')


def main() -> None:
    specs = {
        'NMJE_ReEntryEventID': ('RE|', ['pair', 'state.Timeframe', 'state.Direction', 'state.Type', 'state.StartCandleTime']),
        'NMJE_ExtremeEventID': ('EXT|', ['pair', 'state.Timeframe', 'state.Direction', 'state.RawCandleTime']),
        'NMJE_MLVEventID': ('MLV|', ['pair', 'PERIOD_M15', 'state.Direction', 'state.ParentRawCandleTime', 'state.ParentConfirmationCandleTime']),
        'NMJE_D1OwnerEventID': ('D1OWN|', ['pair', 'owner.State', 'owner.Direction', 'owner.SourceCandleTime']),
        'NMJE_H4OwnerEventID': ('H4OWN|', ['pair', 'owner.Direction', 'owner.SourceSignal', 'owner.SourceCandleTime']),
    }

    prefixes = []
    for helper, (prefix, fields) in specs.items():
        b = body(helper)
        require(b, f'"{prefix}"', 'NMJE_IdentityHash(raw)')
        for field in fields:
            require(b, field)
        prefixes.append(prefix)

    if len(prefixes) != len(set(prefixes)):
        raise AssertionError('canonical identity domain prefixes are not unique')

    hash_body = body('NMJE_IdentityHash')
    require(hash_body, 'SHORT_HASH(raw, 16)')

    # The identity layer must remain provenance-only and deterministic.
    forbidden = ('MathRand(', 'GetTickCount(', 'TimeCurrent()', 'MarketInfo(', 'iClose(', 'iOpen(')
    identity_region_start = SRC.index('string NMJE_IdentityHash(')
    identity_region_end = SRC.index('void NMJE_ResetNode(', identity_region_start)
    identity_region = SRC[identity_region_start:identity_region_end]
    for token in forbidden:
        if token in identity_region:
            raise AssertionError(f'non-deterministic/market-dependent identity input: {token}')

    print('NMJE_N3_IDENTITY_DOMAIN_STATIC=PASS')


if __name__ == '__main__':
    main()
