#!/usr/bin/env python3

NONE = "NONE"
PENDING = "MOMENTUM_PENDING"
WAIT = "WAIT_NEXT_REENTRY"
FROZEN = "FROZEN"


def reset(state):
    state.update({
        "managed": False,
        "owner_tf": 0,
        "owner_re": 0,
        "epoch": 0,
        "cursor": 0,
        "lifecycle": NONE,
        "replay_valid": False,
    })


def load_transactional(state, checkpoint_state, replay_ok=True, generation_ok=True):
    state.update({
        "managed": True,
        "owner_tf": 60,
        "owner_re": 100,
        "epoch": 100,
        "cursor": 200,
        "lifecycle": checkpoint_state,
        "replay_valid": False,
    })

    if checkpoint_state == FROZEN:
        return True

    if not replay_ok:
        reset(state)
        return False

    state["replay_valid"] = True
    if not generation_ok:
        reset(state)
        return False
    return True


def main():
    state = {}
    reset(state)
    assert not load_transactional(state, PENDING, replay_ok=False)
    assert state["managed"] is False
    assert state["lifecycle"] == NONE
    assert state["owner_tf"] == 0
    assert state["cursor"] == 0
    assert state["replay_valid"] is False

    reset(state)
    assert not load_transactional(state, WAIT, replay_ok=True, generation_ok=False)
    assert state["managed"] is False
    assert state["lifecycle"] == NONE
    assert state["replay_valid"] is False

    reset(state)
    assert load_transactional(state, PENDING, replay_ok=True, generation_ok=True)
    assert state["managed"] is True
    assert state["lifecycle"] == PENDING
    assert state["replay_valid"] is True

    reset(state)
    assert load_transactional(state, FROZEN, replay_ok=False, generation_ok=False)
    assert state["managed"] is True
    assert state["lifecycle"] == FROZEN
    assert state["replay_valid"] is False

    print("C044_RECOVERY_TRANSACTION_MODEL=PASS")


if __name__ == "__main__":
    main()
