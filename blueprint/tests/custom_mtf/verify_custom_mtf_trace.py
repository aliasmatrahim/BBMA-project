"""Verify normalized offline Custom MTF trace fixtures."""

import argparse
import json
from pathlib import Path


FORMAT = "custom-mtf-fixture-v1"
LIMITATIONS = [
    "Checks normalized offline fixtures only.",
    "Identity expectations are fixture inputs. Native EA logs, broker orders and runtime provenance require a separate binding.",
]


def identifier(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("expected non-empty identifier")
    return value


def timestamp(value):
    if type(value) is not int or value <= 0:
        raise ValueError("expected positive integer timestamp")
    return value


def array(value):
    if not isinstance(value, list):
        raise ValueError("expected array")
    return value


def verify(manifest):
    errors = []
    counts = {"cases": 0, "witnesses": 0, "sends": 0}
    if manifest["format"] != FORMAT:
        raise ValueError("unsupported manifest format")
    for key in ("build", "config"):
        if identifier(manifest["identity"][key]) != identifier(manifest["expected_identity"][key]):
            errors.append("identity_mismatch")
            break

    required = [identifier(case_id) for case_id in array(manifest["required_cases"])]
    if not required or len(set(required)) != len(required):
        raise ValueError("required cases must be non-empty and unique")

    seen = set()
    for case in array(manifest["cases"]):
        case_id = identifier(case["id"])
        if case_id in seen:
            errors.append(f"duplicate_case:{case_id}")
            continue
        seen.add(case_id)
        counts["cases"] += 1
        witnesses = {}
        for witness in array(case["witnesses"]):
            witness_id = identifier(witness["id"])
            if witness_id in witnesses:
                errors.append(f"duplicate_witness:{case_id}")
                continue
            witnesses[witness_id] = (
                identifier(witness["trigger_id"]),
                timestamp(witness["closed_at"]),
            )
        counts["witnesses"] += len(witnesses)

        sends = array(case["sends"])
        counts["sends"] += len(sends)
        expected = case["expected_sends"]
        if type(expected) is not int or expected < 0:
            raise ValueError("expected non-negative send count")
        if len(sends) != expected:
            errors.append(f"send_count:{case_id}")

        sent_triggers = set()
        for send in sends:
            witness_id = identifier(send["witness_id"])
            sent_at = timestamp(send["sent_at"])
            if witness_id not in witnesses:
                errors.append(f"unmatched_witness:{case_id}")
                continue
            trigger_id, closed_at = witnesses[witness_id]
            if sent_at < closed_at:
                errors.append(f"look_ahead:{case_id}")
            if trigger_id in sent_triggers:
                errors.append(f"duplicate_send:{case_id}")
            sent_triggers.add(trigger_id)

    errors.extend(f"missing_case:{case_id}" for case_id in required if case_id not in seen)
    return {"counts": counts, "errors": errors, "limitations": LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.manifest.resolve() == args.output.resolve():
        parser.error("manifest and output must be different files")
    try:
        summary = verify(json.loads(args.manifest.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as error:
        summary = {
            "errors": ["invalid_manifest"],
            "detail": str(error),
            "limitations": LIMITATIONS,
        }
    try:
        args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        parser.exit(1, f"{error}\n")
    return int(bool(summary["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
