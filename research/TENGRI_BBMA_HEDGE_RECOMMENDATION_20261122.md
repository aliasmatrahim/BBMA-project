# Cadangan strategi Hedge BBMA — keputusan dan rekonsiliasi replay

Tarikh: 22 Nov 2026  
Status: **Cadangan untuk ujian penyelidikan sahaja; belum layak production**  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Keputusan cadangan

Bawa hanya satu calon utama ke penilaian seterusnya:

- **Entry:** BBMA H1 Re-Entry Type 3 yang confirmed, sehala dengan pergerakan adverse kepada net exposure Tengri; kekalkan D1/H4/M15 approval, minimum enam order Tengri arah net, same-pair sahaja, sasaran hedge 25% lot net dan spread cap 3 pip.
- **Konteks entry:** H4 Mid-BB + ADX(14)>25 + DI sejajar dengan arah Hedge. Ini ialah konteks yang digunakan EA Hedge sedia ada dan memberikan perbandingan yang boleh terus dibuat dengan kawalan.
- **Exit bersama untuk ujian entry:** exit semasa H4 Mid-BB recross melawan Hedge; safety close jika Tengri flat atau arah net berubah.
- **Kawalan:** entry EA semasa H4 Mid-BB + ADX25/DI dengan exit H4 yang sama.
- **Status calon:** Type 3 ialah calon untuk holdout, bukannya strategi yang sudah dipilih. Jangan masukkan Type 1, 2 atau 4 ke dalam build Hedge produksi. Ia boleh kekal sebagai varian penyelidikan berasingan.

Sebab memilih Type 3 untuk susulan hanyalah keputusan saringan: dalam perbandingan pada laluan Tengri yang diskalakan, ia mengatasi kawalan dalam P&L replay. Sampelnya terlalu kecil dan perbandingan lain menggunakan laluan/exit berlainan; ia belum membuktikan kelebihan yang stabil.

## Apa yang sudah dilaporkan

Perbandingan entry/exit terkawal pada **laluan Tengri yang diskalakan** menggunakan exit H4 Mid-BB X0 melaporkan:

| Varian | P&L selepas kos 1 pip (USC) | Kempen tutup | Expectancy / PF | Max DD |
|---|---:|---:|---:|---:|
| Kawalan H4 Mid-BB + ADX25/DI | +762.46 | 24 (6 menang, 18 kalah; 2 terbuka) | −1.01 USC / 0.943 | 42.27% |
| BBMA Type 3 + gate + ADX25/DI | +887.75 | 5 (3 menang, 2 kalah; 1 terbuka) | +41.33 USC / 11.307 | 45.48% |

Type 3 ialah +125.29 USC berbanding kawalan pada replay tersebut, tetapi mempunyai bilangan kempen tertutup yang kecil, DD lebih tinggi dan floating gabungan cutoff yang lebih buruk daripada kawalan. Nilai expectancy/PF itu tidak cukup stabil untuk mengisytiharkan pemenang.

Ujian exit sepadan pada laluan dan saiz yang sama melaporkan bahawa exit X1, iaitu H1 Re-Entry pertama kembali ke arah Tengri, **mengurangkan** P&L Type 3 daripada +887.75 kepada +779.69 USC; expectancy turun daripada +41.33 kepada +19.71 USC, PF daripada 11.307 kepada 3.003, dan DD naik daripada 45.48% kepada 47.71%. Jadi gunakan exit H4 Mid-BB sebagai exit bersama dalam kajian entry berikutnya. Exit H1 Re-Entry tidak menunjukkan kelebihan pada replay itu.

## Mengapa keputusan replay lain tidak boleh digabungkan

Replay Type 1–4 yang lain melaporkan Type 3 −419.97 USC berbanding baseline Tengri sahaja +7,640.34 USC; expectancy kempen −62.17 USC, PF 0.2566 dan DD 106.10%. Ini **bukan perbandingan yang sepadan** dengan jadual di atas:

