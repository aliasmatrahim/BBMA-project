# Objektif baharu: Hedge untuk kelangsungan margin Tengri

Tarikh: 23 November 2026  
Branch: `research/tengri-bbma-hedge-replay-20261122`  
Status: spesifikasi penyelidikan; belum dilaksanakan dalam EA dan belum diuji untuk trading.

## Perubahan objektif

Objektif utama EA Hedge kini ialah **mengurangkan risiko akaun mencapai stop-out / margin call apabila exposure Tengri dan layer bertambah tinggi**. Hedge profit yang membantu mengimbangi floating loss ialah manfaat sampingan. Sasaran “menampung semua floating loss” bukan lagi kriteria wajib.

Tiada hedge boleh menjamin akaun tidak MC dalam semua keadaan. Gap, spread melebar, slippage, order ditolak, margin rule broker, swap dan kerugian yang telah terkumpul boleh menyebabkan akaun tetap tidak selamat. Matlamat yang boleh diuji ialah mengekalkan margin/free-margin di atas ambang keselamatan yang ditetapkan dalam senario adverse yang eksplisit, termasuk kos dan fill broker.

Susunan keutamaan:
1. Elak stop-out dalam senario ujian yang ditetapkan.
2. Kekalkan free margin dan ruang untuk fill/volatility.
3. Kurangkan exposure bersih terhadap pergerakan adverse seterusnya.
4. Ambil untung hedge taktikal atau tutup hampir BE apabila perubahan exposure Tengri menjadikan pelepasan itu selamat.
5. Kurangkan kos/churn dan tingkatkan P&L gabungan.

## Cadangan polisi: staging berdasarkan layer, saiz berdasarkan risiko

Gunakan layer Tengri sebagai **pencetus pemeriksaan / staging**, bukan sebagai satu-satunya formula lot hedge. Floating loss pula masuk melalui equity semasa dan senario tekanan; jangan darab terus nilai floating loss dengan faktor lot.

- Setiap pair dilindungi oleh hedge bertentangan pada **simbol yang sama** berdasarkan pendedahan bersih Tengri pair itu. Cross-pair boleh diuji berasingan, tetapi jangan anggap ia memberi netting margin atau offset P&L yang tepat.
- Layer bertambah mengalihkan sistem melalui zon risiko: hijau (belum perlu hedge keselamatan), amber (buka tranche kecil), oren (tambah perlindungan), merah (naikkan ke exposure hedge yang diperlukan untuk lulus gate margin). Ambang zon mesti ditentukan daripada data margin/account sebenar, bukan andaian nombor layer sahaja.
- Nisbah 25% / 50% / 75% / 100% kekal sebagai **calon tangga untuk diuji**. Uji dua tafsiran berasingan: sasaran hedge daripada jumlah net lot Tengri semasa, dan tambahan hedge daripada lot baharu setiap layer. Jangan campurkan kedua-dua kaedah dalam satu run.
- Cadangan utama ialah kaedah hibrid: layer menentukan bila perlu menilai/menambah tranche; margin-stress menentukan lot minimum yang benar-benar diperlukan. Had maksimum awal untuk kajian ialah menyamai 100% lot net Tengri; overhedge yang membalikkan exposure tidak dibenarkan tanpa ujian khusus.

## Kaedah pengiraan lot untuk ujian

Bagi setiap simbol, takrifkan (Q) sebagai net lot bertanda bagi semua posisi Tengri (BUY positif, SELL negatif), dan (H) sebagai net lot bertanda hedge yang bertentangan. Gunakan konfigurasi broker untuk menghitung P&L, margin, kos dan conversion deposit currency.

Pada setiap tindakan yang dicadangkan, simulasi sekurang-kurangnya tiga keadaan: adverse continuation, reversal/whipsaw, serta gap atau spread melebar. Bagi setiap calon lot hedge:
- kira equity tekanan selepas perubahan harga dan kos: (E_s(H));
- kira used margin broker sebenar selepas hedge/penutupan: (M_s(H));
- kira margin level tekanan (ML_s(H)=100	imes E_s(H)/M_s(H)), apabila margin bukan sifar;
- pilih lot hedge **paling kecil** yang mengekalkan semua senario di atas ambang margin keselamatan dan free-margin minimum yang dikunci.

Ambang keselamatan mesti berada di atas stop-out broker dengan buffer yang nyata. Nilainya belum dikunci kerana entity akaun, tetapan margin simbol, tahap stop-out dan rekonsiliasi baki belum disahkan. Jika tiada lot dalam had yang dibenarkan boleh lulus gate, sistem mesti menandakan keadaan “tidak dapat dilindungi”; ia tidak boleh menaikkan hedge tanpa had atau melaporkan keadaan selamat.

Floating loss bukan sasaran lot secara langsung. Ia sebahagian daripada equity semasa. Hedge mengehadkan sensitiviti kepada harga **selepas hedge dibuka**; ia tidak memadam loss yang telah berlaku. Membuka hedge terlalu besar lewat dalam drawdown boleh mengunci kerugian dan meningkatkan kos, sementara penutupan hedge boleh mengembalikan margin standard pada posisi Tengri yang terdedah.

## Struktur posisi dan pengurusan exit

