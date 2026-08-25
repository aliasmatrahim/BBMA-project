#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from d1_runtime_evidence_analyzer import analyze

GOOD_LOG = """
[D1-10A] EURUSD D1=B H4=B F=SIGNAL_RE_ENTRY/DIR_BUY
[D1-10A] GBPUSD D1=S H4=S F=SIGNAL_RE_ENTRY/DIR_SELL
[D1-10A] USDJPY D1=T H4=- F=NONE
[D1-10A] USDCHF D1=U H4=- F=NONE
[D1-OPP] EURUSD F=CSD DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 00:00 CYCLE=C1 R=first
[N2-NMJE-DEC] EURUSD X=1 DIR=B AUTH=OPP OFAM=CSD OC=C1 LTF=H1 OSH=ABC123
[D1-OPP] EURUSD F=RE_ENTRY DIR=B ACTIVE=Y TACT=N SRC=2026.08.24 00:00 ACT=2026.08.25 01:00 CYCLE=C2 R=second
[N2-NMJE-DEC] EURUSD X=2 DIR=B AUTH=OPP OFAM=RE_ENTRY OC=C2 LTF=H1 OSH=ABC123
[P3M2][EXEC] Ticket=1001 Pair=EURUSD DecisionID=DEC1 Signal=SIGNAL_RE_ENTRY Dir=DIR_BUY ValidateCandle=2026.08.25 10:00 OrderOpen=2026.08.25 10:15
""".strip()

BAD_TIMING_LOG = """
[D1-10A] EURUSD D1=B H4=B F=SIGNAL_RE_ENTRY/DIR_BUY
[P3M1][EXEC] Ticket=1002 Pair=EURUSD DecisionID=DEC2 Signal=SIGNAL_RE_ENTRY Dir=DIR_BUY ValidateCandle=2026.08.25 10:15 OrderOpen=2026.08.25 10:00
""".strip()


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = root / "good.log"
        bad = root / "bad.log"
        good.write_text(GOOD_LOG + "\n", encoding="utf-8")
        bad.write_text(BAD_TIMING_LOG + "\n", encoding="utf-8")

        report = analyze([good])
        assert report["d1_owner_matrix"]["all_four_states_observed"] is True
        assert report["d1_owner_matrix"]["state_counts"] == {"B": 1, "S": 1, "T": 1, "U": 1}
        assert report["d1o_canonical_dedup"]["unique_execution_hashes"] == 1
        reuse = report["d1o_canonical_dedup"]["cross_d1_attribution_hash_reuse"]
        assert len(reuse) == 1
        assert reuse[0]["classification"] == "EXPECTED_IF_LTF_IDENTITY_UNCHANGED"
        assert report["d1o_canonical_dedup"]["integrity"]["sequence_hash_direction_conflicts"] == []
        assert report["validation_to_order_timing"]["execution_rows"] == 1
        assert report["validation_to_order_timing"]["strict_before_count"] == 1
        assert report["validation_to_order_timing"]["non_strict_or_reversed"] == []
        assert report["validation_to_order_timing"]["min_delta_seconds"] == 900
        assert report["coverage"]["all_requested_runtime_evidence_observed"] is True

        bad_report = analyze([bad])
        assert bad_report["integrity"]["timing_violation_count"] == 1
        assert bad_report["validation_to_order_timing"]["non_strict_or_reversed"][0]["delta_seconds"] == -900

        # Must remain JSON serializable for artifact/report pipelines.
        json.dumps(report, sort_keys=True)

    print("D1_RUNTIME_EVIDENCE_ANALYZER_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
