# Tiga Calon Entry/Exit Hedge Tengri — Replay Diagnostik — 2026-11-23

## Status dan tujuan

Lock ini dibuat sebelum replay. Bandingkan tiga calon pada sampel dan polisi pelaksanaan yang sama. Output hanya signal, sekatan, masa keputusan, layer Tengri/Hedge dan re-entry. Jangan keluarkan P&L, expectancy, profit factor, drawdown akaun, atau dakwaan keselamatan margin daripada replay ini.

Tengri tidak diubah. Tiada EA atau trading diaktifkan.

## Calon yang dibandingkan

1. **Structure-only**
   - Entry: H4 swing break berasaskan candle tertutup, melawan arah net exposure Tengri; tunggu retest level itu pada H1 dan close sambungan sebelum signal entry.
   - Exit: H1 swing break tertutup ke arah Tengri.

2. **Indicator-only**
   - Entry: peralihan H4 close merentasi Mid-BB(20), dengan ADX(14) > 25 dan DI searah signal, melawan arah net exposure Tengri.
   - Exit: H1 close menyeberang semula Mid-BB(20) ke arah Tengri.

3. **Hybrid**
   - Entry: H4 swing break tertutup melawan net exposure Tengri yang disahkan ADX(14) > 25 dan DI searah; kemudian H1 retest level dan close sambungan.
   - Exit: H1 swing break tertutup ke arah Tengri.

Signal hanya dibaca selepas candle berkaitan ditutup. Semua entry mesti bertentangan dengan arah net Tengri.

## Polisi bersama

- Kelayakan entry bermula pada Tengri layer 7.
- Sasaran lot hedge dikira semula daripada lot net Tengri semasa: 25% pada layer 7, 50% pada layer 8, 75% pada layer 9, 100% pada layer 10+; pembundaran ke bawah pada step 0.01.
- Hedge ditambah/trim mengikut perubahan lot Tengri. Re-entry selepas hedge tutup hanya pada signal adverse baharu.
- Signal exit mula menutup hedge jika basket hedge bersih selepas kos >= 0; jika belum, exit pending sehingga breakeven bersih. Jika keuntungan bersih pernah >= 1 unit kajian lalu kembali ke breakeven, tutup untuk menjaga lantai BE.
- Safety close sama bagi semua calon: tutup hedge apabila Tengri flat atau arah net Tengri bertukar.
- Maksimum spread untuk fill ialah 3 pip; fill menggunakan quote yang tersedia seterusnya. Harga Bid/Ask yang tersedia digunakan; andaian kos tetap satu pip bagi setiap tindakan.
- Kos dan polisi pelaksanaan yang sama digunakan untuk ketiga-tiga calon.

## Sampel dan data

- EURUSD dan USDCHF bersama, 2026-05-01 hingga 2026-11-18.
- Fokus layer 7+; laporkan juga layer 9+ dan 10+.
- Warm-up indikator: cuba 15 hari kalendar sebelum 1 Mei, rekod hari/tick yang tersedia bagi setiap simbol dan flag readiness. Ketiadaan arkib warm-up mesti dilaporkan; jangan isi jurang dengan harga anggaran.
- Input semasa daripada ledger/snapshot dan fail tick tempatan; identiti server/broker MT4 HFM dan kelengkapan warm-up belum disahkan. Rekonsiliasi baki dan residual ledger yang terdahulu juga belum ditutup.
- Oleh itu ini bukan holdout bebas dan bukan ukuran prestasi production.

## Medan log wajib

Masa signal/keputusan (UTC), simbol, calon, jenis signal (entry/exit/safety/BE), arah signal dan net Tengri, layer Tengri, lot net Tengri, lot Hedge sebelum/selepas, status diterima/disekat, sebab sekatan, sebab exit, masa entry/exit, dan kiraan re-entry. Ringkasan berasingan untuk setiap calon.
