# D1O-01 — D1 BBMA Opportunity Journey Execution Decision

Date: 2026-08-25  
Status: **APPROVED EXECUTION EXTENSION**

The user explicitly authorized activation of the previously KIV D1 BBMA Opportunity Journey strategy and continuous implementation.

Two authorities remain distinct: the existing MA50-based D1 Strategic Owner and the D1 BBMA Opportunity Journey. Opportunity context is never a direct order trigger; M15 remains sole final new-entry authority and M16 remains fail-closed.

Active families:
- `D1_OPP_EXTREME_TPW`: reversal-confirmed D1 Extreme + still-active TP-Wajib path is one tactical journey. RAW is insufficient. This family may oppose the strategic owner, but requires valid/recovered aligned H4 owner plus fresh confirmed H1 Re-Entry. M15-only is insufficient.
- `D1_OPP_CSD`: confirmed D1 CSD; direction must align with execution-ready strategic owner; fresh confirmed LTF Re-Entry required.
- `D1_OPP_RE_ENTRY`: confirmed D1 Re-Entry; primary/strongest family; direction must align with execution-ready strategic owner; fresh confirmed LTF Re-Entry required.
- `D1_OPP_MOMENTUM_RETRACE`: D1 CSM/Momentum continuation context; never chase; fresh post-activation LTF Re-Entry required; strategic-owner alignment required.

Watch only: D1 MHV/MLV and D1 eCSD. Neither has independent execution authority.

Temporal rule: a D1 opportunity is usable only after its source D1 candle has closed. LTF readiness must occur strictly after activation; no pre-existing LTF setup may be reused via look-ahead.

LTF execution:
- Mode 2 only; Mode 1 preserves previous behavior.
- Confirmed H1 and M15 Re-Entry are the initial executable LTF structures.
- M15 Re-Entry requires aligned recovered H4 owner.
- If H1 and M15 are simultaneously fresh, canonicalize as one opportunity cluster and prefer H1 as structural SL/TP source.
- A later genuinely fresh LTF Re-Entry with a distinct confirmation/sequence identity may create another trade subject to existing caps.

Exact REM/RRE/REE signatures, risk limits and structural M17 SL/TP formula remain unchanged. No score/weighting/voting is introduced.