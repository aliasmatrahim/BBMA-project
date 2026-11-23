# Preflight simulasi Recovery-First Tengri + Hedge — 2026-11-23

## Status

**HOLD — simulasi baharu belum dijalankan kerana input replay yang diperlukan tidak tersedia di repo atau laluan kerja G40 yang diperiksa.** Tiada angka baharu direka atau dikira daripada ringkasan sahaja. EA Tengri/Hedge tidak diubah dan tiada dagangan diaktifkan.

## Objective yang dipakai

- Utamakan margin survival.
- Kekalkan peluang recovery selagi stress-margin masih lulus dan laluan recovery yang munasabah wujud.
- Cari P&L bersih positif untuk hedge dan gabungan Tengri + Hedge selepas kos.
- Guard drawdown 10–15% ialah amaran pilihan; tiada auto-cut berdasarkan angka itu sahaja. Hard-cut hanya pembanding `STRICT_CUT`.
- Jika margin menghampiri stop-out dan tiada hedge/partial de-risk yang lulus gate, teruskan pengurangan risiko secara terkawal.

Spesifikasi penuh: `OBJECTIVE_MC_SURVIVAL_DESIGN_20261123.md`.

## Semakan input

1. Repo branch `research/tengri-bbma-hedge-replay-20261122` mengandungi objektif, laporan hasil lama, JSON ringkasan dan wrapper runner. Wrapper `high_layer_staged_replay_20261123.py` membaca template `tengri_hedge_bbma_exit_comparison_20261122.py`, tetapi template itu tiada dalam direktori GitHub yang diperiksa.
2. JSON hasil lama hanya mengandungi ringkasan/metrics, bukan equity path atau per-tick orders yang diperlukan untuk menguji recovery-first exit dan loss-guard.
3. G40 online diperiksa. Carian di bawah `D:\BBMA` tidak menemukan folder `Statement_Floating_Audit_20261119` atau template runner tersebut. Arkib `dukascopy_jetta\ticks` tidak menyediakan liputan EURUSD/USDCHF Mei–November 2026 yang diperlukan; laluan USDCHF tidak wujud di bawah arkib itu. Sumber tick alternatif lengkap tidak dikenal pasti dalam semakan ini.
4. Carian Library menemukan laporan terdahulu tetapi bukan ledger mentah atau tick archive yang boleh dimasukkan semula ke simulator.
5. Laporan terdahulu menyebut 1,357 order, 227 snapshot balance, dan 13 aliran tunai; fail/baris sumber sebenar untuk merekonstruksi urutan itu tidak ditemui pada preflight ini.

Maka replay baharu dengan data yang sama, pengiraan margin broker, kos sebenar, dan posisi carry-to-recovery belum boleh diulang secara sah.

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

- Ledger asal statement Tengri EURUSD + USDCHF dan aliran tunai/snapshot baki (1,357 order, 227 snapshot, 13 flows) atau eksport semula yang boleh direkonsiliasi.
- Bid/Ask tick penuh kedua-dua pair, termasuk warm-up sebelum 1 Mei 2026 hingga 18 November 2026, dengan manifest/hash dan timezone.
- Template runner serta versi signal/build yang tepat; konflik identiti Build 5.16/4.59 mesti diselesaikan.
- Kontrak/leveraj/margin hedge/stop-out, komisen, swap, spread, fill latency/slippage/rejection yang sepadan dengan akaun sasaran.

Sehingga item itu tersedia, status terbaik yang boleh dipertahankan ialah **DEFER + firewall 1:400 sebagai calon lama untuk diuji semula**, bukan tetapan yang disyorkan untuk diaktifkan.
