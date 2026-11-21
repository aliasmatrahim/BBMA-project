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

- Evaluation window: 2026-05-01 through 2026-11-18. EURUSD and USDCHF quote-day coverage is now verified for all 145 weekdays. The existing replay records monthly coverage of 21, 22, 23, 21, 22, 23, and 13 days (May–November), with no missing weekday in the evaluation window. Broker-clock calibration selected offset 0 hours (552 matched executions; median price difference 0.2 pip), and the replay asserts that alignment.
- The initial tick-file scan found only 22 pre-window dates, which was not enough to prove D1 warm-up. This is now resolved with OHLC history fetched directly from **HFMarketsGlobal-Demo4** via MT5 `copy_rates_range`, spanning 2025-01-02 through 2026-11-18 for both symbols. All exported bars were strictly ordered, duplicate-free, finite, and passed basic OHLC checks.
- Before the evaluation window, the export provides 345 closed D1 bars, 2,066 H4 bars, 8,248 H1 bars, and 32,983 M15 bars for EURUSD / 32,982 M15 bars for USDCHF. This exceeds the locked minimum of 51 closed D1 observations for MA50 and provides a long chronological warm-up for MTF state reconstruction. H4/H1 owner-state reconstruction itself still needs to be demonstrated by the signal harness.
- Bar export and SHA-256 manifest are on G40 under `C:\Trading\Tengri-Hedge-Research\Statement_Floating_Audit_20261119\bars_HFM_Demo4_20250101_20261119`. Hashes:

| Symbol | M15 | H1 | H4 | D1 |
|---|---|---|---|---|
| EURUSD | `95c3957f80f114dba24370976fbdb0fa6f6d80708cd734b483f002e21e59160a` | `d2c5a211e3589385b9e6b5283151beaf075dd4ba3388192027f36ebe4108c4f4` | `73c067eabb5ce63adbb9ea3884d8cc78936835459f5a0a5749aecbd1fa52693a` | `6ac5138674c8738b41d22a748c0a371636f110e3d07fd04f6933d2acd08bbe62` |
| USDCHF | `39af844caad33ebc73c82e01a52b76820340b562470e47d42572b492e0c8edab` | `52c46add281e59a9051f7d73a0b78063cdda1a2cd5282df9a3c82978463ba7d1` | `9c20584149327ac30a200e7be1fa281302e662e22aed8802b5832a8db5cfce58` | `1dec4b0bbbbe23723d8cc43d9676c33adf37b3e6d0dba243b20d668150cdaa6c` |

- The other-server MetaQuotes-Demo HST data is excluded. The evaluation quote archive is treated as HFM Demo4 only; the live-server M15/H1/H4/D1 bars above provide signal/warm-up inputs while the tick archive supplies fill and marking quotes.
- Hedge transaction charges remain a separate unresolved cost limitation: the frozen replay models the same spread cap plus 1 pip/lot/action and a +1 pip stress case, but does not yet replay broker-specific Hedge commission, swap, partial fills, or rejected fills.

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


### Static source audit — Build 5.16

- The pinned Build 5.16 source constructs confirmed Re-Entry candidates only for H1 and requires a current entry candle, a confirmed H1 signal, and an active, valid, recovered H4 directional owner in the same direction. The M15 atomic decision path also filters each candidate through the D1-owner gate and freezes the D1 owner snapshot before selection. These checks are present in source at the pinned base commit; they are not runtime evidence.
- The F4 decision note on the base branch still describes implementation as pending / H4-only. That note conflicts with the inspected Build 5.16 source. It remains unedited; resolve the documentation provenance separately so this research does not rewrite a Core decision record.
- The source state machine gives specific Type 3 (CSM precursor) and Type 4 (CSD precursor) ownership priority, then Type 2, before generic Type 1. Type 1 requires prior directional ownership plus structural ranging/retrace; Type 2 requires three qualifying candles; Type 3 waits for MA5/MA50 retrace; Type 4 waits for MA5/10 retrace. All are closed-source-candle states. The exact implementation must still be exercised or independently audited before emitting tradeable events.
- Runtime/compile identity is still unresolved. MT4 4.0.1492 and MetaEditor 5.0.2425 are installed on G40; the available canonical BBMA tester folder contains older 5.99 artifacts, not the pinned Build 5.16 source. No Build 5.16 executable/hash or signal log has yet been produced.

## Current status after audit

Data and D1 warm-up are **PASS** for the same HFM Demo4 server and evaluation window. Static D1/H4 ownership logic is **present in pinned source**. The combined replay remains **HOLD** because the Build 5.16 runtime signal stream and Tengri ledger-to-executable crosswalk have not yet been verified, and Hedge execution-cost details remain incomplete. No Type 1–4 profitability result is available.


### Build 5.16 compile identity

- The exact pinned `blueprint/source/BBMA_EA.mq4` file was copied to an isolated G40 research folder and compiled with HFM MT4 MetaEditor 5.0.2425. Compile log: **0 errors, 0 warnings**. No production EA/source was overwritten.
- Source SHA-256: `5264A5D10F146B9ADDAEA3B167BEA07D7EEC0EF1E55984374F96DB8A53CD9228` (Git blob `05b961863b53e4c8408f152a5d800699b5f27eaf`). Compiled audit EX4 SHA-256: `E896C34E4D07E84F20A4CAB346BC372527ACD77115E45A0D6636A68BFC8F3D29`.
- This proves the pinned source compiles in the available MT4 compiler. It does not yet prove tester/runtime signal parity or owner recovery behavior. The replay remains HOLD pending a confirmed source-derived event stream and the Tengri ledger crosswalk.
