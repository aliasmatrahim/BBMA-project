# Custom MTF v1 — direction alias authority gate

Status: SOURCE CONFLICT / NOT EXECUTABLE for CSA/CSAK mapping.

Live recovery 2026-11-08: custom branch head 1b3349c141e42859130b0e18d06bd09189b57c63; PR #303 remains the custom workstream. Parser 30/30 and slot validator 11/11 native milestones remain reusable. No source patch applied in this recovery.

## Confirmed mismatch
`blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md` and accepted Core section 7 define eCSD through MA5/MA10 crossings and CSD through MA5/MA10 plus Mid BB. User correction defines CSA via Mid BB crossing and CSAK via Mid BB plus relevant MA High/Low crossings. CSA therefore cannot silently alias to legacy eCSD; these are different predicates. Searches in routed current references/decisions did not locate an accepted CSA alias reconciliation; a negative search alone is not proof no evidence exists.

## Boundary
Approved product design requires all signal meanings remain canonical and explicitly flags CSA/CSAK mapping as verification required. Syntax recognition is not semantic acceptance. No raw M10 signal gains direct execution authority. Pending PR #301 EntryCandle scope remains independent and unmerged.

## Decision needed
Approve a scoped accepted-Core reconciliation that promotes the user's corrected CSA/CSAK meanings, after materially relevant routed evidence is checked, and defines legacy eCSD/CSD compatibility rather than relabeling existing predicates. Do not overwrite locked contracts merely to fit custom syntax. Context/trigger maturity and execution admission remain separate from this definition.

## Remaining work
T02 input integration/config hash and init regression; T03-T12. Unaffected helpers remain valid, but full all-signal feature acceptance cannot be claimed while this mapping is unresolved. No merge, trading activation or release readiness claim.
