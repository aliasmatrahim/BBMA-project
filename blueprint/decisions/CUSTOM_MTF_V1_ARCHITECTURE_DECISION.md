# CUSTOM MTF V1 — scoped architecture decision

User approved design v1 on 2026-11-08 and instructed continuation inline. Issue #302.

Approved product scope: seven TF, five slots/seven atoms, Context AND Trigger with OR groups, auto-entry, three exit profiles, fixed lot/risk percent, per-slot symbols/limits, hedging option, read-only labels.

Clock exception applies only to the future CUSTOM path; Module M15 remains final authority and canonical cadence/signatures remain unchanged. M12N gains no authority. No executable exception is activated by this documentation commit.

Do not change accepted detector semantics to fit aliases. CSA/CSAK mapping remains VERIFICATION REQUIRED against the current source chain and open audit work. MOM maps conceptually to M10 CSM, but custom trigger availability needs a new approved eligibility adapter, not a direct call to OrderSend.

PR #301 EntryCandle and #299 MHV range fix remain independent Draft changes; preserve their provenance and re-evaluate integration before full acceptance. Do not merge them under this feature authorization. Shadow/research PR #282 must not grant N3 authority here.

Native compiler located; exact isolated native harness/runner binding is not yet established. T01 partial; T02 implementation not started.
