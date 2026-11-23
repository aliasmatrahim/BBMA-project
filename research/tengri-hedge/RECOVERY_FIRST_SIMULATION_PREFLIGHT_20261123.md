# Preflight simulasi Recovery-First Tengri + Hedge — 2026-11-23

## Status

**HOLD — ledger mentah dan runner ditemui pada G40, dan log tester mengesahkan Build 5.16 untuk aliran signal yang dikaji. Replay baharu masih disekat: warm-up tick MT4 yang sepadan tidak mencukupi.** Arkib tick yang ada mempunyai liputan hari ujian Mei–November, tetapi hanya 4 daripada 19 hari kerja warm-up sebelum 1 Mei mempunyai quote. Sumber downloader yang ditemui menggunakan MT5; ia tidak dijalankan dan datanya tidak dianggap setara dengan MT4.

Tiada replay prestasi baharu dijalankan. EA Tengri/Hedge tidak diubah dan trading tidak diaktifkan.

## Objective yang dipakai

- Utamakan margin survival.
- Kekalkan peluang recovery selagi stress-margin masih lulus dan laluan recovery yang munasabah wujud.
- Cari P&L bersih positif untuk hedge dan gabungan Tengri + Hedge selepas kos.
- Guard drawdown 10–15% ialah amaran pilihan; tiada auto-cut berdasarkan angka itu sahaja. Hard-cut hanya pembanding `STRICT_CUT`.
- Jika margin menghampiri stop-out dan tiada hedge/partial de-risk yang lulus gate, teruskan pengurangan risiko secara terkawal.

Spesifikasi penuh: `OBJECTIVE_MC_SURVIVAL_DESIGN_20261123.md`.

## Semakan input semula — 23 November 2026

### Ledger dan runner
- Ledger mentah kini ditemui pada G40: 1,357 order Tengri, 227 snapshot baki, dan 13 aliran tunai. Audit layer mengesahkan lapisan maksimum 14.
- Template `tengri_hedge_bbma_exit_comparison_20261122.py` dan base runner ADX H4 ditemui pada G40. Wrapper dalam branch masih tidak lengkap untuk dijalankan sendiri; data mentah tidak disalin ke repo.
- Root-cause audit menjejak residual 739.47 USC kepada perbandingan 1,356 order yang diskalakan untuk modal 4,000 USC dengan snapshot baki dan aliran tunai akaun asal yang tidak diskalakan. Ini bukan rekonsiliasi like-for-like dan diklasifikasikan sebagai artifak perbandingan skala, bukan kekurangan ledger mentah. Run order asal mempunyai residual harian maksimum sekitar 14.16 USC dalam tempoh ujian; baki residual kecil masih perlu dipadankan kepada swap/komisen atau sempadan masa server.

### Identiti Build
- Source `BBMA_EA.mq4` menandakan Version 5.16, BuildTag `V516_M12_ENTRYCANDLE_GATE_20261107`, dan SourceRev `M12_ENTRYCANDLE_GATE_001_20261107`.
- Log tester MT4 bagi pair run terkunci mencetak Build=5.16 bersama tag dan revision yang sama. Ini meminkan identiti signal stream untuk kajian ini.
- Rujukan Build 4.59 yang ditemui ialah rekod/artifak legacy; ia bukan bukti bahawa signal stream ujian ini datang daripada Build 4.59. Simpan artifak legacy di luar input replay.

### Tick dan warm-up
- Tick EURUSD/USDCHF yang tersedia mempunyai quote bagi semua 145 hari ujian Mei–18 November untuk setiap pair; tiada hari kerja ujian yang hilang, dan audit menemui tiada quote tidak sah atau susunan masa terbalik.
- Arkib penuh memuat 210 fail bertarikh bagi setiap pair, tetapi 60 fail setiap pair kosong. Dalam warm-up 6–30 April, hanya 4 daripada 19 hari kerja mempunyai quote; 15 hari kerja kosong. Ini gagal keperluan warm-up 16 hari kalendar bagi ADX H4 daripada tick.
- Fail tick mempunyai timestamp berulang pada sebahagian hari dan jurang intra-hari maksimum kira-kira 15 minit untuk EURUSD dan 30 minit untuk USDCHF. Perlu kekalkan audit ini bersama manifest sebelum menganggap liputan tick lengkap.
- Carian MT4 menemukan hanya fail tester FXT kecil dan `ticks.raw` sekitar 9.5 KB; kedua-duanya tidak membuktikan arkib raw tick penuh. Server sejarah MT4 yang ditemui berlabel `HFMarketsSV-Demo Server`, manakala manifest tick sedia ada menyatakan `HFMarketsGlobal-Demo4` melalui MT5. Nama server ini berbeza, jadi tick MT5 tidak boleh dianggap feed MT4 yang sama. Skrip downloader MT5 tidak dijalankan.

