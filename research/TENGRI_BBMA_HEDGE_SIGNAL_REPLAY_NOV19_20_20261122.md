# Replay signal BBMA Hedge — 19–20 Nov 2026

Tarikh rekod: 22 Nov 2026  
Branch: `research/tengri-bbma-hedge-replay-20261122`  
Status: **Selesai sebagai diagnostik signal; bukan replay P&L Hedge**

## Tujuan dan skop

Replay ini menggunakan dua hari pasaran baharu selepas cutoff data replay terdahulu untuk mengira signal Re-Entry yang dikeluarkan Build 5.16 dan menyemak gate D1/H4/M15. Ia tidak membuka pesanan; adapter tester hanya mengeksport signal.

Tempoh ini belum boleh dianggap holdout prestasi akaun: ledger Tengri yang tersedia berakhir pada 18 Nov 2026. Untuk arah hedge, snapshot posisi pada 18 Nov digunakan secara beku sepanjang dua hari tersebut. Tiada aliran posisi Tengri, perubahan net exposure atau status basket selepas tarikh itu.

## Data dan identiti

- Feed: `HFMarketsGlobal-Demo4`
- Tempoh: 19–20 Nov 2026 UTC
- Sumber: Build 5.16, tag `V516_M12_ENTRYCANDLE_GATE_20261107`
- Setiap pair mempunyai 135,796 dan 162,369 tick EURUSD; 79,880 dan 114,940 tick USDCHF pada 19 dan 20 Nov.
- Bar baharu bagi setiap pair: M15 192, H1 48, H4 12, D1 2.
- Sejarah bar yang dipulihkan bermula 2 Jan 2025 dan berakhir 20 Nov 2026. HST dihasilkan dalam direktori staging yang terasing.
- Test adapter dilancarkan satu pair setiap kali; inisialisasi lulus, tag Build 5.16 dan adapter ditemui; tiada token kegagalan tercatat.
- Folder staging dan fail mentah berada pada G40 di `C:\Trading\Tengri-Hedge-Research\TENGRI_BBMA_NOV19_20_REPLAY_20261122`.

SHA-256 log dan executable yang digunakan:

| Pair | Tester log SHA-256 | EX4 SHA-256 |
|---|---|---|
| EURUSD | `1856f3c0120023b6d4fdb40e304a24ddfe3442b8ce4b7e890257662e6854462c` | `9C0C6D6E64152415C5BBE418AF24685143CEC22DA67BA05BCB54BDEB735C00A7` |
| USDCHF | `83117ba21cb6e112856bd46118f39d16783d551a4c3770bd1b366a2a244a8d5a` | `32B0C3777EE8A7658CBB223DA142E5D6B6E045118781B2C93F38D5DB83C9B164` |

SHA-256 tick files:

| Pair / tarikh | Tick | SHA-256 |
|---|---:|---|
| EURUSD 19 Nov | 135,796 | `afc585393e784f9b03f46e20af1959ef80f6bf06d0d73cd0d326f7c1ce217752` |
| EURUSD 20 Nov | 162,369 | `f605f4f1a751dfb4bcbf6f721aa56fbe54c5173ff2cf49d8deb187c8bf156de4` |
| USDCHF 19 Nov | 79,880 | `304dd4e98cba8851674a6c117389e77f13bc655fd54fae6b665eeeaab6588086` |
| USDCHF 20 Nov | 114,940 | `1dc118ea060151b2dce804c178dd5c524ee24bbea6a8de82e6cd69fe3baf2691` |

## Keputusan signal

Enam signal unik dikesan. Gate di bawah ialah approval D1/H4/M15 daripada exporter Build 5.16. Arah hedge dibandingkan dengan snapshot net exposure 18 Nov: EURUSD net buy, maka hedge SELL; USDCHF net sell, maka hedge BUY.

| Pair | Jenis | Arah | Confirm UTC | M15 pertama | D1/H4/M15 | Sehala dengan hedge snapshot |
|---|---|---|---|---|---|---|
| EURUSD | Type 3 CSM | SELL | 19 Nov 07:00 | 19 Nov 08:00 | Lulus | Ya |
| EURUSD | Type 4 CSD | BUY | 19 Nov 14:00 | 19 Nov 15:00 | Gagal | Tidak |
| EURUSD | Type 1 | SELL | 20 Nov 02:00 | 20 Nov 03:00 | Lulus | Ya |
| USDCHF | Type 1 | BUY | 19 Nov 08:00 | 19 Nov 09:00 | Lulus | Ya |
| USDCHF | Type 4 CSD | BUY | 20 Nov 00:00 | 20 Nov 01:00 | Lulus | Ya |
| USDCHF | Type 3 CSM | SELL | 20 Nov 21:00 | 20 Nov 22:00 | Gagal | Tidak |

Ringkasan mengikut jenis:

| Jenis | Calon | Lulus D1/H4/M15 | Lulus dan sehala dengan snapshot |
|---|---:|---:|---:|
| Type 1 | 2 | 2 | 2 |
| Type 2 | 0 | 0 | 0 |
| Type 3 CSM | 2 | 1 | 1 |
| Type 4 CSD | 2 | 1 | 1 |
| **Jumlah** | **6** | **4** | **4** |

Tiada konflik BUY/SELL pada minit keputusan. Satu Type 3 EURUSD lulus; satu Type 3 USDCHF gagal. Ini hanya menunjukkan liputan signal bagi dua hari, bukan bahawa entry itu mengurangkan floating atau meningkatkan keuntungan.

## Apa yang ujian ini tidak sahkan

- ADX(14)>25, penjajaran DI dan konteks H4 Mid-BB untuk strategi calon belum disahkan dalam replay ini. Oleh itu keputusan ini bukan ujian lengkap bagi calon Type 3 + ADX/DI + H4 Mid-BB.
- Fail tick bid/ask dieksport dan di-hash, tetapi tester ini menggunakan adapter signal berasaskan bar, bukan simulasi fill Hedge pada setiap tick.
- Tiada laluan posisi Tengri selepas 18 Nov; tiada rekod entry/exit Hedge, kos komisen/swap, spread/fill sebenar, fill gagal, floating drawdown, expectancy atau profit factor.
- Sampel dua hari terlalu pendek untuk kesimpulan prestasi atau pemilihan strategi.

Maka **tiada angka P&L, expectancy atau profit factor yang patut dilaporkan** daripada replay ini. Ia tidak menggantikan ujian locked holdout yang diminta sebelum ini.

## Status projek

Replay signal dua hari: **COMPLETE / DIAGNOSTIC ONLY**.  
Replay gabungan Tengri + Hedge: **HOLD — ledger selepas 18 Nov tidak tersedia**.  
EA Hedge production tidak diubah. Tiada trading live/forward diaktifkan dan tiada branch di-merge.

Langkah seterusnya untuk replay prestasi yang sah ialah memperoleh aliran/ledger Tengri yang boleh diselaraskan sepanjang tempoh tick HFM Demo4 lengkap, kemudian menjalankan arm terkunci dengan Type 1–4 dilaporkan berasingan, exit dan kos yang sama, serta tanpa pelarasan parameter pada tempoh itu.
