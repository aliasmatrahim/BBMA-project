# V02 — Extracted BBMA Core Rules

## Scope
Source: `V02_corrected.srt`. BBMA Strategy Core only.

## Rules

### OA-F-V02-001 — Bollinger Band has two operational states
- **Timestamp:** 00:13:51–00:16:08
- **Source-derived rule:** When reading a chart, the class explicitly distinguishes an expanding Bollinger Band from a flat/horizontal Bollinger Band.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** BB state is not decorative; it changes how an outside-BB candle is interpreted.
- **Confidence:** HIGH

### OA-F-V02-002 — Momentum requires outside-BB close in an expanding BB context
- **Timestamp:** 00:17:45–00:18:07; 00:24:44–00:25:24
- **Source-derived rule:** The class defines momentum in context as a candle closing outside the Bollinger Band while the Bollinger Band is expanding.
- **Assessment:** CORRECT / CLARIFY
- **Core impact:** A detector that labels every outside-BB close as momentum without considering BB expansion is too broad.
- **Confidence:** HIGH

### OA-F-V02-003 — Outside-BB close during flat BB is explicitly not momentum
- **Timestamp:** 00:25:28–00:25:59
- **Source-derived rule:** During a flat/horizontal BB, the speaker explicitly says a candle may close outside the band but “itu bukan momentum”; a flat BB itself has no momentum.
- **Assessment:** CORRECT
- **Core impact:** This is one of the strongest Finale corrections to a simplistic CSM/momentum rule.
- **Confidence:** VERY HIGH

### OA-F-V02-004 — Flat-BB excursion tends to revert toward the band / Mid BB
- **Timestamp:** 00:26:02–00:26:18; 00:26:32–00:33:08
- **Source-derived rule:** The teaching examples describe outside excursions under a flat BB as tending to return, with Mid BB repeatedly used as a minimum/reference target in the illustrated cases.
- **Assessment:** ADD / CLARIFY
- **Core impact:** Useful BB-state context, but should not be converted into a guaranteed mean-reversion rule.
- **Confidence:** HIGH for the teaching statement; MEDIUM for any universal execution rule.

### OA-F-V02-005 — Do not counter the direction while expansion/momentum persists
- **Timestamp:** 00:21:43–00:22:00
- **Source-derived rule:** In the shown expanding-BB momentum example, the class says not to look for the opposite-direction entry while candles remain outside in the active move.
- **Assessment:** CLARIFY
- **Core impact:** Supports continuation context and invalidation of premature countertrend interpretations.
- **Confidence:** MEDIUM-HIGH; example-driven.

### OA-F-V02-006 — Both Bollinger Band arms carry context
- **Timestamp:** 00:35:49–00:39:25
- **Source-derived rule:** The speaker reads both outer-band shapes; a change/bend in the opposite arm can indicate that current momentum is losing strength or pausing.
- **Assessment:** ADD / UNCERTAIN for hard coding
- **Core impact:** Valuable discretionary context, but the subtitle does not provide a deterministic numeric threshold for automated detection.
- **Confidence:** MEDIUM

### OA-F-V02-007 — Mid BB and MA50 trend framing
- **Timestamp:** 00:47:22–00:53:26
- **Source-derived rule:** Candles above Mid BB are framed broadly as up context and below as down context; MA50 is taught as an important trend/support-resistance reference, with Mid BB + MA50 strengthening context.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Corroborates existing Mid BB / MA50 trend framing.
- **Confidence:** HIGH

## V02 decisions
- **Major accepted correction:** Momentum must be interpreted with BB state; flat-BB outside closes are not automatically momentum.
- **Hold for discretionary-only context:** Fine-grained interpretation of the opposite BB arm until a deterministic source rule is available.
- **Rejected from Core:** Generic anecdotes and claims not tied to a repeatable BBMA condition.