1. Ujian entry/exit menggunakan laluan `scaled_layer_2026-10-01_4000_fixed_generated.py`. `scaled_layer_replay.py` menskalakan lot ledger mengikut anchor 0.02 lot setiap simbol/arah bagi baki 4,000 USC.
2. Replay Type 1–4 menggunakan lot mentah daripada `replay.py`, sambil meletakkan anchor baki 4,000 USC. Maka pendedahan dan floating core bukan laluan yang sama.
3. Entry gate berbeza: ujian Type 3 yang positif mensyaratkan konteks H4 Mid-BB + ADX25/DI; replay Type 1–4 menggunakan approval gabungan D1/H4/M15 tanpa gate ADX25 tambahan.
4. Exit berbeza: ujian Type 3 menggunakan exit H4 Mid-BB bersama; replay Type 1–4 menggunakan approved H1 Re-Entry kembali ke arah Tengri. Audit mendapati tiada exit normal yang layak semasa kempen dalam replay kedua.

Jadi angka berbeza itu bukan bukti bahawa satu hasil membatalkan yang lain; kedua-dua kajian menguji pendedahan, gate dan exit yang berlainan. Namun ia membuktikan kita belum mempunyai satu replay yang boleh digunakan untuk memilih kombinasi secara adil.

## Kunci perbandingan seterusnya

Sebelum melihat holdout, tetapkan:

1. Satu laluan Tengri dan satu kaedah saiz: sama ada laluan live/ledger mentah dengan modal yang sepadan, atau laluan diskala 0.02 lot. Jangan campurkan kedua-duanya dalam satu ranking.
2. Satu data feed, tempoh, model fill, kos, modal permulaan, lot sizing dan exit X0 yang sama untuk semua arm.
3. Arm kemasukan:
   - kawalan ADX/H4 Mid-BB;
   - BBMA Type 3 sahaja;
   - Type 3 + ADX/DI;
   - Type 3 + Mid-BB;
   - Type 3 + ADX/DI + Mid-BB.
4. D1/H4/M15 approval, enam layer, saiz 25%, spread cap, trim dan safety close dikekalkan seragam. Jangan ubah ambang ADX25 atau cari kombinasi Type lain selepas melihat hasil.
5. Laporkan Type 1–4 secara berasingan jika semua jenis turut diuji. Jangan gabungkan Type 3 dengan jenis lain untuk membesarkan sampel.

## Gate data dan integriti

- Mei–18 Nov 2026 sudah digunakan dalam replay dan tidak boleh menjadi holdout baharu.
- Holdout 6–30 Apr 2026 tidak sah: 15 daripada 19 hari kerja tiada tick lengkap EURUSD dan USDCHF. Jangan isi jurang dengan sumber lain atau potong tempoh secara selektif.
- Sebelum angka prestasi baharu: perlukan satu tempoh bebas dengan tick HFM Demo4 lengkap untuk kedua-dua simbol serta aliran Tengri yang boleh disepadankan.
- Identiti sumber signal, executable EA, ledger Tengri, 739.47 USC/rekonsiliasi yang berkaitan, margin/stop-out, komisen, swap, partial/rejected fill dan model kos perlu dipin/diperjelas sebelum sebarang kesimpulan production.
- Sehingga semua gate lulus, status ujian baharu ialah **HOLD — spesifikasi dikunci, tiada P&L holdout yang sah**.

## Rujukan penyelidikan

- [Perbandingan entry/exit dan keputusan](TENGRI_HEDGE_ENTRY_EXIT_COMPARISON_RESULT_20261122.md)
- [Lock perbandingan entry/exit](TENGRI_HEDGE_ENTRY_EXIT_COMPARISON_LOCK_20261122.md)
- [Replay overlay Type 1–4 dan keputusannya](TENGRI_BBMA_HEDGE_LOCKED_REPLAY_RESULT_20261122.md)
- [Gate holdout alternatif](TENGRI_BBMA_ALTERNATE_EXIT_HOLDOUT_GATE_20261122.md)
- [Kajian kebolehlaksanaan indikator](TENGRI_BBMA_HEDGE_INDICATOR_FEASIBILITY_20261122.md)

EA Hedge produksi tidak diubah. Tiada trading live/forward diaktifkan dan tiada branch di-merge.
