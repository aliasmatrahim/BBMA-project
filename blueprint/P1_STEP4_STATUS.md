# P1 Step 4 — Architecture Invariant Verification

Status: **PARTIAL PASS — ARCHITECTURE/STRUCTURAL VERIFICATION PASS; NATIVE MT4 COMPILE STILL REQUIRED**

## Verified source
Canonical baseline SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

Fully materialized working-source SHA-256:
`e81b91a96d95b4446531b445a54c7d60ee5eb71d91646e98eac15ad8e1001da6`

The Step 4 workflow reconstructed the canonical baseline and materialized the same exact ordered patch chain used by P1 Step 3 before running checks.

## Successful verification
Workflow:
`.github/workflows/p1-step4-architecture-invariants.yml`

GitHub Actions run:
`31951148538`

Job:
`95174679337`

Conclusion: `success`

Passed checks:
- canonical baseline reconstruction and SHA verification;
- deterministic materialization of patches 0001–0025;
- full working-source SHA equality with the P1 Step 3 result;
- M22 executor-only ownership (no lot sizing, risk filter, or portfolio gate inside `ProcessEntry`);
- M27 single preflight ownership and order `M17 -> M21 -> M19 -> M20 -> M22`;
- one preflight delegation from `ProcessPair`;
- tick lifecycle ordering `M20 -> M23 -> emergency gate -> scan`;
- M25 no `PriorityTier` dashboard authority;
- M26 equity-based protection initialization;
- presence of Modules 01–27;
- lexical structural sanity / balanced source braces.

## Native MT4 compilation
Status: **NOT YET VERIFIED**.

The GitHub-hosted Linux runner does not contain MetaTrader 4 MetaEditor, so this workflow intentionally does not claim a real MQL4 compile result. Structural sanity is not a substitute for MetaEditor compilation.

No final MASTER LOCKED SHA may be promoted until the exact materialized source is compiled by a real MT4/MetaEditor compiler and the compile result is captured.

## Next action
P1 Step 5: establish a native MetaEditor compilation path for the exact materialized source, compile without semantic changes, repair compile-only defects if any, then re-run the architecture invariants and decide whether the SHA can be promoted to MASTER LOCKED.

Do not merge `blueprint-dev` into `main` yet.
