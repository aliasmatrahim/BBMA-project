#!/usr/bin/env python3
from pathlib import Path
import csv
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_outcome_log_extractor.py"
spec = importlib.util.spec_from_file_location("n2_nmje_outcome_log_extractor", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    log = td_path / "expert.log"
    csv_path = td_path / "outcomes.csv"
    log.write_text(
        "\n".join(
            [
                "[N2-NMJE-OUT] PAIR=EURUSD TICKET=101 DID=D1 DIDH=H1 NET=12.50 CLOSE=1770000000 REC=REC_NORMAL",
                "[N2-NMJE-OUT] PAIR=GBPUSD TICKET=102 DID=- DIDH=H2 NET=-3.25 CLOSE=1770000060 REC=REC_IDENTITY_HASH_ONLY",
                "[N2-NMJE-OUT] PAIR=USDJPY TICKET=103 DID=D3 DIDH=H3 NET=0.00 CLOSE=1770000120 REC=REC_NORMAL",
            ]
        ),
        encoding="utf-8",
    )

    records = mod.parse_logs([log])
    report = mod.analyze(records)
    assert report["record_count"] == 3, report
    assert report["exact_decision_outcomes"] == 2, report
    assert report["hash_only_outcomes"] == 1, report
    assert report["valid_exact_outcomes"] == 2, report
    assert report["duplicate_tickets"] == [], report
    assert report["duplicate_decision_ids"] == [], report
    assert report["hash_only_rows"][0]["decision_hash"] == "H2", report

    mod.write_exact_csv(csv_path, report)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["decision_id"] for r in rows] == ["D1", "D3"], rows
    assert rows[0]["net_profit"] == "12.5", rows

    dup_log = td_path / "dup.log"
    dup_log.write_text(
        "\n".join(
            [
                "[N2-NMJE-OUT] PAIR=EURUSD TICKET=201 DID=DX DIDH=HX NET=1.0 CLOSE=1770000200 REC=REC_NORMAL",
                "[N2-NMJE-OUT] PAIR=EURUSD TICKET=201 DID=DX DIDH=HX NET=1.0 CLOSE=1770000200 REC=REC_NORMAL",
            ]
        ),
        encoding="utf-8",
    )
    dup = mod.analyze(mod.parse_logs([dup_log]))
    assert dup["duplicate_tickets"] == [201], dup
    assert dup["duplicate_decision_ids"] == ["DX"], dup
    assert dup["valid_exact_outcomes"] == 0, dup

print("N2-07 NMJE outcome log extractor synthetic self-test PASS")
