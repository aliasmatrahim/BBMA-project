# P3-M2-07 Cycle Direction Guard Patch

Status: PATCH APPLIED; NATIVE METAEDITOR 0E0W REQUIRED BEFORE MERGE.

Build identifier: `P3-M2-07 Cycle Direction Guard`.

Behavior: blocks a fresh opposite-direction EA entry when an EA-owned live position already exists on the same pair. Distinct same-direction BBMA add-on decisions remain allowed subject to duplicate, risk, portfolio, and MaxTradePerPair controls. No forced close, scoring, relative-quality ranking, SL/TP change, or BBMA detector change is introduced.
