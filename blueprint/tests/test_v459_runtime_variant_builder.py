#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
TOOLS = REPO / "blueprint" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import v459_runtime_variant_builder as tool


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        outputs = {}
        for profile in ("baseline", "r1-d1tpw", "r2-c044"):
            out = root / f"{profile}.mq4"
            meta = root / f"{profile}.json"
            record = tool.build(REPO, profile, out, meta)
            outputs[profile] = out.read_text(encoding="utf-8")
            loaded = json.loads(meta.read_text(encoding="utf-8"))
            assert loaded == record
            assert record["canonical_blob"] == tool.EXPECTED_BLOB
            assert record["canonical_sha256"] == tool.EXPECTED_SHA256

        canonical = (REPO / "blueprint" / "source" / "BBMA_EA.mq4").read_text(encoding="utf-8")
        assert outputs["baseline"] == canonical
        assert outputs["r1-d1tpw"].count(tool.D1_GATE_ON) == 1
        assert outputs["r1-d1tpw"].count(tool.C044_GATE_ON) == 0
        assert outputs["r2-c044"].count(tool.C044_GATE_ON) == 1
        assert outputs["r2-c044"].count(tool.D1_GATE_ON) == 0
        assert outputs["r1-d1tpw"].replace(tool.D1_GATE_ON, tool.D1_GATE_OFF, 1) == canonical
        assert outputs["r2-c044"].replace(tool.C044_GATE_ON, tool.C044_GATE_OFF, 1) == canonical

        # Fail-closed proof: a baseline gate drift must be rejected even though
        # the rest of the source is byte-for-byte identical.
        bad = root / "badrepo"
        src = bad / "blueprint" / "source"
        src.mkdir(parents=True)
        drifted = canonical.replace(tool.D1_GATE_OFF, tool.D1_GATE_ON, 1)
        (src / "BBMA_EA.mq4").write_text(drifted, encoding="utf-8")
        subprocess.check_call(["git", "init", "-q", str(bad)])
        rejected = False
        try:
            tool.build(bad, "baseline", root / "bad.mq4", root / "bad.json")
        except ValueError:
            rejected = True
        assert rejected, "drifted canonical gate was not rejected"

    print("V459_RUNTIME_VARIANT_BUILDER_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
