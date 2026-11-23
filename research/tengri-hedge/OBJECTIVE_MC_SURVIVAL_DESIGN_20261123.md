# Objektif baharu: Hedge untuk kelangsungan margin Tengri

Tarikh: 23 November 2026  
Branch: `research/tengri-bbma-hedge-replay-20261122`  
Status: spesifikasi penyelidikan; belum dilaksanakan dalam EA dan belum diuji untuk trading.

## Perubahan objektif

EA Hedge kini mempunyai dua objektif:

1. **Survival:** mengurangkan risiko akaun mencapai stop-out/MC apabila exposure dan layer Tengri meningkat.
2. **Pulangan:** mencari hedge yang memberi sumbangan untung bersih dan memperbaiki hasil gabungan Tengri + Hedge selepas kos.

Kriteria keseluruhan ialah memaksimumkan hasil bersih gabungan pada holdout, tertakluk pada gate survival dan had kerugian. P&L hedge sahaja tetap dilaporkan; hedge yang menanggung kos perlindungan hanya boleh diterima jika ia membantu survival dan keputusan gabungan lebih baik daripada Tengri sahaja. Ia tidak cukup sekadar menghasilkan banyak trade hedge yang menang.

### Guard opsyenal dan keutamaan recovery

Nisbah drawdown 10–15% ialah **guard pilihan untuk amaran/de-risk**, bukan arahan auto-cut lalai. Default reka bentuk ialah `RECOVERY_FIRST`: jangan realisasikan kerugian hanya kerana ambang itu tersentuh jika basket masih mempunyai laluan recovery yang munasabah dan margin boleh dikekalkan dengan selamat.

Gunakan baki rujukan tetap (B_ref), iaitu balance akaun sejurus sebelum kitaran risiko gabungan pertama bermula. Kitaran bermula apabila exposure Tengri pertama dibuka dan berakhir apabila semua posisi Tengri/Hedge yang dilindungi kembali flat. Jangan alihkan baseline setiap kali balance berubah; deposit/pengeluaran selepas baseline perlu dinormalkan supaya tidak menyamarkan drawdown.

Guard perlu melihat **equity akaun**, bukan balance sahaja, supaya floating loss Tengri dan Hedge dikira:
`LossPct = 100 × (B_ref − Equity_adjusted) / B_ref`

Tindakan default yang dicadangkan:
- **10% daripada B_ref:** amaran dan semakan risiko dipertingkat. Kira semula stress margin, hedge minimum dan kos carry. Tiada auto-close semata-mata kerana threshold ini tercapai.
- **15% daripada B_ref:** amaran serius dan semakan recovery. Ia juga tidak auto-close dalam mod default.
- Simpan `STRICT_CUT` sebagai mod pilihan untuk dibandingkan secara berasingan: hard cut pada 10% atau 15%. Ia tidak menjadi default EA sehingga dipilih secara jelas.

Dalam mod `RECOVERY_FIRST`, posisi boleh dikekalkan selepas amaran selagi stress-margin kekal di atas buffer yang dikunci dan replay menunjukkan laluan munasabah untuk mengurangkan basket/berundur ke BE atau TP dalam horizon ujian yang ditetapkan. “Masih ada potensi recovery” tidak boleh ditentukan daripada harapan semata-mata: laluan itu mesti kekal dalam margin gate, termasuk adverse continuation, spread/gap dan swap. Jika tiada laluan yang mengekalkan gate, buat de-risk separa; tutup seluruh basket hanya jika langkah lebih kecil tidak dapat memulihkan keselamatan margin.

Survival gate stop-out tetap wajib walaupun loss cap pilihan dimatikan. Jika margin menghampiri stop-out dan tiada hedge/trim yang selamat dapat memulihkan buffer, perlindungan akaun mengatasi usaha menunggu BE. Tanpa kuasa atau sambungan untuk menghalang layer baharu dan mengurangkan/menutup posisi Tengri apabila gate gagal, keupayaan anti-MC dan mana-mana loss limit tidak boleh dikuatkuasakan dengan boleh dipercayai.

