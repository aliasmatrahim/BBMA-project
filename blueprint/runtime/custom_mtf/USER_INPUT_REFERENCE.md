# Rujukan input BBMA Custom MTF

Build **6.15**, branch `feat/custom-mtf-v1-20261108`, checkpoint sumber `6e76d8707d3294df80c660d2f775bd27c221242f`. Rujukan ini menerangkan konfigurasi yang tersedia dalam Draft PR #303. Auto-entry custom kekal OFF. Owner yang belum disahkan kekal unavailable.

## Timeframe dan signal

| Timeframe | Input timeframe | Default | Senarai signal | Default |
|---|---|---|---|---|
| M1 | `CustomTF_M1` | `true` | `CustomSignals_M1` | `""` |
| M5 | `CustomTF_M5` | `true` | `CustomSignals_M5` | `""` |
| M15 | `CustomTF_M15` | `true` | `CustomSignals_M15` | `""` |
| M30 | `CustomTF_M30` | `true` | `CustomSignals_M30` | `""` |
| H1 | `CustomTF_H1` | `true` | `CustomSignals_H1` | `""` |
| H4 | `CustomTF_H4` | `true` | `CustomSignals_H4` | `""` |
| D1 | `CustomTF_D1` | `true` | `CustomSignals_D1` | `""` |

Senarai signal menerima kod dipisahkan koma, contohnya `MOM,CSA`. Ruang di tepi setiap kod dibuang dan huruf dinormalisasi. Kod yang dikenali parser ialah `RE`, `RE1`, `RE2`, `RE3`, `RE4`, `EXT`, `MHV`, `MLV`, `CSA`, `CSAK`, `MOM`. Kod yang dikenali masih tertakluk kepada semakan availability setiap pasangan timeframe dan signal.

## Lima slot

| Slot | Enable (default `false`) | Context (default `""`) | Trigger (default `""`) | Symbols (default `"ALL"`) |
|---|---|---|---|---|
| 1 | `Custom1_Enable` | `Custom1_Context` | `Custom1_Trigger` | `Custom1_Symbols` |
| 2 | `Custom2_Enable` | `Custom2_Context` | `Custom2_Trigger` | `Custom2_Symbols` |
| 3 | `Custom3_Enable` | `Custom3_Context` | `Custom3_Trigger` | `Custom3_Symbols` |
| 4 | `Custom4_Enable` | `Custom4_Context` | `Custom4_Trigger` | `Custom4_Symbols` |
| 5 | `Custom5_Enable` | `Custom5_Context` | `Custom5_Trigger` | `Custom5_Symbols` |

Context dan Trigger masing-masing menggunakan `TF:SIGNAL`. Contoh sintaks parser ialah `H4:MOM AND (H1:CSA OR H1:CSAK)` untuk Context dan `M15:RE1` untuk Trigger. Contoh ini menerangkan bentuk formula. Ia belum tersedia sebagai preset entry pada Build 6.15.

- `AND` menggabungkan kumpulan. `OR` boleh digunakan sebagai satu senarai alternatif atau dalam kurungan di dalam formula `AND`. Operator bercampur tanpa kumpulan dan kurungan bersarang ditolak.
- Had keseluruhan ialah tujuh atom bagi Context dan Trigger dalam satu slot. Atom berulang dalam formula yang sama ditolak.
- Slot OFF boleh dibiarkan kosong. Slot ON perlu melepasi semakan kedua-dua formula, TF, signal dan availability bagi setiap atom, termasuk semua alternatif `OR`.
- Build ini memulakan semua 77 sel availability konfigurasi sebagai `false`. Tetapan `CustomTF_*` dan `CustomSignals_*` sahaja belum membolehkan slot aktif. Simpan kelima-lima slot pada `false` untuk konfigurasi semasa.

## Skop simbol

| Input | Default | Kegunaan |
|---|---|---|
| `CustomSymbolMode` | `CUSTOM_CHART_ONLY` | Simbol carta. Pilihan lain ialah `CUSTOM_MARKET_WATCH` untuk snapshot Market Watch atau `CUSTOM_LIST` untuk senarai manual. |
| `CustomSymbolList` | `""` | Isi senarai dipisahkan koma apabila memilih `CUSTOM_LIST`, contohnya `GBPUSD,EURUSD`. |

Input `Custom1_Symbols` hingga `Custom5_Symbols` menggunakan `ALL` atau subset daripada skop simbol custom selepas resolver broker menentukan simbol sebenar. Subset di luar skop atau simbol yang gagal dipadankan ditolak.

## Sebab konfigurasi ditolak

| Kod | Semakan |
|---|---|
| `TIMEFRAME_DISABLED` | TF formula ditutup. |
| `SIGNAL_DISABLED` | Kod belum disenaraikan dalam `CustomSignals_*` untuk TF itu. |
| `SIGNAL_UNAVAILABLE` | Sel owner untuk TF dan signal belum tersedia. |
| `SYMBOL_UNRESOLVED` / `SYMBOL_OUTSIDE_UNIVERSE` | Resolver gagal memadankan simbol atau simbol berada di luar skop custom. |

Sumber pengesahan ialah `CustomInputs.mqh`, `CustomSymbolInputs.mqh`, `CustomFormula.mqh`, `CustomSlot.mqh` dan `CustomSymbols.mqh` di `blueprint/source/custom_mtf/`.
