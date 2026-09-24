# G40 Tier-A Media Semantic Reconciliation — 2026-09-25

Status: **COMPLETE / ACCEPTED CORE DELTA NONE**
Scope: final semantic adjudication of the two media-only Tier-A-priority direct-Oma-labelled candidates that blocked the 2026-09-24 strict G40-wide reconciliation gate.

Parent records:
- `blueprint/audits/G40_STRICT_SOURCE_DISCOVERY_AUDIT_20260924.md`
- `blueprint/audits/G40_SOURCE_RECONCILIATION_REGISTER_20260924.md`
- `blueprint/audits/G40_FINAL_RECONCILIATION_GATE_20260924.md`
- `blueprint/audits/TIER_B_C_ITEM_LEVEL_CLOSURE_20260924.md`

## 1. Authority boundary

These recordings are supplemental instructional evidence. Direct-Oma labelling raises review priority but does not automatically override:
1. the primary operational PDF;
2. accepted Core V2;
3. reconciled Finale evidence;
4. explicit conflict/HOLD decisions.

Small-model ASR is a screening layer. Material or apparently novel wording was rechecked with the local Malaysian large-v3-turbo model. Ambiguous wording is not executable. Visual context is used only where audio alone cannot distinguish a material semantic boundary.

## 2. Exact media evidence

### Momentum — `-nMZUF1Bx0k`
Local audio:
`D:\BBMA_SOURCE_AUDIT_VIDEOS\youtube_priority\P0\08_momentum_oma_ally_-nMZUF1Bx0k\BBMA Basic Signal Momentun - Dijelaskan Oleh Oma Ally [-nMZUF1Bx0k].m4a`

Audio SHA-256:
`A26A4E03265C8A062DA9F0BED52D2BFFAA252BF76D9F59E8F72B61356E71512E`

Full screening transcript:
`TRANSCRIPT_MS_SMALL_V3_COMBINED_20260925.txt`

Transcript SHA-256:
`B082525FA7315EA3817267DB5C49B4B446AAF7A7C33D26BDA968469DD5A1F8AD`

Coverage:
- three 300-second resume-safe chunks;
- 238 timestamped speech segments;
- first speech ~3.14 s;
- last speech ~849.06 s;
- source audio ~853.73 s.

Material large-model recheck:
`large_recheck/W3_MOMENTUM_DIRECT_265_320_LARGE.txt`
SHA-256:
`C201B42AB91D17DC5E3349F08077628C526E611B4EB897E7EA2AB745195657C8`

### Personal Meeting Room — `hqzptZ9uRmg`
Local audio:
`D:\BBMA_SOURCE_AUDIT_VIDEOS\youtube_priority\P0\A_hqzptZ9uRmg\Oma Ally BBMA's Personal Meeting Room [hqzptZ9uRmg].m4a`

Audio SHA-256:
`0C92C84C340F3440C4712DFA7F0EFFA5DC0371298F0B7AD01F6B9201E9FD7313`

Full screening transcript:
`TRANSCRIPT_MS_SMALL_V3_COMBINED_20260925.txt`

Transcript SHA-256:
`1B186C834DCA9F78ADC6D88CF76468ECC8066407484243B7FEEC7AA3E53AFF87`

Coverage:
- twenty-five 300-second resume-safe chunks;
- 1,674 timestamped speech segments;
- final speech ~7372 s, consistent with source duration.

Material large-model rechecks:
- `large_recheck/W1_RE_MIDBB_6080_6185_LARGE.txt`
  SHA-256 `D13BBF92F9A9392E9576756B1276D03C1CB6A957726DD657E3F662F01C3AAAFA`
- `large_recheck/W2_MTF_5700_5815_LARGE.txt`
  SHA-256 `2C034BA43C6428211562E25F0F98370184B73373064109DDF720453FA49BE542`
- exact visual section `large_recheck/W1_VISUAL_FF9_6080_6190.mp4`
  SHA-256 `2AC8D4AD9429F43CF3B0DCA8A13CA7E1AE943B2DA58AA22F65FFF19DDD7EB2AB`

Repository audit copies are preserved under `blueprint/audits/evidence/G40_TIERA_MEDIA_20260925/`, including both full screening transcripts, W1/W2/W3 large-model rechecks and selected W1 visual crops. `MEDIA_EVIDENCE_MANIFEST.json` binds the repo copies to the exact G40 source media hashes and records which originals remain local-only.

## 3. Momentum semantic disposition

### M-A — Re-Entry / Momentum lifecycle
Stable recovered wording repeatedly ties valid Re-Entry to subsequent Momentum/continuation and warns that missing Momentum may lead to rotation/reversal.

Classification: **CORROBORATION_ONLY**.

Reason:
- already covered by the canonical `Arah -> Re-Entry -> Momentum -> Re-Entry` lifecycle;
- Home Course/F7 evidence already owns the post-Re-Entry no-Momentum lifecycle discussion;
- no new detector, entry owner or lifecycle transition is required.

### M-B — first Re-Entry validation / following candle
Recovered wording is consistent with waiting for the validating Re-Entry candle to close and using the immediately following candle.

Classification: **CORROBORATION_ONLY**.

