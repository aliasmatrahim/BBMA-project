#!/usr/bin/env python3

CP = "D1TPW|"
PAYLOAD = ("D", "X", "LP", "L", "XL", "F", "OT", "MG")


def loadable(store):
    cm = store.get(CP + "CM")
    gen = store.get(CP + "G")
    if cm is None or gen is None or cm <= 0 or gen != cm:
        return False
    return all(CP + key in store for key in PAYLOAD)


def payload(gen, frozen=False, latched=False):
    return {
        CP + "D": 1,
        CP + "X": 100,
        CP + "LP": 200,
        CP + "L": 1 if latched else 0,
        CP + "XL": 200 if latched else 0,
        CP + "F": 1 if frozen else 0,
        CP + "OT": 50,
        CP + "MG": 81001,
        CP + "G": gen,
    }


def committed(gen, frozen=False, latched=False):
    out = payload(gen, frozen, latched)
    out[CP + "GN"] = gen
    out[CP + "CM"] = gen
    return out


def replacement_ops(gen, frozen=False, latched=False):
    p = payload(gen, frozen, latched)
    ops = [("del", CP + "CM", None), ("set", CP + "GN", gen)]
    ops.extend(("set", CP + key, p[CP + key]) for key in PAYLOAD)
    ops.append(("set", CP + "G", gen))
    ops.append(("set", CP + "CM", gen))
    return ops


def apply(store, op):
    action, key, value = op
    if action == "del":
        store.pop(key, None)
    else:
        store[key] = value


def main():
    old = committed(7, frozen=False, latched=False)
    assert loadable(old)

    # Legacy eight-key checkpoint has no commit identity and must fail closed.
    legacy = {key: value for key, value in old.items()
              if not key.endswith(("CM", "G", "GN"))}
    assert not loadable(legacy)

    ops = replacement_ops(8, frozen=True, latched=True)
    for fail_at in range(len(ops)):
        store = dict(old)
        for idx, op in enumerate(ops):
            if idx == fail_at:
                break
            apply(store, op)
        if fail_at == 0:
            # Commit-marker invalidation did not happen: old committed state survives.
            assert loadable(store)
            assert store[CP + "CM"] == 7
        else:
            # Once old CM is invalidated, no partial replacement may load.
            assert not loadable(store), (fail_at, store)

    store = dict(old)
    for op in ops:
        apply(store, op)
    assert loadable(store)
    assert store[CP + "CM"] == 8 == store[CP + "G"]
    assert store[CP + "F"] == 1
    assert store[CP + "L"] == 1 and store[CP + "XL"] == 200

    snapshot = dict(store)
    assert loadable(store) and store == snapshot
    print(f"D1TPW_GENERATION_MODEL=PASS failure_points={len(ops)}")


if __name__ == "__main__":
    main()
