# Replay Hedge Berperingkat untuk Tengri Layer Tinggi — 2026-11-23

## Status
Ujian dikunci sebelum replay baru. Tengri tidak diubah; tiada EA atau trading diaktifkan. Ini kajian replay, bukan keputusan production.

## Tafsiran arahan
Lot hedge disasarkan sebagai peratus daripada pendedahan bersih Tengri yang sedang terbuka. Apabila Tengri menambah atau menutup layer, sasaran hedge dikira semula dan hedge aktif ditambah/dikurangkan untuk ikut sasaran. Lot dibundarkan ke bawah pada step 0.01.

Tangga ujian bagi layer Tengri 7+:
- layer 7: sasaran 25% daripada lot bersih Tengri
- layer 8: 50%
- layer 9: 75%
- layer 10 atau lebih: 100%

Kawalan tambahan menguji nisbah tetap 25%, 50%, 75% dan 100% pada signal Re-Entry Type 3. Nisbah ini tidak dicampur atau dioptimumkan selepas melihat keputusan.

## Peraturan entry, exit dan re-entry
1. Entry hedge hanya pada signal tertutup yang bergerak melawan pendedahan bersih Tengri. Sampel utama ialah BBMA Re-Entry Type 1–4 Build 5.16 yang lulus gate D1/H4/M15 dan konteks H4 ADX(14)>25 dengan DI searah. Kawalan ialah H4 Mid-BB + ADX25/DI.
2. Selepas hedge dibuka, tambah atau trim lot untuk mengekalkan nisbah yang diuji apabila lot Tengri berubah. Spread masuk/add dihadkan kepada 3 pip; fill menggunakan quote tick seterusnya.
3. Pada pengesahan reversal ke arah Tengri, tutup hedge jika P&L hedge bersih selepas kos bukan negatif. Jika rugi, tandakan exit pending dan tunggu pulih ke BE bersih sebelum tutup.
4. Perlindungan BE tambahan menutup hedge apabila ia pernah berada di atas BE bersih, kemudian kembali ke BE bersih. Ini memastikan keuntungan yang hampir terhapus tidak dibiarkan bertukar rugi.
5. Entry baru hanya dibenarkan pada signal adverse baharu selepas hedge ditutup. Jika adverse disahkan semula semasa exit pending, pending dibatalkan dan hedge kekal ikut exposure semasa.
6. Hedge ditutup atas keselamatan jika Tengri flat atau arah exposure bersih bertukar.

## Perbandingan
- BBMA Re-Entry Type 1, 2, 3 dan 4, setiap jenis dilaporkan berasingan.
- Kawalan H4 Mid-BB + ADX25/DI dengan exit Mid-BB.
- Kawalan ADX25 dengan exit Re-Entry, untuk mengasingkan kesan signal exit.
- Tangga 25/50/75/100 dan sweep nisbah tetap Type 3.
- Rekod struktur H4/H1 swing-break + M15 retest daripada replay terdahulu akan dilapor berasingan sebagai rujukan; ia tidak setanding jika lot ladder/BE belum dilaksanakan.

## Data, kos dan batas
Replay tick pada EURUSD dan USDCHF dengan ledger Tengri yang sama, 2026-05-01 hingga 2026-11-18. Fokus entry layer 7+; lapor layer 9+ dan 10+ berasingan. Satu pip kos tetap per tindakan sebagai kos asas dan dua pip sebagai sensitiviti; spread sebenar ada dalam harga bid/ask tick. Pengiraan offset membandingkan keuntungan bersih hedge dengan floating loss Tengri ketika layer tinggi.

Ledger audit mengandungi 1,357 tiket. Semakan awal menunjukkan pendedahan 7+ wujud merentasi kedua-dua pair, manakala 10+ kebanyakannya hanya muncul pada Oktober dalam tetingkap ujian. Tiada holdout bebas kerana tempoh ini telah digunakan dalam replay terdahulu.

Jurang rekonsiliasi baki maksimum yang pernah direkod ialah 739.4727 USC, dan baki residual 14.16 USC pada 4 Ogos masih belum ditutup. Oleh itu baki/equity akaun, drawdown sebagai peratus akaun, margin, stop-out, fill gagal, komisen dan swap tidak boleh dianggap disahkan. Ukuran hedge dan offset masih perlu dibaca sebagai hasil research bersyarat pada ledger itu.
