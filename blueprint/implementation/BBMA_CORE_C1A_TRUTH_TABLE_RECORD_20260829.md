# BBMA Core C1-A Truth-Table Record — 2026-08-29

## Scope

Materialize the first safe core-perfection step as an audit-only contract and
deterministic golden fixture. The work reads build 4.71 behavior and introduces
no EA source, detector, geometry, frequency, risk, authority, or activation
change.

Branch boundary:

- base: `d1-tpw-checkpoint-hardening-dev` at
  `5d752fef4e7a2871f3b6de613790a531b8ca0cb4`;
- head: `bbma-core-truth-table-dev`;
- draft/no merge/no activation;
- no change targets `main`.

## Locked inventory

- M07 BB shape;
- M08 Extreme lifecycle;
- M09 MHV/MLV lifecycle with M08 parent single-writer boundary;
- M10 CSM/CSD/eCSD atoms;
- M12 Re-Entry Types 1-4 and ownership precedence;
- M13 REM/RRE/REE collection only;
- M14 exact signature and direction validation;
- M15 final signal authority and sole M15 processing clock;
- M22 sole `OrderSend` source owner.

Golden coverage:

- 34 explicit transitions: 9 Extreme, 10 MLV, 15 Re-Entry;
- 8 BUY/SELL state-symmetry checks;
- 12 REM/RRE/REE topology and direction checks;
- fail-closed undefined-transition checks;
- semantic-source mapping lock for D1-opportunity RE, legacy RE, REM, RRE, REE.

## Identity hashes

- EA source SHA-256:
  `c6a87f613495547ee3cf52a8fe041ae6f9a63396075c0c755a7475b9f488a7bb`
- Golden fixture SHA-256:
  `7706834380a48430f0397aedacde66cd8bdd92979b24441da2adf357c0dd9dc5`
- Contract SHA-256:
  `3b0316c82db0402697c9bcbed7883db31f64cd462dc0c53fe765fb59226dc891`

## Verification target

- golden truth-table model: PASS;
- source/authority static lock: PASS;
- full existing N3/NMJE/D1TPW/core suite: PASS;
- Python compilation: PASS;
- exact EA source hash unchanged from branch base;
- no native MetaEditor run required because `.mq4` is unchanged.

## Non-authorization

This evidence does not prove market edge or candle-price equivalence and does
not authorize NMJE execution, D1TPW, C044, KIV risk features, demo/live use,
merge, or release. Any semantic difference discovered in later candle fixtures
must stop for explicit strategy review before source modification.

