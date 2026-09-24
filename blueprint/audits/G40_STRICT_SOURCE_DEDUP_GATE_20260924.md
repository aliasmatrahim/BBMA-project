# G40 Strict Source Dedup Gate — 2026-09-24

Status: **EXACT-ID DEDUP PASS / NEW-SOURCE QUEUE ISOLATED**
Parent: G40_STRICT_SOURCE_DISCOVERY_AUDIT_20260924.md
Scope: Group-3 + PRIMARY15 + Finale versus unregistered discovery candidates.

## Canonical corpus identity
- Group-3: 48 YouTube-ID keyed videos.
- PRIMARY15: 15 videos; original YouTube IDs verified from each metadata.json.
- FINAL_CORRECTED: 63 videos total.
- Finale: V01-V07 independent archived subtitle corpus with immutable source hashes.

## PRIMARY15 verified IDs
pU9E_ckLtkI, hq44GaNaW4c, dm04snPxet8, _kCE3vd9bPk, 8dCN4zoVrtA,
lN_yPAKHiL4, 7-rc0D_Fqe0, zywjq6rBr0M, jdghjcQwa_4, 4IEAEkTZ2lU,
RU_Zz7mIDDU, W1RCxzpznBA, 6kdBxqFDZEI, XkcNUPb-8Aw, M-G4bItJ4cA.

## Exact-ID result
All 30 discovery candidate IDs in the 2026-09-07 YouTube queue plus aoykkvmzabk were compared against the Group-3 directory IDs and PRIMARY15 metadata IDs.
**Exact VideoID overlap: 0.**
Machine-readable recheck: `blueprint/audits/evidence/G40_EXACT_ID_DEDUP_20260925.json` (`candidate_count=30`, `canonical_final_corrected_count=63`, `overlap_ids=[]`).
Therefore none may be discarded as a Group-3/PRIMARY15 duplicate by ID.

## Semantic/content dedup rule
No candidate is promoted merely because its ID is new.
Before semantic extraction it must still be checked for:
1. mirrored/re-uploaded content;
2. excerpt of an already reconciled Finale/PRIMARY15/Group-3 recording;
3. same speaker/session with different upload ID;
4. derivative explanation of an existing rule;
5. provenance mismatch between title and actual speaker/audio.

## New-source queue
Tier A-candidate: 11 direct-Oma-Ally-labelled recordings.
Tier B-corroboration: 9 Roohi Bin Adnan recordings.
Tier C-discovery: 9 gap-specific derivative recordings.
Additional candidate: aoykkvmzabk missing-chapter/MHV lead.

## Local availability gate
youtube_priority/P0 currently contains seven candidate directories.
Only f0NkEgM2EtQ exposed a readable VTT during strict inspection; the auto-caption is materially noisy.
The remaining candidates must not be represented as extracted/reconciled merely because their directory exists.

## Authority gate
NEW-ID != NEW-RULE.
Title attribution != verified speaker provenance.
Tier B/C cannot independently alter Core.
Any conflict/uncertainty remains HOLD and non-executable.
No EA/Core/runtime behavior is changed by this dedup gate.

## Next processing order
1. Tier A candidates: verify local media/caption/provenance; content-dedup against Finale/PRIMARY15/Group-3.
2. Extract only genuinely novel source windows.
3. Reconcile novel claims against canonical Core and conflict register.
4. Then process Tier B as corroboration.
5. Tier C only for unresolved discovery gaps.
