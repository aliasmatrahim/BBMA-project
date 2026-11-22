# Perbandingan Entry Hedge Tengri: H4 ADX vs BBMA Re-Entry

Tarikh: 22 Nov 2026  
Tempoh replay: 1 Mei–18 Nov 2026  
Status: **Entry pass selesai; keputusan bersyarat. Exit BBMA belum dibandingkan pada stream dan saiz yang sama.**  
Branch: research/tengri-bbma-hedge-replay-20261122

## Soalan yang diuji

Adakah H1 BBMA Re-Entry Type 1–4, selepas gate D1/H4 dan pengesahan konteks H4 ADX25/DI, memberi kemasukan Hedge yang lebih baik daripada trigger H4 Mid-BB + ADX25/DI? Semua varian menggunakan exit H4 Mid-BB yang sama supaya perbandingan ini mengasingkan kesan entry.

## Kunci replay

- Pair EURUSD dan USDCHF; data quote/tick HFM Demo4 yang sama; anchor akaun 4,000 USC.
- Laluan Tengri dibekukan dan dikecilkan kepada anchor ujian. P&L Hedge tidak mengubah lot Tengri selepas itu.
- Hedge lawan net exposure Tengri hanya selepas sekurang-kurangnya 6 order bersih; saiz sasaran 25% lot bersih, dibundarkan ke bawah; satu kempen Hedge pada satu masa bagi setiap pair.
- Entry menggunakan quote segar pertama selepas pengesahan event; event dibuang jika quote lewat lebih 5 minit. Event Type 1–4 mesti lulus D1/H4/M15 dan mempunyai konteks H4 Mid-BB + ADX(14)>25 + DI searah.
- Exit bersama: H4 Mid-BB recross melawan Hedge; keselamatan tutup jika net exposure Tengri kosong atau bertukar arah. Saiz, spread cap 3 pip dan sumber quote dikekalkan sama.
- Bid/Ask tick digunakan untuk fill; spread sudah terkandung dalam fill. Kos tambahan dimodelkan 1 pip bagi setiap lot/tindakan Hedge; stress 2 pip. Jangan tolak spread sekali lagi.
- Coverage quote: Mei 21 hari, Jun 22, Julai 23, Ogos 21, September 22, Oktober 23 dan 1–18 November 13 hari.

## Keputusan akaun

P&L dan drawdown ialah flow-adjusted akaun, termasuk mark-to-market Hedge terbuka pada cutoff. “Base” menolak kos 1 pip/tindakan; “stress” menolak 2 pip/tindakan. DD dan ekuiti minimum dalam jadual datang daripada siri ekuiti setelah kos yang berkenaan.

| Entry | P&L base / stress (USC) | Max DD base / stress | Min equity base / stress (USC) | Kempen ditutup; menang/kalah; terbuka | Expectancy / PF kempen tertutup, selepas kos base |
|---|---:|---:|---:|---:|---:|
| Tiada Hedge | +603.71 / +603.71 | 49.54% / 49.54% | 3,252.80 / 3,252.80 | — | — |
| H4 Mid-BB + ADX25/DI, kawalan | +762.46 / +668.96 | 42.27% / 42.86% | 3,383.12 / 3,362.21 | 24; 6/18; 2 | −1.01 USC / 0.943 |
| H1 RE Type 1 + gate + ADX25 | +662.03 / +636.60 | 47.18% / 47.40% | 3,331.84 / 3,327.02 | 9; 3/6; 1 | −4.51 USC / 0.826 |
| H1 RE Type 2 + gate + ADX25 | +603.71 / +603.71 | 49.54% / 49.54% | 3,252.80 / 3,252.80 | 0; 0/0; 0 | Tiada signal/trade |
| H1 RE Type 3 + gate + ADX25 | +887.75 / +870.76 | 45.48% / 45.57% | 3,414.99 / 3,414.99 | 5; 3/2; 1 | +41.33 USC / 11.307 |
| H1 RE Type 4 + gate + ADX25 | +642.99 / +610.80 | 46.92% / 47.06% | 3,397.80 / 3,383.14 | 6; 2/4; 2 | −8.93 USC / 0.820 |

