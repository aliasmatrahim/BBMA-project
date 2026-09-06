# V04 — Extracted BBMA Core Rules

## Scope
Source: `V04_corrected.srt`. BBMA Strategy Core only.

## Rules

### OA-F-V04-001 — Extreme criterion 1: relevant MA5 outside outer BB
- **Timestamp:** 00:27:23–00:28:56
- **Source-derived rule:** First Extreme condition: MA5 extends outside the relevant outer Bollinger Band. Above Top BB corresponds to Extreme sell context; below Lower BB corresponds to Extreme buy context. The speaker explicitly says this first condition alone is not enough to enter.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Confirms raw Extreme condition is not entry eligibility.
- **Confidence:** VERY HIGH

### OA-F-V04-002 — Extreme criterion 2: reversal candle
- **Timestamp:** 00:30:15–00:30:38
- **Source-derived rule:** A reversal candle is required as the second condition.
- **Assessment:** KEEP
- **Core impact:** Corroborates existing reversal confirmation.
- **Confidence:** VERY HIGH

### OA-F-V04-003 — Extreme criterion 3: retest; entry occurs at retest
- **Timestamp:** 00:31:08–00:31:55; 00:40:28–00:40:53
- **Source-derived rule:** A retest is the third condition; all three conditions are required before an Extreme entry. The retest need not be the immediate next candle and can develop over roughly two or three candles in the examples.
- **Assessment:** ADD / CORRECT
- **Core impact:** Current core that validates Extreme at reversal-candle close alone is incomplete for standalone Extreme entry eligibility. Retest lifecycle must exist before Mode 2 can safely include standalone Extreme.
- **Confidence:** VERY HIGH

### OA-F-V04-004 — Reversal candle preferably closes inside BB
- **Timestamp:** 00:31:32–00:31:40
- **Source-derived rule:** The reversal candle is said to preferably be inside the BB.
- **Assessment:** CLARIFY
- **Core impact:** “Preferably” is not equivalent to a universal hard requirement; V05 adds nuance that a reversal candle can sometimes be outside BB but inside MA5.
- **Confidence:** HIGH

### OA-F-V04-005 — Extreme retest reference can be the marked highest/lowest body or MA5
- **Timestamp:** 00:34:56–00:36:18
- **Source-derived rule:** The retest may revisit the marked body/reference line around the Extreme or the relevant MA5 area.
- **Assessment:** ADD / CLARIFY
- **Core impact:** Gives concrete retest targets for lifecycle design.
- **Confidence:** HIGH

### OA-F-V04-006 — Outside-BB close during retest invalidates the Extreme context
- **Timestamp:** 00:37:27–00:38:26; 00:43:20–00:43:29
- **Source-derived rule:** If price starts closing outside the BB during/after the attempted Extreme retest, the class treats it as momentum rather than a valid Extreme continuation and instructs exiting the Extreme position.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Reinforces Extreme invalidation on outside-BB close.
- **Confidence:** VERY HIGH

### OA-F-V04-007 — Normal Extreme TP Wajib levels
- **Timestamp:** 00:41:02–00:42:42
- **Source-derived rule:** For a normal Extreme sell, TP Wajib is around MA5/MA10 Low; for a normal Extreme buy, around MA5/MA10 High. Mid BB is described as a farther/maximum possibility in the teaching examples.
- **Assessment:** CLARIFY / CORRECT if current TP is always Mid BB
- **Core impact:** Current “Extreme TP = Mid BB” is too coarse if used as the only source-derived target. MA5/MA10 opposite-side target is the explicitly mandatory first target in this class.
- **Confidence:** VERY HIGH

### OA-F-V04-008 — Advanced Extreme without TP Wajib is mentioned but not defined
- **Timestamp:** 00:41:49–00:41:56
- **Source-derived rule:** The speaker mentions that some advanced Extreme cases may not have TP Wajib, but does not provide a deterministic standalone definition here.
- **Assessment:** UNCERTAIN / HOLD
- **Core impact:** Do not remove TP Wajib from normal Extreme based on this statement.
- **Confidence:** HIGH that the statement was made; LOW for implementation criteria.

## V04 decisions
- **Major addition:** standalone Extreme entry requires a retest after the reversal condition.
- **Major TP clarification:** mandatory target for normal Extreme is the opposite MA5/MA10 zone first; Mid BB is not automatically the only TP.
- **Hold:** advanced Extreme exceptions until a source-valid deterministic definition exists.
