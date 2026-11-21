# Tengri + BBMA Hedge — locked replay checkpoint

Updated: 2026-11-22  
Status: **HOLD — no valid combined performance replay yet**  
Issue: #304  
Research branch: `research/tengri-bbma-hedge-replay-20261122`  
Base: `d1-owner-dev` at `7567af7dfbfaafff35a37c1d307b387e96273c78`

## Requested experiment

One offline, locked combined-account comparison for EURUSD and USDCHF, using the same frozen Tengri order stream, the D1 strategic owner → H4 structural owner → H1 Re-Entry chain, and a separate Hedge overlay. Report H1 Re-Entry Type 1, 2, 3, and 4 independently; keep data window, exit hypothesis, and costs the same across types. No parameter tuning on this sample.

Tengri source/behavior must remain unchanged. This is research only: no live or forward trading, no production activation, and no merge without separate authorization.

## Evidence checked

### Build/source identity

- BBMA source at base commit `7567af7dfbfaafff35a37c1d307b387e96273c78`, file `blueprint/source/BBMA_EA.mq4`, reports version `5.16`, tag `V516_M12_ENTRYCANDLE_GATE_20261107`, blob `05b961863b53e4c8408f152a5d800699b5f27eaf`.
- The same branch's `blueprint/source/EA_RELEASE_IDENTITY.json` still says display/property version 4.5.9/4.59 and points at source blob `dc83e62748c93171d89a312e9f7a53c06d97e261`. These records describe different builds and are not reconciled.
- The provided Tengri source is v1.45 / Magic 12345 per the existing lock report; the actual tester executable/build that produced the frozen ledger still needs a source-to-executable crosswalk.
- G40 Hedge source `Tengri_Hedge_ADX_H4_25_Overlay.mq4` is version 1.00. It reads Tengri orders by symbol and Magic 12345, but its entry signal is H4 Mid-BB + ADX(14)>25 + DI. It is **not a BBMA Re-Entry consumer** and cannot supply this experiment's Type 1–4 events.

### Data and warm-up

- Candidate evaluation window remains 2026-05-01 through 2026-11-18. The audit folder contains date-named EURUSD/USDCHF tick files from 2026-04-06 through 2026-11-19.
- A filename-level scan found all 144 calendar weekdays in the evaluation window for both pairs. This is not yet a verified quote-coverage pass: the full audit-folder tick counts/hashes were not reconciled to a manifest.
- Only 22 date-named files exist before 2026-05-01 (earliest 2026-04-06). The locked spec requires at least 51 closed D1 bars to calculate current and previous MA50 observations. This archive alone cannot establish that warm-up.
- The standalone root manifest covers a different slice (2026-07-27 to 2026-11-01); the root summary is marked `FETCH_COMPLETE_COVERAGE_NOT_YET_VERIFIED` and covers Aug–Oct. Those records do not prove May–Nov quote coverage.
- MT4 HST files staged for the overlay begin 2026-07-27. A separate MetaQuotes-Demo history file has older D1 bars but is a different server and must not be substituted. No matching HFM EURUSD/USDCHF D1 HST warm-up has been established yet.

### BBMA exit classification

- Core M17/M23 contracts distinguish source-defined destinations from EA lifecycle management. The normal BBMA EA position retains broker SL/TP; dynamic opposite-CSM close remains disabled pending separate lifecycle approval.
- Therefore, “close Hedge on the first confirmed H1 Re-Entry back toward Tengri's net direction” may be used only as a **research-defined Hedge exit hypothesis**, not as a universal BBMA source rule. Apply it identically to Type 1–4 if the test proceeds. Keep the shared safety close for Tengri-flat/net-direction-flip.
- The M15 processing clock, closed-candle signal confirmation, and immediate following H1 candle eligibility remain the timing basis. Do not consume candidate/unconfirmed signals.

## Locked comparison retained

| Variant | Hedge entry event |
|---|---|
| Baseline | None |
| Type 1 | Confirmed H1 Re-Entry Type 1 |
| Type 2 | Confirmed H1 Re-Entry Type 2 |
| Type 3 | Confirmed H1 Re-Entry Type 3 |
| Type 4 | Confirmed H1 Re-Entry Type 4 |

Common gates/settings retained from the existing lock: D1 and H4 owners agree with H1 signal; hedge direction opposes same-symbol Tengri net exposure; minimum 6 net-side Tengri layers; hedge target 25% of net lots rounded down; no cross-pair hedge; trim to target if net exposure shrinks. Use first fresh quote after the confirmed H1 candle closes. Preserve broker spread cap of 3 pips and the locked base/stress Hedge cost assumptions (1 pip/lot/action; stress adds 1 pip/lot/action). The existing frozen-order replay still does not model Hedge P&L feeding back into later Tengri lot sizes; label results as an overlay replay, not a fully path-dependent two-EA account simulation.

## Gates before the single run

1. Reconcile the BBMA source/build record used by the signal harness; do not silently rewrite the canonical 4.59 release identity.
2. Identify/hash the actual Tengri tester source/executable for the frozen order ledger and pin the Hedge research source/build.
3. Obtain matching-broker D1/H4/H1 history back far enough to reconstruct D1 MA50 and H4/H1 structural owner state; verify tick-file counts, quotes, timestamps, and hashes across the full evaluation window.
4. Produce an auditable confirmed-event stream from the pinned BBMA source/contract. The existing ADX25 overlay is not a substitute.
5. Freeze the common exit hypothesis and all costs before examining variant performance.
6. Run once; report net expectancy, profit factor, floating drawdown, total costs, and number of campaigns/tickets separately by type, pair, and combined account. Record exclusions and open-at-end Hedge exposure.

Until these pass, status remains **HOLD**. No profitability figures are reported from the current ADX overlay as though they were BBMA Type 1–4 results.