Kiraan signal yang lulus gate tambahan H4 ADX25/DI: Type 1 = 27 (EURUSD 14, USDCHF 13), Type 2 = 0, Type 3 = 14 (5, 9), Type 4 = 23 (18, 5). Kiraan kempen yang benar-benar dibuka ialah 10 untuk Type 1, sifar untuk Type 2, 6 untuk Type 3, dan 8 untuk Type 4. Event yang lulus tidak semestinya menjadi entry jika syarat layer, kempen sedia ada atau quote tidak membenarkan.

Kos tetap 1 pip / stress 2 pip masing-masing ialah: kawalan ADX25 93.50 / 187.01 USC; Type 1 25.43 / 50.87; Type 3 16.99 / 33.97; Type 4 32.18 / 64.37. Anggaran spread Bid/Ask yang sudah tercermin dalam P&L: 116.45, 43.24, 16.10 dan 29.98 USC mengikut turutan tersebut.

## Tafsiran

- Dalam sampel ini, Type 3 ialah petunjuk entry paling menjanjikan: P&L selepas kos base +887.75 USC, iaitu +125.29 USC berbanding kawalan ADX25. Stress 2 pip kekal +870.76 USC, +201.80 USC berbanding kawalan.
- Type 3 **bukan pemenang yang disahkan**. Hanya 5 kempen tertutup menyokong expectancy positif; 1 lagi masih terbuka. PF 11.31 datang daripada 3 menang dan 2 kalah sahaja, jadi sangat tidak stabil.
- Type 3 memberi max DD 45.48%, lebih tinggi 3.21 mata peratus daripada kawalan 42.27%, walaupun ekuiti minimum lebih tinggi. Pada cutoff, floating gabungan Type 3 ialah −1,430.47 USC berbanding −1,323.86 kawalan dan −1,511.56 tanpa Hedge. Jadi Type 3 menghasilkan lebih banyak P&L ujian tetapi perlindungan floating hujung sampelnya lebih lemah daripada kawalan.
- Kawalan ADX25 sendiri menaikkan P&L berbanding tanpa Hedge, tetapi 18 daripada 24 kempen tertutup rugi dan expectancy kempen tertutupnya negatif. Sebahagian P&L akaun termasuk nilai Hedge yang masih terbuka.
- Type 1 dan Type 4 tidak mengatasi kawalan. Type 2 tiada trade, maka tiada kesimpulan profitabiliti.
- Trigger Type 3 mengambil quote pertama dalam tetingkap maksimum 5 minit selepas event. Runner ini belum melaporkan median/p95 kelewatan sebenar, jadi ketepatan latensi belum dibuktikan.

## Exit dan batas kesahihan

Replay ini **tidak mengasingkan exit**: semua varian menggunakan exit H4 Mid-BB yang sama. Kajian struktur berasingan sebelum ini mendapati entry H4+H1 dengan retest M15 dan exit H4+H1 mengurangkan kerugian daripada −581.39 kepada −414.85 USC serta DD daripada 36.82% kepada 33.33%, tetapi masih rugi. Ia menggunakan saiz hedge bertahap 25/50/75/90%, jadi angka itu bukan perbandingan sepadan dengan ujian 25% ini.

Pengesahan release masih bercanggah: sumber BBMA menunjukkan Build 5.16 tetapi fail identiti release menyebut 4.59. Replay juga melaporkan jurang rekonsiliasi sehingga 739.47 USC apabila laluan akaun 4,000 USC dibandingkan dengan statement berskala lot asal; data itu bukan hasil akaun live yang disahkan. Komisen, swap, slip di luar quote, rejection/partial fill, margin dan stop-out sebenar belum dimodelkan. Ini bukan out-of-sample dan tiada parameter dilaras pada sampel ini.

## Keputusan sementara dan langkah berikutnya

Kekalkan H4 Mid-BB + ADX25/DI sebagai kawalan. Bawa Type 3 sahaja ke pass penyelidikan exit seterusnya, bersama kawalan ADX25, dan bandingkan exit H4 Mid-BB dengan exit H1 BBMA Re-Entry ke arah net Tengri pada data, saiz 25%, fill dan kos yang sama. CSAK exit hanya boleh dimasukkan selepas audit sumber/event memastikan formula close melepasi Mid-BB dan MA5 High/Low betul-betul tersedia. Jangan aktifkan EA berdasarkan replay ini.
