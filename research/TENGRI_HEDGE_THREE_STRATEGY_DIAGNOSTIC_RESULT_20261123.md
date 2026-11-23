# Keputusan Replay Diagnostik — Tiga Calon Hedge Tengri — 2026-11-23

## Ringkasan

Replay selesai untuk EURUSD dan USDCHF, 2026-05-01 hingga 2026-11-18. Ketiga-tiga calon berkongsi sizing, kos, spread gate, safety close dan exit-to-BE yang sama. Log penuh menyimpan signal entry/exit, sekatan, tindakan hedge, masa, lot/layer Tengri dan re-entry.

**Ini replay diagnostik sahaja.** Tiada P&L, expectancy, profit factor, drawdown akaun atau dakwaan keselamatan margin dilaporkan.

## Hasil signal dan tindakan

| Calon | Signal entry | Diterima | Disekat | Hedge dibuka | Re-entry | Hedge ditutup |
|---|---:|---:|---|---:|---:|---|
| Structure-only | 78 | 9 | layer <7: 48; bukan adverse: 15; Tengri tiada exposure: 6 | 9 | 7 | 8 BE floor; 1 Tengri safety |
| Indicator-only | 210 | 6 | ADX/DI: 186; layer <7: 10; bukan adverse: 6; Tengri tiada exposure: 2 | 4 | 2 | 4 BE floor |
| Hybrid | 78 | 7 | ADX/DI di retest: 60; layer <7: 9; bukan adverse: 2 | 7 | 5 | 6 BE floor; 1 Tengri safety |

Signal exit yang sampai ketika hedge masih aktif: **2 Structure-only, 0 Indicator-only, 2 Hybrid**. Tiada hedge ditutup oleh signal exit strategi dalam replay ini; semua penutupan sebenar berlaku melalui lantai breakeven atau safety close Tengri. Jadi ujian ini belum membuktikan kelebihan exit H1 swing atau Mid-BB.

## Contoh masa entry/exit

Semua masa UTC. Butiran semua kitaran ada dalam CSV.

| Calon | Simbol/layer | Tengri net lot → hedge lot | Entry | Exit |
|---|---|---|---|---|
| Structure-only | EURUSD / 7 | 0.47 → 0.11 | 2026-05-19 22:00:00.208 | 2026-05-20 04:12:53.091 — BE floor |
| Indicator-only | EURUSD / 8 | 0.76 → 0.38 | 2026-05-21 08:00:00.368 | 2026-05-21 08:48:43.126 — BE floor |
| Hybrid | EURUSD / 7 | 0.47 → 0.11 | 2026-05-19 22:00:00.208 | 2026-05-20 04:12:53.091 — BE floor |

## Polisi bersama yang digunakan

- Hedge layak bermula pada layer Tengri 7. Sasaran lot: 25% layer 7, 50% layer 8, 75% layer 9, 100% layer 10+, ikut net lot Tengri dan dibundarkan ke bawah 0.01.
- Maksimum spread untuk fill 3 pip; kos tetap satu pip setiap tindakan.
- Exit signal menunggu breakeven bersih jika hedge masih rugi; lantai BE tutup selepas keuntungan bersih pernah mencapai satu unit kajian dan kembali ke BE.
- Tutup atas safety apabila Tengri flat atau arah net exposure bertukar. Re-entry hanya pada signal adverse baharu.

## Kualiti data dan batas

- Loader menggunakan fail tick tempatan `.npz` bersama ledger Tengri/snapshot; identiti server/broker MT4 HFM tidak terkandung atau belum disahkan.
- Warm-up 15 hari kalendar dicuba. Fail tick tersedia hanya untuk **29 April** bagi kedua-dua pair (EURUSD 82,684 tick; USDCHF 45,776 tick). Warm-up penuh tidak dibuktikan.
- Oleh itu, signal awal boleh terjejas cold-start/jurang data. Keputusan ini bukan holdout bebas dan bukan ukuran production.
- Jurang rekonsiliasi ledger terdahulu masih belum ditutup. Margin, stop-out, komisen/swap broker dan fill gagal kekal tidak disahkan.

## Fail

- Runner: `research/tengri_hedge_three_strategy_diagnostic_20261123.py`
- Log tindakan: `research/tengri_hedge_three_strategy_action_log_20261123.csv`
- Lock metodologi: `research/TENGRI_HEDGE_THREE_STRATEGY_DIAGNOSTIC_LOCK_20261123.md`
