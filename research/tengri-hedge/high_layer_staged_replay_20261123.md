# Ujian Tengri layer tinggi — ladder hedge dan BE

Tarikh: 23 Nov 2026  
Branch: `research/tengri-bbma-hedge-replay-20261122`  
Jenis: replay tick research; Tengri tidak diubah dan tiada trading diaktifkan.

## Tafsiran dan kunci ujian

Untuk menjadikan “25%→100% ikut risk layer” boleh diuji secara eksplisit, lot hedge sasaran dikira daripada **pendedahan bersih Tengri yang sedang terbuka**. Apabila layer Tengri dibuka atau ditutup, sasaran hedge dikira semula. Jika hedge masih aktif, lotnya ditambah atau di-trim untuk ikut sasaran semasa. Lot dibundarkan ke bawah ke step 0.01.

Tangga yang dikunci: layer 7=25%, layer 8=50%, layer 9=75%, layer 10+=100%. Entry hanya dicetuskan pada layer 7 atau lebih. Ini andaian pemetaan layer yang digunakan untuk replay ini; keputusan perlu diulang jika maksud “risk layer” awak memetakan 25/50/75/100 kepada nombor layer lain.

Entry BBMA ialah Re-Entry Type 1–4 Build 5.16 yang lulus gate D1/H4/M15 dan konteks H4 ADX(14)>25 serta DI searah. Kawalan H4 ialah Mid-BB + ADX25/DI. Exit pada reversal menutup jika untung bersih; jika rugi, exit ditangguh sehingga BE bersih. Selepas kempen hedge pernah melebihi +1 USC bersih, lantai BE menutup apabila ia kembali ke BE. Re-entry hanya pada pengesahan adverse baharu. Hedge aktif ikut pertambahan Tengri tanpa memerlukan signal entry baharu.

Data EURUSD dan USDCHF: 1 Mei–18 Nov 2026, 145 hari quote (21/22/23/21/22/23/13 hari mengikut Mei–Nov). Sampel ini pernah digunakan dalam kajian terdahulu, jadi ia bukan holdout bebas. Spread masuk/keluar sudah wujud dalam harga tick; kos tambahan ialah 1 pip setiap tindakan sebagai asas dan 2 pip sebagai stress. Komisen, swap dan margin broker tidak dimasukkan.

## Hasil kempen hedge

Nilai “net 1 pip” ialah P&L kempen hedge selepas kos asas; “net 2 pip” ialah sensitiviti kos. Semua senario selesai tanpa posisi hedge terbuka pada hujung replay.

| Entry / exit | Kempen (menang/rugi) | Expectancy (USC) | PF selepas 1 pip | Net 1 pip (USC) | Net 2 pip (USC) | Kos 1 pip (USC) |
|---|---:|---:|---:|---:|---:|---:|
| H4 Mid-BB + ADX25, ladder | 96 (1/95) | -27.00 | 0.000 | -2592.11 | -3506.62 | 914.51 |
| ADX25 entry + H1 RE exit, ladder | 106 (0/106) | -28.04 | 0.000 | -2972.43 | -4017.75 | 1045.32 |
| BBMA RE Type 1, ladder | 8 (0/8) | -14.85 | 0.000 | -118.83 | -160.10 | 41.27 |
| BBMA RE Type 2, ladder | 0 (0/0) | — | — | 0.00 | 0.00 | 0.00 |
| BBMA RE Type 3, ladder | 7 (0/7) | -56.01 | 0.000 | -392.10 | -438.68 | 46.58 |
| BBMA RE Type 4, ladder | 7 (0/7) | -0.15 | 0.000 | -1.07 | -91.36 | 90.29 |
| RE3 fixed 25% | 7 (0/7) | -27.90 | 0.000 | -195.29 | -221.23 | 25.93 |
| RE3 fixed 50% | 7 (0/7) | -56.04 | 0.000 | -392.26 | -445.51 | 53.24 |
| RE3 fixed 75% | 7 (0/7) | -84.16 | 0.000 | -589.12 | -669.18 | 80.06 |
| RE3 fixed 100% | 7 (0/7) | -112.29 | 0.000 | -786.05 | -893.66 | 107.61 |

Type 2 tidak menghasilkan event yang lulus gate dalam fail signal bagi tempoh itu, jadi ia tiada trade dan tiada bukti prestasi. Type 1, 3 dan 4 masing-masing menghasilkan 8, 7 dan 7 kempen ladder; tiada satu pun kempen BBMA itu menang selepas kos. Type 4 hampir pulang modal pada kos asas, tetapi rugi 91.36 USC pada stress 2 pip dan masih tidak menampung floating Tengri.

