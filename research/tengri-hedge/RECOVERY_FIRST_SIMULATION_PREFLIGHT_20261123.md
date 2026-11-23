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

- Arkib bid/ask tick yang sepadan dengan feed MT4 Tengri, dengan sekurang-kurangnya 16 hari warm-up sebelum 1 Mei 2026 hingga 18 November 2026, serta timezone dan manifest/hash.
- Selesaikan residual kecil pada order asal dengan memadankan balance, closed P&L, swap/komisen, deposit/pengeluaran dan sempadan masa server yang sama. Ujian saiz semula perlu membandingkan order dengan baseline balance/flows yang turut diskalakan, bukan snapshot akaun asal.
- Salinan runner/template serta base dependency yang dipinkan dalam branch untuk ulang kaji; data akaun mentah kekal di G40.
- Spesifikasi margin/stop-out, kontrak, komisen, swap, spread, fill latency/slippage dan rejected order bagi akaun sasaran.

Build signal stream untuk kajian ini sudah dipinkan kepada Build 5.16; jangan masukkan binary/artifak legacy 4.59. Sehingga warm-up tick MT4 dan rekonsiliasi baki diselesaikan, status terbaik kekal **HOLD**.