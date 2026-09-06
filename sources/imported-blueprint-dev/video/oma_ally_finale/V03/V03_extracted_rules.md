# V03 — Extracted BBMA Core Rules

## Scope
Source: `V03_corrected.srt`. BBMA Strategy Core only.

## Rules

### OA-F-V03-001 — Candle momentum and candle direction are distinct
- **Timestamp:** 00:12:22–00:12:40; 00:16:38–00:19:11
- **Source-derived rule:** The class distinguishes candle direction from candle momentum. A candle can provide directional intent while still inside the Bollinger Band; once the relevant outside-BB momentum condition is met, it is treated as momentum rather than merely an early direction candle.
- **Assessment:** CLARIFY
- **Core impact:** Prevents eCSD/CSD/direction signals from being conflated with CSM/momentum.
- **Confidence:** HIGH

### OA-F-V03-002 — MA5/MA10 are key directional break references
- **Timestamp:** 00:26:15–00:30:20
- **Source-derived rule:** Candle direction is taught around a candle breaking/closing past the relevant MA5/MA10 High or Low pair.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Corroborates current direction detector mechanics.
- **Confidence:** HIGH

### OA-F-V03-003 — Early direction is an initial momentum/direction signal inside BB
- **Timestamp:** 00:27:20–00:27:49
- **Source-derived rule:** The first candle that breaks the relevant MA5/MA10 pair is described as candle direction / early momentum, before a full outside-BB momentum condition.
- **Assessment:** CLARIFY
- **Core impact:** Supports the early-direction stage preceding stronger confirmation.
- **Confidence:** HIGH

### OA-F-V03-004 — Buy candle direction uses the upper MA pair; sell uses the lower MA pair
- **Timestamp:** 00:26:15–00:30:20
- **Source-derived rule:** The class examples identify buy direction by breaking MA5/MA10 High and sell direction by breaking MA5/MA10 Low.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Important directional polarity check for eCSD/CSD implementation.
- **Confidence:** HIGH

### OA-F-V03-005 — Outside BB plus MA extension strengthens momentum context
- **Timestamp:** 00:13:57–00:15:08
- **Source-derived rule:** Momentum examples are described as stronger where the candle closes outside the Bollinger Band and beyond the relevant MA5 reference.
- **Assessment:** CLARIFY
- **Core impact:** Adds strength/context information, but V02 BB-state rule remains mandatory when deciding whether an outside close is actually momentum.
- **Confidence:** MEDIUM-HIGH

### OA-F-V03-006 — Re-Entry zone is associated with MA5 after direction/momentum
- **Timestamp:** 00:23:48–00:24:49
- **Source-derived rule:** MA5 is repeatedly framed as an entry/retest zone after direction/momentum develops.
- **Assessment:** KEEP / CLARIFY
- **Core impact:** Corroborates Re-Entry at MA5/MA5-10 zone.
- **Confidence:** HIGH

## V03 decisions
- **Accepted:** Distinction between direction and momentum, MA-pair polarity, MA5 Re-Entry context.
- **Deferred to V05:** Exact “early” versus “strong” candle-direction definition involving Mid BB is clearer in V05 and should be sourced there in the master contract.