Untuk Type 3, menaikkan nisbah tetap daripada 25% kepada 100% membesarkan kerugian hampir sebaris: -195.29, -392.26, -589.12, kemudian -786.05 USC selepas kos asas. Ini menunjukkan lot lebih besar menggandakan kerugian signal yang sama; ia tidak memperbaiki masa entry.

Kawalan ADX25 sangat kerap masuk semula selepas BE: 96 kempen (1 menang, 95 rugi) dengan exit Mid-BB; 106 kempen (0 menang, 106 rugi) dengan exit H1 RE. Kos asas terkumpul masing-masing 914.51 dan 1,045.32 USC. Ini ialah churn tinggi, bukan bukti perlindungan berkesan.

## Adakah untung hedge menampung floating Tengri?

**Tidak dalam replay ini.** Pada semua senario, masa hedge net menampung 100% floating loss Tengri pada layer 7+ ialah 0. Purata masa berwajaran bagi kadar offset yang dihadkan pada 100% juga amat kecil: tertinggi 0.0211% untuk ADX25 ladder. Kadar offset maksimum pada satu masa ialah 12.07% untuk ADX25 ladder; untuk BBMA ladder maksimum 2.18%. Keuntungan hedge positif hanya muncul pada 1.16% masa layer tinggi bagi ADX25 ladder, dan kurang daripada 0.05% bagi setiap jenis BBMA ladder.

Bagi Type 1–4, tiada exit kempen yang direkod sebagai close pada reversal dengan untung; kebanyakannya keluar melalui lantai BE atau safety close. Dalam praktik tick, gap quote selepas ambang BE boleh menyebabkan realisasi selepas kos sedikit negatif. Lantai BE membantu mengehadkan giveback, tetapi tidak menghasilkan hedge profit yang cukup untuk menampung basket Tengri.

## Drawdown model dan batas keputusan

Drawdown akaun yang dikira daripada replay (sebelum kos / kos asas / stress 2 pip) ialah:

| Senario | Model DD sebelum kos | Model DD kos 1 pip | Model DD stress 2 pip |
|---|---:|---:|---:|
| H4 Mid-BB + ADX25 ladder | 55.64% | 69.25% | 83.90% |
| ADX25 + H1 RE exit ladder | 57.16% | 73.91% | 92.19% |
| RE Type 1 ladder | 49.93% | 50.47% | 51.02% |
| RE Type 3 ladder | 52.50% | 52.75% | 52.99% |
| RE Type 4 ladder | 49.25% | 49.55% | 49.85% |
| RE3 fixed 25% | 50.90% | 51.09% | 51.27% |
| RE3 fixed 50% | 52.34% | 52.75% | 53.16% |
| RE3 fixed 75% | 53.89% | 54.52% | 55.17% |
| RE3 fixed 100% | 55.52% | 56.42% | 57.33% |

Angka DD ini **tidak disahkan sebagai risiko akaun**. Audit replay mencatat jurang rekonsiliasi baki maksimum 739.4727 USC dan residual 14.16 USC pada 4 Ogos yang belum ditutup. Identiti sumber juga bercanggah: source branch menunjukkan Build 5.16 sementara fail identiti menyebut Build 4.59. Stop-out, margin, komisen, swap dan fill gagal broker masih belum dibuktikan. Oleh itu, P&L hedge relatif kepada Tengri-only ialah hasil simulasi atas ledger ini, bukan prestasi production.

Replay swing-break H4/H1 + retest M15 yang dibuat terdahulu pada nisbah tetap 25% mencatat -414.85 USC selepas kos model dan DD model 33.33%; ia belum diuji semula dengan ladder dan lantai BE yang sama, jadi tidak setanding dengan matriks di atas.

## Keputusan

Ladder semasa 25/50/75/100 dan kombinasi exit yang diuji **tidak memenuhi objektif utama**: ia tidak membayar semula floating loss Tengri. Type 4 paling hampir pulang modal pada kos asas, tetapi hanya tujuh kempen, tiada pemenang dan gagal pada stress 2 pip. Nisbah tetap 100% menambah kerugian Type 3 dan tidak memberi offset penuh. Belum ada calon yang patut diaktifkan pada EA.

Langkah penyelidikan seterusnya ialah tutup jurang rekonsiliasi dan sahkan identiti Build 5.16 dahulu. Selepas itu barulah kunci holdout bebas untuk entry struktur H4/H1 → retest M15 berbanding BBMA Type 4, dengan polisi exit/BE yang sama, kos broker lengkap dan pemeriksaan margin. Jangan ubah parameter pada sampel Mei–November ini.
