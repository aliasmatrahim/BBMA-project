# Keputusan Replay Diagnostik — Tiga Calon Hedge Tengri — 2026-11-23

## Ringkasan

Replay diagnostik pembetulan selesai untuk EURUSD dan USDCHF, 2026-05-01 hingga 2026-11-18. Ketiga-tiga calon berkongsi sizing, kos, spread gate, safety close dan exit-to-BE. Gate Hybrid kini dinilai pada candle pecah H4 sebelum retest H1; 123 setup H4 yang gagal gate direkod sebagai sekatan. Run awal yang memeriksa gate pada retest H1 telah digantikan oleh keputusan ini.

**Tiada P&L, expectancy, profit factor, drawdown akaun atau dakwaan keselamatan margin dilaporkan.**

## Hasil signal dan tindakan

| Calon | Signal entry/retest | Diterima | Sekatan utama | Hedge dibuka | Re-entry | Hedge ditutup |
|---|---:|---:|---|---:|---:|---|
| Structure-only | 78 | 9 | layer <7: 48; bukan adverse: 15; tiada exposure: 6 | 9 | 7 | 8 BE floor; 1 Tengri safety |
| Indicator-only | 210 | 6 | ADX/DI: 186; layer <7: 10; bukan adverse: 6; tiada exposure: 2 | 4 | 2 | 4 BE floor |
| Hybrid | 18 | 7 | **123 setup H4 ditolak ADX/DI**; selepas retest: layer <7: 9; bukan adverse: 2 | 7 | 5 | 6 BE floor; 1 Tengri safety |

Signal exit yang diterima ketika hedge aktif: **2 Structure-only, 0 Indicator-only, 2 Hybrid**. Tiada hedge ditutup oleh signal exit strategi dalam replay ini; semua penutupan sebenar berlaku melalui lantai breakeven atau safety close Tengri. Maka exit H1 swing dan H1 Mid-BB belum menunjukkan penutupan trade dalam sampel ini.

## Contoh masa entry/exit

Semua masa UTC. Log penuh menyenaraikan setiap signal, sekatan, layer dan kitaran re-entry.

| Calon | Simbol/layer | Tengri net lot → hedge lot | Entry | Exit |
|---|---|---|---|---|
| Structure-only | EURUSD / 7 | 0.47 → 0.11 | 2026-05-19 22:00:00.208 | 2026-05-20 04:12:53.091 — BE floor |
| Indicator-only | EURUSD / 8 | 0.76 → 0.38 | 2026-05-21 08:00:00.368 | 2026-05-21 08:48:43.126 — BE floor |
| Hybrid | EURUSD / 7 | 0.47 → 0.11 | 2026-05-19 22:00:00.208 | 2026-05-20 04:12:53.091 — BE floor |

## Polisi bersama

- Entry layak dari layer Tengri 7; sizing relatif kepada net lot Tengri: 25% pada layer 7, 50% pada 8, 75% pada 9, dan 100% pada 10+. Lot dibundarkan ke bawah pada step 0.01.
- Maksimum spread fill 3 pip; kos tetap satu pip bagi setiap tindakan.
- Signal exit menunggu BE bersih jika hedge masih rugi. Lantai BE menutup selepas net hedge pernah mencapai +1 unit kajian dan kembali ke BE.
- Safety close apabila Tengri flat atau arah net exposure bertukar. Re-entry memerlukan signal adverse baharu.

## Kualiti data dan batas

- Data datang daripada fail tick tempatan `.npz` serta ledger/snapshot Tengri. Identiti server/broker MT4 HFM tidak terkandung atau belum disahkan.
- Warm-up 15 hari kalendar dicuba; fail tick tersedia hanya untuk **29 April** bagi setiap pair: EURUSD 82,684 tick dan USDCHF 45,776 tick. Warm-up penuh tidak dibuktikan.
- Jurang warm-up boleh menjejaskan signal awal; sampel juga bukan holdout bebas.
- Jurang rekonsiliasi ledger terdahulu belum ditutup. Komisen, swap, margin, stop-out dan fill gagal sebenar broker kekal belum disahkan.

## Fail

- Runner: `research/tengri_hedge_three_strategy_diagnostic_20261123.py`
- Log ringkas tindakan: `research/tengri_hedge_three_strategy_action_log_20261123.csv`
- Jejak penuh signal/sekatan: `research/tengri_hedge_three_strategy_full_trace_20261123.csv`
- Lock metodologi: `research/TENGRI_HEDGE_THREE_STRATEGY_DIAGNOSTIC_LOCK_20261123.md`
