from copy import deepcopy

LIFECYCLE_KEYS = ["D", "TF", "OR", "EP", "LP", "ST", "XR", "XL", "OT", "MG"]
REPLAY_KEYS = ([f"R{i}" for i in range(20)] +
               [f"B{i}" for i in range(19)] +
               [f"S{i}" for i in range(19)])
CP = "C|"
RP = "C|R|"


def read_state(store, frozen=False):
    cm = store.get(CP + "CM")
    generation = store.get(CP + "G")
    if cm is None or generation is None or cm <= 0 or generation != cm:
        return None
    if any(CP + key not in store for key in LIFECYCLE_KEYS):
        return None
    if not frozen:
        if store.get(RP + "V") != 2 or store.get(RP + "G") != cm:
            return None
        if any(RP + key not in store for key in REPLAY_KEYS):
            return None
    return (cm,
            tuple(store[CP + key] for key in LIFECYCLE_KEYS),
            () if frozen else tuple(store[RP + key] for key in REPLAY_KEYS))


def operation_plan(generation, label, frozen=False):
    ops = [("del", CP + "CM", None)]
    ops += [("del", CP + key, None) for key in LIFECYCLE_KEYS + ["G"]]
    ops += [("del", RP + key, None) for key in ["V", "G"] + REPLAY_KEYS]
    ops += [("set", CP + "GN", generation)]
    if not frozen:
        ops += [("set", RP + "V", 2)]
        ops += [("set", RP + key, f"{label}:{key}") for key in REPLAY_KEYS]
        ops += [("set", RP + "G", generation)]
    ops += [("set", CP + key, f"{label}:{key}") for key in LIFECYCLE_KEYS]
    ops += [("set", CP + "G", generation), ("set", CP + "CM", generation)]
    assert ops[-1][1] == CP + "CM"
    return ops


def apply_op(store, op):
    action, key, value = op
    if action == "del":
        store.pop(key, None)
    else:
        store[key] = value


def apply_ops(store, ops):
    for op in ops:
        apply_op(store, op)


def committed(generation, label, frozen=False):
    store = {}
    apply_ops(store, operation_plan(generation, label, frozen))
    assert read_state(store, frozen) is not None
    return store


def assert_all_torn_prefixes_fail_frozen(frozen=False):
    prior = committed(1, "old", frozen)
    ops = operation_plan(2, "new", frozen)
    assert read_state(prior, frozen)[0] == 1
    for prefix in range(1, len(ops)):
        store = deepcopy(prior)
        apply_ops(store, ops[:prefix])
        assert read_state(store, frozen) is None, ("prefix", frozen, prefix)
    store = deepcopy(prior)
    apply_ops(store, ops)
    recovered = read_state(store, frozen)
    assert recovered is not None and recovered[0] == 2
    assert read_state(store, frozen) == recovered
    return len(ops)


def assert_all_writer_failures_safe(frozen=False):
    prior = committed(1, "old", frozen)
    ops = operation_plan(2, "new", frozen)
    for fail_index in range(len(ops)):
        store = deepcopy(prior)
        for index, op in enumerate(ops):
            if index == fail_index:
                break  # production writer must abort on the first failed GV operation
            apply_op(store, op)

        recovered = read_state(store, frozen)
        if fail_index == 0:
            # Commit-marker invalidation failed before any mutation: retain old generation.
            assert recovered is not None and recovered[0] == 1, (
                "invalidation_failure", frozen, fail_index)
        else:
            # Once the old commit marker was removed, no partial generation may load.
            assert recovered is None, ("write_failure", frozen, fail_index)
    return len(ops)


def main():
    normal_ops = assert_all_torn_prefixes_fail_frozen(False)
    frozen_ops = assert_all_torn_prefixes_fail_frozen(True)
    normal_failures = assert_all_writer_failures_safe(False)
    frozen_failures = assert_all_writer_failures_safe(True)
    print("C044_GENERATION_MODEL=PASS "
          f"normal_ops={normal_ops} frozen_ops={frozen_ops} "
          f"normal_failure_points={normal_failures} "
          f"frozen_failure_points={frozen_failures}")


if __name__ == "__main__":
    main()
