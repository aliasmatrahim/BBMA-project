# Gate replay seterusnya — semakan data 22 Nov 2026

Branch: `research/tengri-bbma-hedge-replay-20261122`  
Status: **HOLD — tiada ledger Tengri selepas 18 Nov**

## Semakan yang dibuat

- Inventori direktori G40 `C:\Trading\Tengri-Hedge-Research` pada 22 Nov.
- Carian fail bernama ledger/statement atau bertarikh 19–20 Nov dalam direktori penyelidikan.
- Semakan proses terminal: satu `terminal64.exe` berada di `C:\Trading\MT5-G40-AI`; tiga `terminal.exe` yang ditemui menggunakan direktori portable ujian (`mt4_probe`, `mt4_cent_margin_preflight_20261120`, `mt4_shared_exit_validation_20261120`). Tiada terminal MT4 biasa yang jelas menyediakan sejarah akaun Tengri semasa untuk dieksport.

Tiada ledger/order stream baharu yang dapat disahkan selepas 18 Nov. Replay signal 19–20 Nov masih satu-satunya tempoh baharu yang ada bar dan tick lengkap, tetapi ia tidak mengandungi aliran posisi Tengri.

## Keputusan gate

Replay gabungan Tengri + Hedge belum boleh dimulakan secara sah. Snapshot posisi 18 Nov tidak boleh dianggap kekal sepanjang tempoh baharu: Tengri mungkin membuka, menutup atau menambah layer selepas snapshot itu. Menganggap posisi beku akan mengubah exposure Hedge dan menghasilkan P&L yang tidak mewakili akaun sebenar.

Data lama Mei–18 Nov sudah digunakan untuk kajian strategi. April 6–30 tidak memenuhi liputan tick, dan sampel Jan–Mar yang disiasat tiada tick HFM Demo4. Tempoh-tempoh itu tidak digunakan semula atau ditampal dengan feed lain.

## Data minimum untuk sambung

Sediakan/export dari MT4 akaun Tengri bagi tempoh selepas snapshot 18 Nov:
- sejarah transaksi (pair, buy/sell, lot, masa/harga buka dan tutup, ticket, untung, komisen, swap);
- semua posisi yang masih terbuka dan lot bersih mengikut pair pada masa eksport;
- balance/equity serta deposit/withdrawal jika ada.

Gunakan data ini bersama tick bid/ask HFM Demo4 yang telah diarkibkan. Selepas rekonsiliasi, jalankan replay terkunci Type 1–4 berasingan, dengan exit, kos dan safety close yang sama. Tiada parameter dioptimumkan pada holdout.

EA production kekal tidak berubah; tiada pesanan dibuka atau ditutup oleh kerja penyelidikan ini.
