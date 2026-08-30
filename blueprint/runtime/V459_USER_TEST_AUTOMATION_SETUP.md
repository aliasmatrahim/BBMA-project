# BBMA v4.59 — Setup Sekali, Ujian Automatik R1–R6

Runner ini mengautomasi bahagian yang selamat untuk diautomasi: pengesahan build v4.59, pembinaan varian, native compile, pelancaran profil MT4, pengesahan akaun demo, satu clean restart pada checkpoint R1/R2, pengumpulan log, analisis, status R1–R6 dan ZIP bukti.

Ia tidak mencipta akaun broker, menyimpan login/kata laluan atau memaksa market menghasilkan setup BBMA. Jika bukti belum cukup selepas tempoh monitor, status ialah `INCOMPLETE`; jalankan semula dan bukti baharu akan digabungkan dengan bukti lama.

## Apa yang user perlu sediakan sekali sahaja

1. Pasang satu salinan MT4 khas untuk ujian BBMA. Jangan guna terminal akaun real.
2. Buka akaun **demo**, login dalam terminal itu dan pastikan `AutoTrading` boleh dihidupkan.
3. Salin `v459_user_test_settings.example.json` sebagai `v459_user_test_settings.json`.
4. Isi empat path sahaja:
   - `terminal_path`: lokasi `terminal.exe`.
   - `metaeditor_path`: lokasi `metaeditor.exe`.
   - `data_path`: folder yang dipaparkan oleh MT4 melalui **File → Open Data Folder**.
   - `work_root`: folder output ujian, contohnya `C:\BBMA-V459-UserTest`.
5. Jika MT4 dipasang dalam portable mode, kekalkan `portable_mode: true`. Jika tidak, tukar kepada `false`.

Jangan masukkan nombor akaun, login, server atau kata laluan dalam fail settings. Validator akan menolak medan credential.

## Sediakan program dan profil MT4

1. Tutup terminal MT4 khas itu.
2. Jalankan `PREPARE_BBMA_USER_TESTS.cmd`. Ia membina dan compile dua program stabil:
   - `BBMA_EA_V459_USERTEST`
   - `V459_Runtime_Observer`
3. Buka MT4 secara manual dan login akaun demo.
4. Cipta profil `BBMA_V459_DEMO_PREFLIGHT` yang mengandungi **observer sahaja**. Jangan lampirkan EA trading dalam profil ini. Tandakan `Allow live trading` pada observer supaya ia boleh melaporkan status permission; observer telah diperiksa dan tidak mempunyai arahan broker-write.
5. Cipta enam profil dengan nama tepat yang terdapat dalam fail settings: R1 hingga R6.
6. Dalam setiap profil R1–R6:
   - Lampirkan `BBMA_EA_V459_USERTEST` pada satu chart.
   - Lampirkan `V459_Runtime_Observer` pada chart kedua.
   - Untuk R1, R2, R3, R4 dan R6, load `v459_user_test_common.set` pada EA.
   - Untuk R5, load `v459_user_test_r5.set` pada EA. Preset ini mengaktifkan `LOCK_ONE_POSITION` untuk bukti TradeLock.
   - Pastikan `StrategyID=1` dan `InstanceID=0` sama pada EA dan observer.
   - Benarkan live trading pada EA. “Live trading” MT4 mesti dibenarkan, tetapi runner tetap menolak akaun real melalui `Demo=Y`.
   - Tandakan juga `Allow live trading` pada observer supaya `TradeAllowed=Y` boleh disahkan; observer tidak boleh membuka/ubah/tutup order.
7. Simpan semua tujuh profil dan tutup MT4 secara normal.

## Jalankan automasi

Klik dua kali `RUN_BBMA_USER_TESTS.cmd`.

`AUTO` memilih stage pertama yang belum PASS dan mematuhi urutan ketat R1 → R6. Untuk setiap sesi, runner:

1. mengesahkan blob dan SHA-256 canonical v4.59;
2. membina varian yang betul tanpa mengubah source canonical;
3. compile EA dan observer dengan 0 error/0 warning;
4. membuka profil observer-only dan mengesahkan `Demo=Y` sebelum profil trading dibuka;
5. membuka profil stage yang betul dan mengesahkan semula `Demo=Y`, `Connected=Y`, `TradeAllowed=Y`;
6. membuat maksimum satu clean restart apabila checkpoint R1/R2 dan order terbuka dikesan;
7. menutup MT4 secara bersih pada akhir sesi — tiada force-kill;
8. mengumpul bukti kumulatif, menganalisisnya dan menghasilkan ZIP.

Kod keluar runner:

| Kod | Status | Maksud |
|---:|---|---|
| 0 | PASS | Stage lengkap atau semua R1–R6 sudah PASS |
| 2 | FAIL | Bukti menunjukkan pelanggaran |
| 3 | BLOCKED | Safety/setup/runtime menghalang ujian |
| 4 | INCOMPLETE | Sesi sah, tetapi market belum menghasilkan semua bukti |

Fail utama berada di bawah `work_root`:

- `state.json`: kemajuan R1–R6;
- `evidence\R*`: log kumulatif setiap stage;
- `runs\R*\<masa>`: manifest, report analyzer, stage report, compile log dan ZIP bukti.

## Had automasi

- Akaun demo dan login perlu dibuat sendiri kerana credential tidak boleh diurus oleh repository/ChatGPT.
- Profil MT4 perlu disimpan sekali secara manual kerana MT4 menyimpan susunan chart dan input EA dalam profil terminal.
- Setup BBMA bergantung pada pergerakan market sebenar; runner boleh menunggu dan menyambung bukti, tetapi tidak boleh mencipta signal tanpa membatalkan tujuan user test.
