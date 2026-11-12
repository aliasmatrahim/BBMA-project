"""Check recorded HFM native seed evidence against a frozen expected checkpoint."""

import argparse
import json
from pathlib import Path
import re

from verify_custom_mtf_trace import unique_object

IDENTITY_FIELDS = (
    "source_checkpoint", "build", "server", "symbol", "timeframe",
    "source_sha256", "harness_sha256", "binary_sha256", "archive_sha256",
    "archive_rows", "owner_replay_bars_per_case",
)
LIMITATIONS = [
    "Verifies recorded native manifest fields and log markers against a frozen checkpoint.",
    "Does not rehash original G40 binaries or history files, rerun MT4, or authenticate the owner epoch.",
    "October owner divergence is an expected diagnostic result. Production recovery remains HOLD.",
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def marker_fields(line, marker):
    prefix, separator, payload = line.partition(marker + " ")
    if not separator or "CustomHFMSeedH1Harness GBPUSD,M15:" not in prefix:
        raise ValueError("unexpected native marker")
    pairs = []
    for token in payload.split():
        key, separator, value = token.partition("=")
        if not separator or not key or not value:
            raise ValueError("invalid marker field")
        pairs.append((key, value))
    return unique_object(pairs)


def verify(evidence, expected):
    errors = []
    identity = {field: evidence[field] for field in IDENTITY_FIELDS}
    if identity != expected["identity"]:
        errors.append("identity_mismatch")
    if evidence["cases"] != expected["cases"]:
        errors.append("case_inputs_mismatch")
    if not re.fullmatch(r"Result: 0 errors, 0 warnings, [0-9]+ msec elapsed", evidence["compile"]):
        errors.append("compile_failed")
    if type(evidence["exit"]) is not int or evidence["exit"] != 0:
        errors.append("runtime_failed")

    results = []
    markers = evidence["markers"]
    if not isinstance(markers, list):
        raise ValueError("markers must be an array")
    if len(markers) != 3:
        errors.append("marker_count")
    else:
        results = [marker_fields(line, "[HFM-SEED]") for line in markers[:2]]
        ending = marker_fields(markers[2], "[HFM-SEED-END]")
        if results != expected["results"]:
            errors.append("case_results_mismatch")
        if ending != expected["end"]:
            errors.append("end_result_mismatch")

    return {
        "errors": errors,
        "baseline_commit": expected["baseline_commit"],
        "case_count": len(results),
        "owner_matches": {row["case"]: row["full_exact"] == "true" for row in results},
        "recovery_acceptance": "HOLD",
        "limitations": LIMITATIONS,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in (args.manifest.resolve(), args.expected.resolve()):
        parser.error("output must differ from both input files")
    try:
        result = verify(read_json(args.manifest), read_json(args.expected))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        result = {
            "errors": ["invalid_manifest"],
            "detail": str(error),
            "recovery_acceptance": "HOLD",
            "limitations": LIMITATIONS,
        }
    try:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        parser.exit(1, f"{error}\n")
    return int(bool(result["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
