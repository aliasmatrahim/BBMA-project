# Internet direction-evidence review — 2026-11-10

Task C/T04-D; base099de1d6192471e81f6ef42d404a0db389aacf10, branch feat/custom-mtf-v1-20261108. SOURCE_INDEX/Core/locked M10 mapping remain authoritative. No strategy or availability change.

New primary technical source: Marlina, SEMMAU publication record dated2021-12-20, pp177-180, “Notifikasi di Telepon Seluler pada Platform MT4 untuk Indikator BBMA-OA”. Publisher landing: https://publikasi.uyelindo.ac.id/index.php/semmau/article/view/236 ; publisher PDF: https://publikasi.uyelindo.ac.id/index.php/semmau/article/download/236/205/570 . PDF printed page179 supplies explicit numerical CSAK implementation:

| Side | Open relation | Close relations |
|---|---|---|
| BUY | O < Mid | C > Mid, C > MA5High, C > MA10High |
| SELL | O > Mid | C < Mid, C < MA5Low, C < MA10Low |

This is the researcher's implementation, not an authenticated founder rule. It spans MidBB but places no explicit open-side bound on either MA. The paper's MT4/MQL5 terminology is inconsistent; notification examples are not founder-rule validation or trading-profit proof. Do not promote it into executable Core.

This reveals a third engineering interpretation, distinct from both unrestricted close-side and spanning all required lines. Illustration only, not market data: Mid100, MA5High98, MA10High99, O99.5,C101 satisfies the paper formula but fails full-body crossing of every MA. Formula evaluation is reproducible arithmetic; it does not resolve source authority or first-event/continuation classification.

Internet copy of the already registered Tier-B Home Course Workbook, Lesson9/page11: https://id.scribd.com/document/333531988/BBMA-Home-Course . Close beyond MA5/10 and MidBB is corroborated; no explicit numerical open requirement was recovered there. Existing product-linked/strong-provenance ceiling remains; mirror identity/authorship was not independently established by web retrieval.

Other mirror slide decks/blogs largely repeat that wording and are not independent votes. The author-hosted MQL5 OmniView page https://www.mql5.com/en/code/67831 lists CSA/CSAK but does not expose enough formula on its description to decide semantics. Browser download was unsupported octet-stream; direct G40 read-only retrieval returned403. No claim of reading/validating its source code. Public BBMATV channel page fetch was throttled; no new founder-video statement accepted from it.

Ruling: VERIFICATION REQUIRED remains. Keep all-line body-span as the currently locked engineering mapping pending explicit source reconciliation, not as newly proven founder wording. The new MidBB-only-open alternative must be included in the next numerical/source adjudication. No CSA/eCSD alias or independent CSA admission is inferred.

Owner-epoch: internet references cannot authenticate this project's missing historical M08/M09 snapshot. Same-feed/session-bound runtime evidence remains required; this search makes no recovery-status promotion.

Verification: publication metadata and PDF formulas cross-read; illustrative arithmetic checked; source identity unchanged. No EA/test changes and no repeated native compile/regression. Compile/runtime/75-cloud evidence stays historical exact-source proof. Auto-entry/all77 availability OFF; no merge/deployment.

Exact next: reconcile three explicit interpretations against labelled founder/Core evidence, including first-event semantics. Separately acquire a source-proven M08/M09 origin snapshot on authenticated history before restart comparison. Publication SHA is recorded in Draft PR303.