## Dapatan terdahulu yang boleh dijadikan calon sementara sahaja

Laporan replay terdahulu `TENGRI_MTF_STAGED_REVERSAL_REPLAY_20261121.md` mencatat:

| Polisi lama | P&L stress model | Max DD stress model | Equity minimum | Status akhir |
|---|---:|---:|---:|---|
| Tengri sahaja | +603.71 USC | 49.54% | 3,252.80 USC | Tiada hedge |
| HoldCap | +524.22 USC | 26.22% | 3,332.18 USC | Hedge protection berbeza |
| DEFER + firewall 1:400 | +1,204.24 USC | 30.10% | 3,489.69 USC | Tiada emergency close; hedge USDCHF 1.12 lot masih terbuka |

DEFER + firewall 1:400 ialah **calon saringan paling seimbang daripada laporan lama**: hasil model tertinggi antara baris ini dan drawdown lebih rendah daripada Tengri sahaja, tetapi drawdown masih lebih tinggi daripada HoldCap. Ia selari dengan keutamaan recovery kerana exit negatif ditangguhkan ketika stress gate masih selamat.

Ia **bukan setting terbaik yang sudah disahkan**: angka berasal daripada sampel Mei–18 November yang pernah digunakan, kos/margin broker belum disahkan, dan hedge masih terbuka pada akhir replay. Floating gabungan Tengri + Hedge ketika itu ialah −1,314.67 USC. Ia juga menggunakan strategi struktur/DEFER lama, bukan ujian baharu BBMA atau sizing berdasarkan margin-stress.

## Batch simulasi yang akan dijalankan apabila input pulih

Kunci perbandingan kecil dahulu, tanpa sweep luas:

- Baseline Tengri sahaja.
- HoldCap semasa sebagai rujukan drawdown.
- DEFER + firewall; ukur pada margin proxy dan margin HFM akaun sebenar secara berasingan.
- Sizing hedge: 25/50/75/100% daripada net lot semasa **berasingan** daripada tambahan per layer; sertakan satu hybrid yang lotnya minimum untuk lulus stress-margin.
- Exit recovery-first yang sama: jangan tutup rugi hanya kerana 10/15% amaran; kekalkan hanya jika margin gate dan recovery path lulus. `STRICT_CUT` 10%/15% dilaporkan sebagai sensitiviti pilihan, bukan default.
- BBMA Type 1–4 hanya boleh dibandingkan jika signal event stream Build yang dipinkan ditemui semula. Jangan menggantikannya dengan ADX/struktur dan melabel keputusan sebagai BBMA.

Lapor net P&L gabungan, P&L hedge, expectancy/PF, drawdown terapung, minimum equity/margin level/free margin, kos, jumlah campaign, re-entry, hasil posisi carry hingga tutup, kejadian amaran 10/15%, masa recovery, serta perbezaan terhadap Tengri sahaja. Mei–November kekal development/in-sample; calon pilihan mesti diuji pada holdout bebas.

## Input untuk membuka HOLD

- Arkib bid/ask tick sepadan dengan server MT4 Tengri untuk 1 Mei–18 November 2026, ditambah sejarah pemanasan daripada feed yang sama. Untuk ujian BBMA D1/H4/H1, sediakan sekurang-kurangnya 51 candle D1 tertutup sebelum 1 Mei bagi owner MA50 (praktikalnya sediakan data sejak 1 Februari); ujian berasingan yang memakai ADX H4 memerlukan warm-up ADX tersendiri. Sertakan server label, timezone, manifest/hash dan liputan tanpa jurang.
- Selesaikan residual kecil pada order asal dengan memadankan balance, closed P&L, swap/komisen, deposit/pengeluaran dan sempadan masa server yang sama. Ujian saiz semula perlu membandingkan order dengan baseline balance/flows yang turut diskalakan, bukan snapshot akaun asal.
- Salinan runner/template serta base dependency yang dipinkan dalam branch untuk ulang kaji; data akaun mentah kekal di G40.
- Spesifikasi margin/stop-out, kontrak, komisen, swap, spread, fill latency/slippage dan rejected order bagi akaun sasaran.

Build signal stream untuk kajian ini sudah dipinkan kepada Build 5.16; jangan masukkan binary/artifak legacy 4.59. Sehingga warm-up tick MT4 dan rekonsiliasi baki diselesaikan, status terbaik kekal **HOLD**.

## Semakan khusus MT4 dan aliran signal — 23 November 2026

### Aliran event BBMA ditemui, tetapi belum layak menjadi replay prestasi

