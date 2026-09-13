from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any, Iterable

TRACE_KEYS = (
    "event_type",
    "state",
    "journey_id",
    "decision_id",
    "symbol",
    "direction",
    "reason",
)

def normalize_trace(records: Iterable[dict[str, Any]], keys: Iterable[str] = TRACE_KEYS) -> list[dict[str, str]]:
    key_list = list(keys)
    normalized = []
    for record in records:
        row = {}
        lowered = {str(k).lower(): v for k, v in record.items()}
        for key in key_list:
            value = lowered.get(key.lower(), "")
            row[key] = "" if value is None else str(value)
        normalized.append(row)
    return normalized

def compare_traces(expected: Iterable[dict[str, Any]], actual: Iterable[dict[str, Any]]) -> dict[str, Any]:
    left = normalize_trace(expected)
    right = normalize_trace(actual)
    if left == right:
        return {"classification": "NO_DELTA", "first_mismatch": None, "expected_len": len(left), "actual_len": len(right)}
    limit = min(len(left), len(right))
    mismatch = None
    for idx in range(limit):
        if left[idx] != right[idx]:
            mismatch = {"index": idx, "expected": left[idx], "actual": right[idx]}
            break
    if mismatch is None:
        mismatch = {
            "index": limit,
            "expected": left[limit] if len(left) > limit else None,
            "actual": right[limit] if len(right) > limit else None,
        }
    return {
        "classification": "UNEXPECTED_DELTA",
        "first_mismatch": mismatch,
        "expected_len": len(left),
        "actual_len": len(right),
    }

def classify_build_delta(
    baseline: Iterable[dict[str, Any]],
    candidate: Iterable[dict[str, Any]],
    *,
    authorized_delta: bool = False,
) -> dict[str, Any]:
    result = compare_traces(baseline, candidate)
    if result["classification"] == "NO_DELTA":
        return result
    result["classification"] = "EXPECTED_DELTA" if authorized_delta else "UNEXPECTED_DELTA"
    return result

@dataclass
class ShadowComparison:
    authoritative: list[dict[str, str]]
    shadow: list[dict[str, str]]
    result: dict[str, Any]

def compare_shadow(
    authoritative: Iterable[dict[str, Any]],
    shadow: Iterable[dict[str, Any]],
) -> ShadowComparison:
    left = normalize_trace(authoritative)
    right = normalize_trace(shadow)
    return ShadowComparison(left, right, compare_traces(left, right))

LIFECYCLE_STATES = (
    "NONE",
    "CANDIDATE",
    "CONFIRMED",
    "SELECTED",
    "VALIDATED",
    "RISK_APPROVED",
    "ENTRY_READY",
    "EXECUTED",
    "VOID",
    "EXPIRED",
    "SUPERSEDED",
)

DEFAULT_TRANSITIONS: dict[str, set[str]] = {
    "NONE": {"CANDIDATE"},
    "CANDIDATE": {"CONFIRMED", "VOID", "EXPIRED", "SUPERSEDED"},
    "CONFIRMED": {"SELECTED", "VOID", "EXPIRED", "SUPERSEDED"},
    "SELECTED": {"VALIDATED", "VOID", "EXPIRED", "SUPERSEDED"},
    "VALIDATED": {"RISK_APPROVED", "VOID", "EXPIRED", "SUPERSEDED"},
    "RISK_APPROVED": {"ENTRY_READY", "VOID", "EXPIRED", "SUPERSEDED"},
    "ENTRY_READY": {"EXECUTED", "VOID", "EXPIRED", "SUPERSEDED"},
    "EXECUTED": set(),
    "VOID": set(),
    "EXPIRED": set(),
    "SUPERSEDED": set(),
}

TERMINAL_STATES = {"EXECUTED", "VOID", "EXPIRED", "SUPERSEDED"}

class LifecycleModel:
    """Engineering lifecycle separation model; this is not a BBMA signal rule."""

    def __init__(self, transitions: dict[str, set[str]] | None = None):
        source = transitions if transitions is not None else DEFAULT_TRANSITIONS
        self.transitions = {key: set(values) for key, values in source.items()}
        self.state = "NONE"
        self.history = ["NONE"]

    def allowed(self) -> set[str]:
        return set(self.transitions.get(self.state, set()))

    def transition(self, new_state: str) -> None:
        if new_state not in LIFECYCLE_STATES:
            raise ValueError(f"unknown lifecycle state: {new_state}")
        if new_state not in self.allowed():
            raise ValueError(f"invalid lifecycle transition {self.state} -> {new_state}")
        self.state = new_state
        self.history.append(new_state)

def validate_transition_table(transitions: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for state in LIFECYCLE_STATES:
        if state not in transitions:
            errors.append(f"missing state {state}")
    for terminal in TERMINAL_STATES:
        if transitions.get(terminal):
            errors.append(f"terminal state {terminal} has outgoing transitions")
    forbidden_skips = {
        ("NONE", "CONFIRMED"),
        ("CANDIDATE", "SELECTED"),
        ("CONFIRMED", "VALIDATED"),
        ("SELECTED", "RISK_APPROVED"),
        ("VALIDATED", "ENTRY_READY"),
        ("RISK_APPROVED", "EXECUTED"),
    }
    for src, dst in forbidden_skips:
        if dst in transitions.get(src, set()):
            errors.append(f"forbidden skip {src}->{dst}")
    return errors

def randomized_lifecycle_check(seed: int = 1, iterations: int = 500) -> dict[str, int]:
    rng = Random(seed)
    valid_attempts = 0
    invalid_attempts = 0
    for _ in range(iterations):
        model = LifecycleModel()
        for _step in range(20):
            options = list(model.allowed())
            choose_valid = bool(options) and rng.random() < 0.65
            if choose_valid:
                target = rng.choice(options)
                model.transition(target)
                valid_attempts += 1
                if target in TERMINAL_STATES:
                    break
            else:
                invalid = [state for state in LIFECYCLE_STATES if state not in model.allowed()]
                target = rng.choice(invalid)
                try:
                    model.transition(target)
                except ValueError:
                    invalid_attempts += 1
                else:
                    raise AssertionError(f"invalid transition unexpectedly accepted: {model.history[-2]}->{target}")
    return {"valid_attempts": valid_attempts, "invalid_attempts": invalid_attempts}

def mutation_self_test() -> bool:
    mutated = {key: set(values) for key, values in DEFAULT_TRANSITIONS.items()}
    mutated["CANDIDATE"].add("SELECTED")
    errors = validate_transition_table(mutated)
    return any("CANDIDATE->SELECTED" in item for item in errors)
