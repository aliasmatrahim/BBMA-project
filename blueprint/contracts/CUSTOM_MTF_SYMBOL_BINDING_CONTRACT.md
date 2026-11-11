# Custom symbol to PairState binding — candidate Build 5.96

M04 remains the sole owner of broker-symbol state and PairID/Magic allocation. Custom formulas share the canonical PairState pool through an immutable initialization-time index map, not a second detector pool.

- No enabled custom slot: no custom state allocation, and the canonical pool remains unchanged.
- Reuse an existing state only by its exact resolved actual symbol. Preserve its base key, PairID, Magic, lifecycle state and candle watermark. Required broker-spec readiness must already be true.
- For a new actual symbol, stage an append using the existing PairState initializer and the canonical broker-spec checks. GeneratePairID and GenerateMagicNumber remain the only identity allocators. Preflight rejects duplicate resolved names, ID/Magic collisions, invalid identities and a combined pool beyond MAX_PAIRS.
- Do not resolve collisions by choosing a different ID. In particular, exact broker variants which share a canonical PairID must fail closed. Existing canonical identity is preserved when reused, including historical base-name identity.
- Publish the custom index map and new count only after every new state is ready. Failed staging clears the new appended slots and leaves existing states and watermarks intact.
- New custom-only states have canonical dispatch scope false. The existing M27 canonical loop must not admit them solely because a PairState now exists. Canonical states retain their scope when reused. Future custom owner scheduling and M15 arbitration are separate tasks.

The mapping and broker readiness are engineering state; neither grants signal or execution authority. Owner availability remains closed in this milestone. Arbitrary symbols which collide are unavailable rather than renumbered. Changes to PairList/base aliases can change a reused historical identity: persistence/owned-position reconciliation must pin or reject identity drift before activation. This checkpoint does not establish live reinit, retention of removed symbols with open positions, broker execution on multiple symbols, or seven-TF owner support. Symbol-key consistency across downstream decision/order recovery consumers remains an acceptance requirement.

Native binding tests rename the real EA callbacks and do not invoke its controller. Successful multi-state assertions use explicitly labeled broker-I/O fixtures; the real API case separately verifies that unavailable non-chart broker specifications are rejected and staging is rolled back. No valid broker spec is fabricated in production code. A separate native scope harness exercises the actual M27 dispatch loop with counters below its routing boundary.