Pada G40 terdapat `BBMA516_signal_events_clean_20261122.csv` dan ringkasan sumbernya. Bagi 1 Mei–18 November 2026, bilangan event yang diluluskan oleh ekstraktor ialah:

| Pair | Type 1 | Type 2 | Type 3 | Type 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| EURUSD | 18 | 0 | 18 | 35 | 71 |
| USDCHF | 24 | 0 | 23 | 36 | 83 |

Type 2 tiada dalam event log tetingkap ini; ia mesti dilaporkan sebagai sifar, bukan digabungkan dengan type lain. Ekstraktor menyatukan RE_ADMIT dengan kiraan M15 selepas D1 filter dan membuang minit yang ada konflik arah.

### Sebab data tester itu belum membuktikan feed MT4

Skrip `make_mt4_hst_from_mt5.py` menunjukkan HST yang dimasukkan ke terminal tester dibina daripada fail bar `HFMarketsGlobal-Demo4 via MT5 copy_rates_range`. Ujian MT4 terkunci pada G40 menggunakan `TestModel=2`; laporan HTML menyebut **Open prices only**, spread tetap 30 points, dan modelling quality `n/a`. Jadi Build 5.16 memang berjalan sebagai EA MQL4 dalam tester MT4, tetapi harga sejarah yang dimasukkan bukan tick sejarah daripada server MT4 Tengri dan model itu bukan replay Bid/Ask tick. Laporan tester standalone BBMA yang mempunyai order tester tidak dikira sebagai prestasi EA Hedge.

Perbandingan OHLC pada tempoh overlap, selepas penjajaran timestamp terbaik 0 jam, mengesahkan dua sumber ini bukan salinan bar yang sama:

| Data MT4 `HFMarketsSV-Demo Server` | Overlap | OHLC tepat sama | Deviasi OHLC maksimum |
|---|---:|---:|---:|
| EURUSD M15 | 2,048 bar | 504 (24.6%) | 94 points / 9.4 pip |
| EURUSD H1 | 2,816 bar | 469 (16.7%) | 182 points / 18.2 pip |
| USDCHF H1 | 2,528 bar | 541 (21.4%) | 136 points / 13.6 pip |

HST MT4 setempat juga hanya meliputi EURUSD M15 dari 19 Oktober dan H1/USDCHF H1 dari 5 Jun; H4/D1 tidak tersedia dalam folder server tersebut, USDCHF M15 tiada, dan `ticks.raw` server cuma 9,480 bytes. FXT tester EURUSD/USDCHF masing-masing 78,232 bytes. Ini tidak membuktikan tick history penuh bagi tetingkap ujian.

### Laluan data yang disemak

- [MT4 History Center](https://www.metatrader4.com/en/trading-platform/help/service/history_center) boleh memuat turun bar M1 daripada historical-data server MetaQuotes, tetapi MetaQuotes sendiri memberi amaran bahawa data itu mungkin berbeza daripada historical data broker.
- [HFM Tick Chart Trader guide](https://static.hfm.com/assets/docs/tools_hfm/premium-trader-tools/tick-chart-trader-user-guide-HFSC-en.pdf?v=70) menyatakan carta ticknya mula terkumpul apabila aplikasi bermula dan tidak memberi akses kepada tick sejarah. Ia sesuai untuk kutipan ke hadapan, bukan mengisi Februari–November 2026.
- [MT4 tester setup](https://www.metatrader4.com/en/trading-platform/help/autotrading/tester/tester_parameters) menerangkan bahawa sejarah terminal MT4 disimpan sebagai bar OHLC dan pergerakan intra-bar dimodelkan; laporan G40 yang diperiksa memang `Open prices only`.

### Keputusan dan tindakan seterusnya

Status replay kekal **HOLD**. Signal event awal sudah ditemui, tetapi feed MT4 Bid/Ask lengkap serta warm-up 51 D1 candle daripada sumber yang sama belum ada. Template comparison yang ditemui pula membandingkan ADX25 dengan RE3 dan exit H4; ia bukan runner yang mengikut lock baseline + Type 1–4 dengan exit bersama. Jangan jalankan atau label template itu sebagai ujian terkunci.

Untuk membuka gate, perlu dapatkan arkib raw Bid/Ask EURUSD dan USDCHF daripada feed MT4 `HFMarketsSV-Demo Server` bagi sekurang-kurangnya **1 Februari–18 November 2026**, dengan timestamp/server timezone dan bukti asal. Selepas itu, sahkan manifest, warm-up, ledger rekonsiliasi, kemudian sediakan runner khusus bagi baseline/Type 1–4. Tiada EA produksi diubah dan tiada trading diaktifkan.
