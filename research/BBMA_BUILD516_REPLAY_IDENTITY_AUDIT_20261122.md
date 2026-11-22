# BBMA Build 5.16 replay identity and open-gate audit

Date: 22 Nov 2026  
Status: **Build source/release identities distinguished; clean signal-event replay verified; account residual and production execution gates remain open.**  
Scope: research branch only. No production EA source/configuration was changed and no live/demo order was activated.

## Build identity

- d1-owner-dev is at owner commit 7567af7dfbfaafff35a37c1d307b387e96273c78, where PR #301 merged Build 5.16 / V516_M12_ENTRYCANDLE_GATE_20261107.
- The current source blueprint/source/BBMA_EA.mq4 has Git blob 05b961863b53e4c8408f152a5d800699b5f27eaf. G40 raw source SHA-256: 5264A5D10F146B9ADDAEA3B167BEA07D7EEC0EF1E55984374F96DB8A53CD9228.
- G40 BBMA_EA.ex4 SHA-256: E896C34E4D07E84F20A4CAB346BC372527ACD77115E45A0D6636A68BFC8F3D29. compile.log SHA-256 187057FD27AC2A0DFA7595811E291821E006E23B0FAF800393F144E95A32C8EE records 0 errors and 0 warnings.
- EA_RELEASE_IDENTITY.json is a different, deliberately frozen v4.59 release record: source blob dc83e62748c93171d89a312e9f7a53c06d97e261 and historical EX4 SHA-256 89821c5b1ae2d7c28a6cad7569cb2ced0e45090d0897451e0f61e0b46eb8944c. It must not be overwritten with Build 5.16 hashes. The confusion came from stale current-state docs and from treating a historical frozen release manifest as the identity of the newer development source. Build 5.16 has not been promoted as a production release.

## Clean pair-specific signal replay

The earlier tester reused a saved MT4 expert profile whose PairList was EURUSD,USDCHF, even though each research adapter defaulted to one symbol. This caused one [P3S1][FAIL] for the non-target symbol on each run. I reran each pair with a unique test-expert name so MT4 could not reuse that stale profile. The run scripts saved and restored the prior HST files, lastparameters.ini, and temporary expert profile after each run.

| Artifact | EURUSD | USDCHF |
|---|---|---|
| Tester expert | BBMA516_RE_D1H4H1_LOCKED_20261122_EURUSD | BBMA516_RE_D1H4H1_LOCKED_20261122_USDCHF |
| Adapter source SHA-256 | 91e034e089c23b36fe799d84a7ce3858e2b988d5b46e99e887e06f414081fd91 | 157133caff7ea9eaaaf3baef5535b90893e6a9a01199bed12af1aabd9f753511 |
| Adapter EX4 SHA-256 | 9c0c6d6e64152415c5bbe418af24685143cec22da67ba05bcb54bdeb735c00a7 | 32b0c3777ee8a7658cbb223da142e5d6b6e045118781b2c93f38d5db83c9b164 |
| Tester log SHA-256 | dc7e7f65ff7bdeb72ceef5a60c70591646d5106e0eee6b4ba304094006a282f3 | f9ed9c8dc0b809db6925b3b5006528ed105eeba65439a494a9b635a421c72193 |
| Init / pair resolution | PASS; no P3S1 failure | PASS; no P3S1 failure |

Both adapters compiled with 0 errors and 0 warnings. They are test harnesses, not production binaries: they set Re-Entry-only mode, a one-pair PairList, signal logging, and an M15 tester timer fallback. Adapter hashes are intentionally distinct from the production-source EX4 hash.

The G40 clean replay reproduces the previous 282 event rows byte-for-byte (CSV SHA-256 34da7e8b9c5857befa887df0f1b331f3afb0273675738311b8c4d8b8f6b42acf; clean summary SHA-256 030cfebcb8c3c3db33189f4ebedb7fe3da0286316a8f98325ecaf02ad7e3ced2). The 282-row event table and clean summary are archived in research/BBMA516_signal_events_clean_20261122.csv and research/BBMA516_signal_event_summary_clean_20261122.json. Approved source events after D1/H4/M15 gating:

| Re-Entry type | EURUSD | USDCHF |
|---|---:|---:|
| Type 1 | 18 | 24 |
| Type 2 | 0 | 0 |
| Type 3 | 18 | 23 |
| Type 4 | 35 | 36 |

No opposite-direction M15 conflict minutes were recorded. These are signal-event counts, not Hedge orders or profitable trades. The tester used M15 Model 2 (open prices only), spread 30, 10,000 USD test deposit, and no live trading. It does not validate tick-level fills or production returns. Because the clean event CSV exactly matches the prior input, the already reported exploratory replay metrics remain unchanged.

## Warm-up evidence

The G40 HST manifest mt4_hst_manifest.json (SHA-256 8bad02296d0374f184acf0221c53075f32b4a9318dc2592f147641e4f75608b7) identifies HFMarketsGlobal-Demo4 bars from 2 Jan 2025 through 18 Nov 2026:

- Per symbol: 11,704 H1 bars, 2,931 H4 bars, 490 D1 bars.
- M15: 46,807 EURUSD bars and 46,805 USDCHF bars.
- The tester logs initialize the target pair and produce D1/H4 owner state at the first evaluation timestamp.

This proves adequate higher-timeframe history for this signal-event replay. It does not establish tick-accurate execution performance.

## The 739.47 USC reconciliation item

739.47 USC is not an unexplained account-balance shortfall. It is the largest residual from an invalid comparison that mixed the unscaled statement ledger with a differently sized replay path. The raw statement contains 1,357 orders totaling 113.43 lots; the scaled path contains 1,356 orders totaling 49.35 lots. On 2 July the scaled close P&L was 132.88 USC while the unscaled balance delta was 872.35 USC, creating the apparent 739.47 USC difference.

After comparing raw statement to raw statement, the remaining in-window residuals are:

- 3 Aug: balance delta +1,150.57 USC, recorded closes +13.17, deposit +1,125.00, residual +12.40 USC.
- 4 Aug: balance delta −14.16 USC with no recorded close P&L or cash flow, residual −14.16 USC.

The 12.40 and 14.16 USC entries are still unexplained and require the original statement/account-history lines or another source record. The scale error is explained; the raw-ledger reconciliation is not fully closed.

The 1,357 captured Tengri order rows have zero recorded commission and zero recorded swap. That describes this export only; it does not verify the broker's current fee schedule or Hedge costs. The replay models Hedge cost as 1 pip per lot/action with a 2-pip stress. It has no actual Hedge fill, commission, swap, rejection, or partial-fill record.

## Production gates still open

1. The installed Hedge EA still uses H4 Mid-BB + ADX(14)>25 + DI and does not consume the BBMA Re-Entry event stream.
2. No account-matched margin calculation, broker stop-out level, or path-dependent hedge-margin release proof has been verified.
3. Actual Hedge commission, swap, slippage, rejected orders, and partial fills remain unverified.
4. The Tengri source/executable-to-frozen-ledger crosswalk and the 12.40/14.16 USC raw balance residual remain open.
5. The Type 1–4 comparison is same-sample historical research, with few Hedge campaigns and open positions. It is not out-of-sample, not a production result, and not authority to change or activate either EA.

Next permitted research step: obtain the original missing account-history records and exact account/server symbol-margin settings; keep any strategy comparison offline and do not alter the production Hedge or Tengri EA.
