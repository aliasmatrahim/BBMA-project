# BBMA Finale — Strategy Core Implementation Gap Register

## Purpose
Separate **source knowledge changes** from **active EA implementation gaps**. A source rule can already be correct in the BBMA Core specification while the current code still implements it incompletely.

Audit basis:
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`
- current Core contracts (`M08`, `M10`, `M12`, `M15`, `M17`)
- BBMA Finale V01–V07 evidence
- active `blueprint/source/BBMA_EA.mq4` on the status-owner branch identified by `blueprint/CURRENT.md`

No item in this file is an instruction to patch the EA during the current runtime/debug phase. It is a KIV source-alignment backlog.

| ID | Area | Current active behavior | Source/Core expectation | Assessment | Priority |
|---|---|---|---|---|---|
| IG-01 | M09 MLV outer-BB invalidation | `MarkMLVVoid()` exists, but the active source only contains its definition; `DetectMLV_State()` does not call it when a candidate/confirmed MLV closes outside the relevant outer BB | Existing PDF Core and Finale V05 both say MHV/MLV becomes void when price closes outside the relevant outer BB / turns into momentum | **CORRECT — genuine implementation gap** | **HIGH** |
| IG-02 | M09 MLV pattern construction | Candidate is hard-wired to current High/Low vs bar `+2`, `< point*10` tolerance, and a synthetic `point*5` neckline; candidate type is only `DoubleTop`/`DoubleBottom` | Existing Core emphasizes highest/lowest **body** marking and retest; double/triple morphology is descriptive, and the sources do not define those fixed point thresholds | **CORRECT / RE-DESIGN SOURCE ENCODING** | **HIGH** |
| IG-03 | M09 raw `DetectMHV()` | Uses close vs MA5 and MA5 slope only; does not encode prior Extreme/TP context, inside-outer-BB validity or retest structure | PDF + Finale describe MHV/MLV as a loss-of-volume setup after Extreme/TP with outer-BB validity and retest context | **CORRECT or demote/remove legacy detector** | **MEDIUM-HIGH** |
| IG-04 | M07 `BB_FLAT` state | `DetectBBState()` returns SQUEEZE below 0.9, EXPANDING above 1.1, and CONTRACTING for 0.9–1.1; the remaining `BB_FLAT` return is effectively unreachable for valid positive ratios | Finale V02 gives flat/horizontal BB explicit semantic importance | **CORRECT auxiliary classification** | **MEDIUM** |
| IG-05 | M10 CSM / momentum | Requires outer-BB close + width expansion + directional Mid/outer movement | PDF Core and Finale both require expanding/directional BB context for momentum | **KEEP — no fix** | NONE |
| IG-06 | M10 eCSD/CSD | eCSD crosses relevant MA5/10; CSD crosses MA5/10 + Mid BB; raw signals are not directly executable | Matches PDF Core and Finale V03/V05/V06 | **KEEP — no fix** | NONE |
| IG-07 | M12 MA5/MA10 Re-Entry close-side rule | BUY confirmation closes on/above MA5/10 Low cluster; SELL confirmation closes on/below MA5/10 High cluster | Matches Finale statement that a Re-Entry may penetrate MA5 but should not close through/clear both MAs | **KEEP — verify all type paths only** | LOW/VERIFY |
| IG-08 | M12 Re-Entry first/second-candle semantics | Confirmation metadata and `EntryPrice` are stored from the fully closed validation candle; actual broker execution is later at live ASK/BID | Finale says first Re-Entry candle validates and second candle is entry | **VERIFY SEMANTICS — not proven gap** | **MEDIUM VERIFY** |
| IG-09 | M08 standalone Extreme lifecycle | M08 intentionally detects raw Extreme signal only; standalone Extreme is withheld from Mode 2 | Existing Core and Finale both require reversal + retest before standalone Extreme entry; Finale still contains unresolved exceptions | **KEEP WITHHELD — no implementation expansion yet** | NONE |
| IG-10 | Extreme TP Wajib | Current executable Mode 1/2 decisions source TP from Re-Entry components; standalone Extreme is non-executable | Finale clarifies normal standalone Extreme TP Wajib toward opposite MA5/MA10 first | **DORMANT SPEC CLARIFICATION, not current live TP bug** | LOW/FUTURE |
| IG-11 | REM/RRE/REE signatures | Current M13/M14 exact signatures match the PDF-derived contracts | Finale does not provide unambiguous subtitle-only evidence to replace them | **KEEP — no fix** | NONE |

## Highest-value future repairs
### P1 — M09 source alignment
The strongest actionable finding is M09. This is supported by **both** the pre-existing PDF Core and Finale, so it is not a speculative video-only change.

A future repair should first define one canonical MHV/MLV owner/state model and then ensure:
- outer-BB close voids candidate/confirmed state immediately on the source timeframe;
- highest/lowest body and retest ownership are explicit;
- no arbitrary fixed point tolerance is presented as an Oma Ally rule;
- pattern morphology is not restricted to an invented single double-top/bottom formula unless explicitly classified as engineering interpretation;
- the legacy raw `DetectMHV()` cannot contradict the persistent MLV/MHV owner.

### P2 — BB flat classification
Fix the auxiliary state enum so `BB_FLAT` is reachable and semantically distinct. This is lower priority than M09 because the active M10 CSM detector already uses direct expansion/directional tests and is currently source-aligned.

### VERIFY — Re-Entry timing before changing anything
Do not add a new waiting candle yet. The current architecture processes closed source candles and executes later at the live market price. A timestamp audit should answer whether the current market entry already occurs on the second Re-Entry candle as Finale describes. Only if execution is demonstrably one candle too early should M12/M15 timing be altered.

## Non-findings
Finale does **not** justify changing the following merely for the sake of change:
- M10 expanding-BB momentum rule;
- eCSD/CSD semantics;
- Type 2 three-candle confluence;
- current exact REM/RRE/REE signatures;
- prohibition on raw direction/Extreme execution;
- Mode 1/Mode 2 eligibility contract.
