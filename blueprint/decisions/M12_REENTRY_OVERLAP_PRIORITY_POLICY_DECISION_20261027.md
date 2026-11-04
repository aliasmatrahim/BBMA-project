# M12 Re-Entry Type 2/3/4 Overlap Priority — Project Decision

Date: 2026-10-27  
Issue: #292  
Branch: audit/core-fidelity-20261021  
Status: **APPROVED PROJECT POLICY — NOT A SOURCE-DERIVED BBMA RULE**

## Source finding

CP15 inspected supplied primary PDF pages 9–10 in extracted and rendered form. The PDF SHA-256, 3e6065dd97c20951bd8af96bc81b81ca138800184be6fc4740a32aa4ab0a9c9c, matches SOURCE_INDEX. The primary PDF defines Types 2, 3 and 4 separately but states no overlap priority, tie-break or mutual-exclusion rule. Reviewed Core V2, Finale and indexed forum material add no such priority. Static review does not establish that the predicates have overlapped in market data.

## Decision

The requester approved preserving the current deterministic M12 empty-owner order:

**Type 3 → Type 4 → Type 2 → Type 1 fallback**

The first matching specific Type 3, Type 4 or Type 2 precursor starts the direction/timeframe owner. Type 1 remains the fallback when none of those specific precursors starts. This policy applies only when that M12 direction/timeframe owner is empty.

This is a project implementation policy for deterministic continuity. It must not be attributed to Oma Ally, the primary PDF, accepted Core V2, Finale or forum sources.

## Boundaries

- No claim is made that Type 2/3/4 predicates are mutually exclusive or that an overlap has occurred.
- Type detectors, source classification, confirmed-owner lifetime and reset rules, close-side validity, higher-timeframe eligibility, M15/M16 authority, risk and execution are unchanged.
- Existing Build 5.15 owner code already follows this sequence; no EA code change is required for this documentation decision.
- The decision does not amend or promote the order into BBMA Strategy Core.

## Result

The M12 project-policy gate recorded in CP15 is closed. Core §9 may proceed to its next static audit. Qualified G40 history remains NOT VERIFIED and Strategy Tester remains NOT RUN. PR #293 remains open, draft, unmerged and explicitly DO NOT MERGE.