Reason:
- already closed by Core V2 §8.6 / Finale CF-05;
- no extra candle delay or alternate clock is authorized.

### M-C — nested lower-timeframe support
Recovered wording uses smaller timeframes to expose/refine same-direction structures.

Classification: **CORROBORATION_ONLY / BOUNDED MTF**.

Guard:
- no lower timeframe becomes a second processing clock;
- no M5/M1 independent create/reject/rank/execute authority;
- current owner/lineage contracts remain unchanged.

### M-D — news-specific Momentum next-candle shortcut
Large recheck ~267–311 s confirms a specific teaching example:
- trending market;
- large-news event;
- Momentum candle;
- wait for that candle to close;
- enter on the next candle when lower timeframe aligns.

Cross-source reconciliation:
- this family is already present in the authenticated Home Course atomic ledger as HC-P16-006 `[N]`, HC-P16-007 `[N/H]`, HC-P16-008 `[N]`, HC-P16-009 `[N]`, HC-P16-010 `[N]`, HC-P16-011 `[N]`;
- ledger legend defines `N = NON_CORE`;
- project scope also prohibits adding news/session strategy authority without explicit authorization.

Classification: **NON_CORE / HOLD-NON-EXECUTABLE**.

Effect:
- no news filter;
- no direct Momentum execution path;
- no second-candle news rule in EA;
- accepted Core delta NONE.

## 4. Personal Meeting Room semantic disposition

### PM-A — recursive multi-timeframe structure
The full screening transcript repeatedly describes higher/lower timeframe structure, same-cycle repetition, and lower-timeframe completion/refinement of higher-timeframe context.

Classification: **CORROBORATION_ONLY / BOUNDED MTF**.

It supports the existing recursive-MTF principle but does not authorize unrestricted recursion or child-to-parent state synthesis.

### PM-B — H4 two-Momentum-candle example
Large recheck W2 explicitly says that the shown H4 example has two Momentum candles while looking for Re-Entry.

Classification: **EXAMPLE-SPECIFIC / NO UNIVERSAL THRESHOLD**.

Reason:
- the recording does not establish a universal rule requiring exactly two Momentum candles;
- no fixed-candle threshold is promoted.

### PM-C — M15/H1 cross-timeframe wording
W2 states in substance that a strong-direction structure on M15 is reflected at H1 in the illustrated cycle.

Classification: **CORROBORATION OF MTF STRUCTURE / HOLD AGAINST DIRECT STATE SYNTHESIS**.

Guard:
- H1 state remains owned by H1 evidence under current contracts;
- M15 does not manufacture an H1 owner/event;
- M15 remains the sole processing clock.

### PM-D — Re-Entry MA5/MA10 vs Mid-BB wording
Large W1 initially appears to say SELL Re-Entry remains valid while price has passed MA5/MA10 High as long as Mid BB is not passed.

Audio/visual adjudication resolves the apparent contradiction:
- the speaker separately defines strong direction by a candle **closing** past MA5/MA10 and Mid BB;
- for the Re-Entry example the chart shows probing/penetration around the MA5/MA10 area;
- the explanation concludes that the relevant SELL candle must **close below**;
- this is compatible with Finale CF-06 / Core V2 §8.1, which permits penetration but rejects a close clearing the MA5/MA10 cluster against the setup.

Classification: **MATCH / CORROBORATION — NO SOURCE CONFLICT**.

Core impact: NONE.

### PM-E — one/two Momentum candles for swing holding
The meeting discusses one or two Momentum candles and subsequent holding in an advanced/personal swing-management context.

Classification: **CONTEXTUAL / PERSONAL MANAGEMENT / NON-UNIVERSAL**.

No fixed one/two-candle hold rule is created.

### PM-F — “zero-loss zone” and other management wording
Repeated management phrases are not part of the accepted universal Strategy Core.

Classification: **NON_CORE / CONTEXT ONLY**.

## 5. Content uniqueness

Content-dedup closure is recorded separately in:
`blueprint/audits/G40_CONTENT_DEDUP_CLOSURE_20260925.md`.

Result:
- no strong mirror/re-upload match against reconciled Group-3 + PRIMARY15 + Finale text evidence;
- shared n-grams are consistent with common BBMA vocabulary;
- uniqueness does not imply Core authority.

## 6. Final semantic result

- Momentum: reconciled.
- Personal Meeting Room: reconciled.
- Material ambiguous windows: rechecked with large model.
- W1 potential MA5/MA10 conflict: resolved as compatible penetration-vs-close semantics.
- W2 MTF wording: bounded corroboration; no state-authority expansion.
- W3 news/Momentum shortcut: independently corroborates an already-known Home Course NON_CORE family and remains non-executable.
- No new accepted Strategy-Core rule.
- No accepted source conflict requiring Core modification.
- No EA/runtime change.

**Accepted Core delta: NONE.**

## 7. Safety rule

Any later attempt to activate:
- news-driven Momentum entry;
- fixed two-Momentum-candle gating;
- unrestricted lower-TF add-on execution;
- child-to-parent timeframe state synthesis;
- personal “zero-loss” management;

requires a separate evidence-backed decision. None is authorized by this reconciliation.
