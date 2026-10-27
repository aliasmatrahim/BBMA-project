# CORE-FIDELITY-292 — CP21 nested typed-field inventory

Date: 2026-10-27. Phase: STATIC DIRECT-FIELD INVENTORY; INTERPROCEDURAL OWNERSHIP / RUNTIME PARTIAL.
Branch: audit/core-fidelity-20261021. Parent checkpoint: CP20 at a1d27c9a6a03cc88662946adc9312615b2bc83e0.
Owner baseline: d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de, Build 5.15.
Source: blueprint/source/BBMA_EA.mq4, blob 09de8b80fdaeeb2fd614de0a1826134e9a8b2411.
PR #293 remains open, draft, unmerged and DO NOT MERGE.

## Verified live graph state

- PR #295 is merged at main commit 22b2e539a82eea768c53bd2a905dd958b6072324.
- The PR head a9e10ae474707f9de79bb7eb14b29f6f5f951a81 passed the deterministic-tooling check.
- The accepted root graph authority remains pinned to d1-owner-dev@23def0919386263007ead1898b94637cc17f7f36. Its accepted module schema is preserved.
- The separate current_owner_source_overlay and config/bbma_field_access_inventory_build515.json are pinned to the exact Build 5.15 owner source blob above. The overlay carries M11J in addition to the 28-module accepted root graph.

## Static source inventory

The exact source snapshot records 29 module headers (M01–M27, plus M11J and M12N), 431 function definitions, 1,478 function-call occurrences, 502 cross-module call occurrences, 96 module edges and 364 distinct caller/callee function pairs. The typed inventory contains 36 structs, 640 declared fields, 595 fields with typed accesses and 338 struct-field pairs observed in more than one module. The scanner reports zero unresolved typed-member occurrences within its typed scope.

Each module row below is [direct reads, direct writes, nested traversals] for typed struct fields. Zero means no direct typed struct-field access was detected for that module in this scope; it does not mean the module has no dependency or connection.

| Module | Reads | Writes | Traversals |
|---|---:|---:|---:|
| M01 | 0 | 0 | 0 |
| M02 | 0 | 0 | 0 |
| M03 | 0 | 0 | 0 |
| M04 | 0 | 4 | 0 |
| M05 | 49 | 150 | 80 |
| M06 | 13 | 33 | 0 |
| M07 | 31 | 7 | 0 |
| M08 | 183 | 82 | 0 |
| M09 | 211 | 121 | 0 |
| M10 | 30 | 0 | 0 |
| M11 | 50 | 28 | 19 |
| M11J | 117 | 43 | 5 |
| M12 | 179 | 108 | 0 |
| M12N | 518 | 193 | 62 |
| M13 | 90 | 47 | 19 |
| M14 | 40 | 15 | 24 |
| M15 | 579 | 193 | 60 |
| M16 | 178 | 12 | 0 |
| M17 | 237 | 9 | 2 |
| M18 | 6 | 5 | 1 |
| M19 | 18 | 27 | 0 |
| M20 | 20 | 25 | 0 |
| M21 | 79 | 0 | 0 |
| M22 | 420 | 188 | 82 |
| M23 | 221 | 28 | 15 |
| M24 | 313 | 191 | 169 |
| M25 | 8 | 0 | 6 |
| M26 | 18 | 22 | 0 |
| M27 | 186 | 24 | 48 |

## Representative typed field paths

- PairState.d1_major_trend_owner: direct writes are detected in M11; direct reads are detected in M11, M15 and M16, with nested traversal paths in M05, M11J, M12N and M27.
- PairState.d1_opportunity: direct writes are detected in M11J; direct reads are detected in M11J, M12N, M15 and M16, with nested traversal paths in M05 and M27.
- ReEntryData.State: direct access spans M05, M11J, M12, M12N, M15–M17, M23, M24 and M27; the inventory records direct writes and reads separately.
- ExtremeLifecycleData.Maturity: M08 is the principal lifecycle access path; typed accesses also occur in M05, M09, M11J, M12N, M15–M17, M23, M24 and M27.

These are lexical typed-access paths, not a proof that every access refers to one shared object. The inventory does not resolve every interprocedural by-reference/copy alias, infer all callee mutation at call sites, or prove same-type object identity between functions. No dependency absence is inferred.

## Scope and gates

- CP21 changes documentation and the separate machine-readable static inventory only; it changes no EA/Core source rule or owner branch.
- The deterministic-tooling CI check verifies graph/tooling compatibility, not field-owner semantics or runtime behavior.
- The G40 device is online. No terminal/process, Strategy Tester or broker runtime was inspected or run in CP21. Qualified G40 history remains NOT VERIFIED; Strategy Tester and broker/runtime remain NOT RUN.
- No terminal restart, trading activation or live trade occurred.
- Next scoped action: trace by-reference/copy aliases, call-side mutation and actual object identity for the remaining cross-module field paths. Keep consumer_edges and the full rule-to-runtime denominator PARTIAL until those paths are resolved.
- Q10 Phase L R5 remains the highest-priority global final-acceptance task on its separate frozen Build 5.11 scope.