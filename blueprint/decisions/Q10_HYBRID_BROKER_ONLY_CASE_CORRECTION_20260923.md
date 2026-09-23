# Q10 Hybrid Evidence Authority Correction — Broker-Only Cases

Date: 2026-09-23
Issue: #109
Baseline: `d1-owner-dev@f968d758f2ee69c42f7ba6c766b3e03cd7517dea`

## Classification

**ENGINEERING POLICY CORRECTION / NO STRATEGY CHANGE**

The hybrid policy already requires broker/runtime-dependent facts to remain under final MetaQuotes-Demo authority. Two R5 cases were incorrectly left in `historical_required_cases`:

- `R5-14` — broker comment stripped/blank/replaced;
- `R5-16` — broker retryable error occurrence/classification in an actual server interaction.

Strategy Tester and static source inspection can prove local identity precedence and retry classification code, but they cannot prove that a broker server actually strips a comment or emits a particular retryable error.

Therefore both cases move to `live_only_cases`.

This does not weaken final acceptance. It prevents tester/static evidence from being mislabeled as broker evidence.

No EA source, Strategy Core, risk/MM, execution or lifecycle semantic is changed.