Susunan keutamaan:
1. Lulus margin/free-margin gate di semua senario tekanan yang dikunci.
2. Kekalkan pilihan recovery selagi margin gate masih lulus.
3. Dalam kekangan survival dan recovery tersebut, tingkatkan P&L bersih gabungan Tengri + Hedge.
4. Tingkatkan sumbangan bersih hedge dan kurangkan kos/churn tanpa mengorbankan perlindungan.
5. Gunakan guard 10–15% hanya sebagai amaran atau mod STRICT_CUT yang dipilih; ambil untung/BE apabila pelepasan selamat.

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
- pilih lot hedge **paling kecil** yang mengekalkan semua senario di atas ambang margin keselamatan dan free-margin minimum yang dikunci. Dalam ruang saiz yang lulus gate, nilai exit/re-entry berdasarkan P&L bersih gabungan dan pilih calon yang meningkatkan pulangan holdout tanpa melanggar margin gate atau polisi loss-guard yang dipilih.

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
- P&L gabungan Tengri + hedge serta sumbangan Hedge tersendiri selepas spread, komisen, swap dan fill/reject; expectancy dan PF bersih pada holdout;
- floating drawdown gabungan dan maksimum loss sebagai % B_ref; amaran 10/15%, pemulihan selepas threshold, partial/full cut dalam STRICT_CUT jika diuji, slippage ketika de-risk, kos hedge, churn, duration, BE/profit exits dan re-entry;
- perbandingan Tengri sahaja vs polisi hedge menggunakan ledger, tick, kos dan senario tekanan yang sama.

Uji holdout bebas selepas polisi dikunci. Jangan cari parameter baharu pada tempoh yang sama. Replay 1 Mei–18 Nov 2026 yang telah dilaporkan tidak menguji margin/stop-out broker dan bukan holdout; angka lama kekal sebagai rekod bagi polisi lama sahaja.

## Gate sebelum angka boleh dianggap sah

Masih perlu ditutup: jurang rekonsiliasi maksimum 739.4727 USC; residual 14.16 USC pada 4 Ogos; konflik identiti Build 5.16 vs Build 4.59; entity akaun sebenar; margin hedge dan margin level/stop-out untuk EURUSD serta USDCHF; komisen/swap; bukti fill gagal/slippage; dan sama ada EA Hedge boleh membaca exposure Tengri serta menyelaras risk-lock/partial close jika survival gate gagal. Dapatkan nilai daripada statement serta spesifikasi MT4 akaun itu sebelum mengunci formula dan ambang.

HFM menerangkan bahawa posisi sama dan bertentangan yang match boleh mendapat margin sifar pada volum matched, manakala menutup satu sisi boleh mengembalikan margin standard pada posisi yang tinggal. Oleh itu, peraturan akaun dan contract specification mesti disahkan pada terminal/entiti yang digunakan sebelum manfaat margin itu masuk dalam model. Rujukan:
- HFM FAQ, margin bagi hedge dan perubahan margin apabila satu sisi ditutup: https://www.hfm.com/int/en/help/faqs
- MetaTrader 4 contract specification, termasuk medan “Margin hedge”: https://www.metatrader4.com/en/trading-platform/help/service/symbol_spec

## Keputusan tindakan

- Objektif bertukar kepada **survival margin + pulangan bersih hedge sambil mengekalkan peluang recovery**. Loss guard 10–15% bersifat opsyenal: default amaran/review, bukan auto-cut; STRICT_CUT diuji hanya sebagai mod pilihan.
- Kaedah calon utama: **hybrid staging + stress-margin sizing**, dengan tranche perlindungan dan tranche taktikal.
- Jangan ubah EA atau aktifkan trading berdasarkan nota ini.
- Ujian seterusnya selepas rekonsiliasi dan identiti build: replay margin-aware yang membandingkan (A) tangga 25/50/75/100 pada net lot semasa, (B) tambahan per layer pada lot Tengri baharu, dan (C) sizing minimum melalui stress-margin gate. Semua guna exit, kos dan senario yang sama.