Uji pengurusan dalam dua fungsi (boleh guna magic/basket berlainan supaya lot dan keputusan exit boleh diaudit):

1. **Tranche perlindungan (insurance):** bertahan selagi stress-margin Tengri masih gagal tanpa tranche ini. Ia dilepaskan hanya apabila stress gate masih lulus selepas pelepasan, atau apabila exposure Tengri mengecil/flat.
2. **Tranche taktikal:** digunakan untuk menangkap reversal jangka pendek. BBMA/struktur harga mengesahkan timing; exit pada profit bersih atau hampir BE dibenarkan hanya jika pengiraan selepas tutup masih lulus stress-margin gate.

Apabila harga kembali menuju TP basket Tengri:
- semak P&L bersih hedge selepas spread, komisen dan swap;
- boleh tutup tranche taktikal apabila untung atau hampir BE **jika** margin selepas tutup masih melepasi gate;
- jika syarat itu gagal, jangan paksa tutup semata-mata untuk mendapat BE. Kekalkan tranche perlindungan atau tunggu exposure Tengri turun;
- insurance tranche lazimnya dilepaskan bersama pengurangan/penutupan exposure Tengri, kerana menutup hedge ketika Tengri masih terbuka boleh menaikkan margin yang diperlukan serta-merta.

Re-entry hanya berlaku selepas price bergerak semula adverse dan signal struktur/BBMA pada candle tertutup mengesahkan keadaan, serta stress gate menunjukkan tranche tambahan perlu. Gunakan hysteresis/cooldown dan satu tindakan bagi setiap event supaya sistem tidak berulang buka-tutup akibat isyarat bertukar cepat.

## Signal entry dan reversal

BBMA bukan pengira margin dan tidak patut menjadi satu-satunya trigger perlindungan. Ia hanya membantu masa tranche taktikal:
- H4/H1 struktur atau bias menentukan sama ada risiko adverse masih aktif;
- M30/M15 retest atau Re-Entry yang sudah disahkan pada candle tertutup menjadi calon timing;
- signal exit pada arah pemulihan Tengri boleh menutup tranche taktikal apabila profit/BE dan margin selepas close selamat.

Tranche perlindungan dicetuskan oleh layer/risk gate walaupun signal reversal belum muncul. Jika menunggu signal teknikal sahaja, hedge mungkin datang terlalu lewat untuk tujuan anti-MC.

## Ukuran kejayaan replay baharu

Kriteria utama bukan win rate/PF hedge semata-mata. Lapor:
- bilangan stop-out atau stress-gate failures;
- minimum margin level dan minimum free margin per simbol serta akaun;
- masa pertama margin gate gagal, dan tempoh pendedahan tanpa perlindungan;
- lot hedge maksimum/ purata dan peratus net Tengri yang dilindungi;
- P&L gabungan Tengri + hedge selepas spread, komisen, swap dan fill/reject;
- floating drawdown gabungan, kos hedge, churn, duration, BE/profit exits dan re-entry;
- perbandingan Tengri sahaja vs polisi hedge menggunakan ledger, tick, kos dan senario tekanan yang sama.

Uji holdout bebas selepas polisi dikunci. Jangan cari parameter baharu pada tempoh yang sama. Replay 1 Mei–18 Nov 2026 yang telah dilaporkan tidak menguji margin/stop-out broker dan bukan holdout; angka lama kekal sebagai rekod bagi polisi lama sahaja.

## Gate sebelum angka boleh dianggap sah

Masih perlu ditutup: jurang rekonsiliasi maksimum 739.4727 USC; residual 14.16 USC pada 4 Ogos; konflik identiti Build 5.16 vs Build 4.59; entity akaun sebenar; margin hedge dan margin level/stop-out untuk EURUSD serta USDCHF; komisen/swap; dan bukti fill gagal/slippage. Dapatkan nilai daripada statement serta spesifikasi MT4 akaun itu sebelum mengunci formula dan ambang.

HFM menerangkan bahawa posisi sama dan bertentangan yang match boleh mendapat margin sifar pada volum matched, manakala menutup satu sisi boleh mengembalikan margin standard pada posisi yang tinggal. Oleh itu, peraturan akaun dan contract specification mesti disahkan pada terminal/entiti yang digunakan sebelum manfaat margin itu masuk dalam model. Rujukan:
- HFM FAQ, margin bagi hedge dan perubahan margin apabila satu sisi ditutup: https://www.hfm.com/int/en/help/faqs
- MetaTrader 4 contract specification, termasuk medan “Margin hedge”: https://www.metatrader4.com/en/trading-platform/help/service/symbol_spec

## Keputusan tindakan

- Objektif masa depan bertukar kepada **survival margin / anti-MC**.
- Kaedah calon utama: **hybrid staging + stress-margin sizing**, dengan tranche perlindungan dan tranche taktikal.
- Jangan ubah EA atau aktifkan trading berdasarkan nota ini.
- Ujian seterusnya selepas rekonsiliasi dan identiti build: replay margin-aware yang membandingkan (A) tangga 25/50/75/100 pada net lot semasa, (B) tambahan per layer pada lot Tengri baharu, dan (C) sizing minimum melalui stress-margin gate. Semua guna exit, kos dan senario yang sama.
