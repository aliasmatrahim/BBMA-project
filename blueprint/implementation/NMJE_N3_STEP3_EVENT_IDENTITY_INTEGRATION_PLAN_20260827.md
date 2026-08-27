# NMJE N3 Step 3 — Event Identity Integration + Regression Gates

Date: 2026-08-27
Branch: nmje-n3-hardening-dev
Status: PRE-SOURCE IMPLEMENTATION GATE

## Purpose
Integrate canonical event identity into NMJE without changing BBMA strategy rules and without touching the frozen runtime candidate on d1-owner-dev.

## Mandatory order
1. M08 Extreme canonical identity: pair + TF + direction + RawCandleTime; identity freezes at canonical owner creation and survives maturity transitions.
2. M12 Re-Entry canonical identity: pair + TF + direction + RE type + structural/start anchor; candidate->confirmed advances maturity, not identity.
3. M09 MHV/MLV identity references the canonical M08 parent identity; M09 may not create or mutate Extreme identity.
4. M11 D1 owner epoch identity: direction/state epoch changes only on canonical owner transition.
5. H4 owner identity follows its canonical owner epoch and recovery state.
6. M12N/NMJE stores references to upstream identities; it never manufactures replacement owner identity.
7. M15 consumes NMJE verdict plus identity/provenance only after N3 enforcement gate is explicitly enabled.
8. M16 revalidates the same frozen identity/provenance; no re-detection.
9. M24 recovery reconstructs identical identity from closed-candle/source-owned facts or marks UNRESOLVED/fail-closed for new entries.

## Regression gates
- No change to M13/M14 exact REM/RRE/REE signatures.
- CANDIDATE Re-Entry cannot become executable through NMJE.
- RAW Extreme cannot become executable through NMJE.
- Retired/superseded identity cannot resurrect.
- Restart replay yields identical identity and relation verdict, otherwise UNRESOLVED.
- M08 remains sole writer of Extreme lifecycle.
- M12 remains sole writer of canonical Re-Entry lifecycle.
- M15/M16 remain final entry/revalidation authorities.
- M22 remains sole OrderSend execution owner.
- No score, weighted voting, AI filter, universal perfect-nesting requirement, session/news/correlation/volatility rule is introduced.

## Runtime isolation
Do not merge this branch into d1-owner-dev until the current runtime evidence is preserved and the hardening branch passes static/native compile + replay/regression gates.

## Next executable step
Implement the identity fields/helpers in source on this branch in small owner-scoped commits, starting with M08 and M12. If repository tooling cannot safely replace the monolithic source without a full-content round trip, stop at this gate rather than risk truncating BBMA_EA.mq4; use a source-safe patch/PR workflow next.
