# BBMA Professional EA — Custom Multi-Timeframe Auto-Entry

**Draf reka bentuk penuh v1 · 7 November 2026**

Status: **DRAFT FOR REVIEW — belum dilaksanakan, belum compile/runtime verified.**

## 1. Tujuan dan sempadan

EA MT4 dapat mengesan signal BBMA pada M1, M5, M15, M30, H1, H4 dan D1; membina kombinasi pilihan pengguna; membuka trade secara automatik selepas pengesahan; dan melabel signal pada chart apabila diaktifkan.

Definisi signal kekal mengikut accepted BBMA Core. Kebebasan konfigurasi mengubah komponen kombinasi, timeframe dan pengurusan trade; ia tidak membenarkan pengguna menukar definisi asas signal atau menjadikan HOLD/UNRESOLVED executable. Formula custom dilabel CUSTOM, bukan REM/RRE/REE rasmi. Tiada RSI, MACD, Stochastic, ADX atau strategi luar ditambah.

Dokumen ini membezakan **DIPERSETUJUI** (keputusan perbincangan), **CADANGAN** (engineering design untuk kelulusan), dan **GATE** (bukti/kontrak wajib sebelum execution). Nilai contoh bukan tetapan trading yang telah diuji. Tiada jaminan keuntungan dibuat.

## 2. Keperluan yang dipersetujui

| ID | Keperluan |
| --- | --- |
| R01 | Tujuh TF: M1/M5/M15/M30/H1/H4/D1; pilihan ON/OFF setiap TF dan setiap signal. |
| R02 | Lima slot Custom1–Custom5; maksimum tujuh komponen aktif keseluruhan setiap slot. Tidak wajib menggunakan semua komponen. |
| R03 | Format `TF:SIGNAL`; Context dan Trigger berasingan; gabungan akhir `(Context) AND (Trigger)`. |
| R04 | AND bagi kumpulan wajib; OR bagi alternatif dalam kumpulan. Tiada formula bebas bertingkat pada versi pertama. |
| R05 | Auto-entry selepas trigger candle tertutup, component validation, risk approval dan execution preflight. |
| R06 | Tiga profil exit setiap slot: BBMA_STRUCTURAL, STRUCTURAL_RR, FIXED_DISTANCE; satu aktif pada satu masa. |
| R07 | Fixed lot atau risk % bagi setiap slot. |
| R08 | Had posisi setiap slot/simbol boleh diubah; had simbol keseluruhan dan portfolio turut terpakai. |
| R09 | Pilihan hedging disediakan. |
| R10 | Senarai simbol utama, dan ALL atau subset simbol bagi setiap slot. |
| R11 | Label chart ON/OFF secara berasingan daripada trading. |

## 3. Asas semakan dan kesan kepada architecture

Semakan melalui GitHub connector pada sesi penyediaan draf mengesahkan README masih meroute source kepada `d1-owner-dev:blueprint/source/BBMA_EA.mq4`. README, CURRENT, MASTER_QUEUE dan SOURCE_INDEX telah dibaca. CURRENT/MASTER_QUEUE yang dikembalikan masih bertarikh September; source yang diperiksa mempunyai header Version 5.1.5. Ini **bukan pengesahan bahawa Build 5.15 ialah calon deployment terkini**, dan bukan alasan mengulang kerja verified. Sebelum implementasi, branch head, PR aktif, release identity, worktree dan runtime mesti dipulihkan semula. Dokumen ini tidak mengubah queue.

Rujukan live yang diperiksa:

- [README](https://github.com/aliasmatrahim/BBMA-project/blob/main/README.md)
- [SOURCE_INDEX](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/docs/references/SOURCE_INDEX.md) dan accepted Core yang diroute olehnya.
- [M13 collector](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md)
- [M15 authority](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md)
- [M17 exit resolution](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md)
- [M21 sizing](https://github.com/aliasmatrahim/BBMA-project/blob/d1-owner-dev/blueprint/contracts/M21_MONEY_MANAGEMENT_CONTRACT.md)

M13 semasa mengehadkan canonical signature kepada TF tertentu. M15 semasa mengikat keputusan kepada closed-M15 cycle dan D1 strategic owner. Source yang dibaca mempunyai OnTick/OnTimer menuju satu OnTickMain, yang memanggil ProcessPair apabila IsNewCandle lulus. Oleh itu membaca M1 tidak dengan sendiri memberikan authority entry M1.

**CADANGAN:** satu laluan canonical yang mengekalkan signature dan eligibility semasa, serta laluan CUSTOM dengan kontrak engineering yang nyata. Kedua-duanya berkongsi detector, validation, risk dan execution owners. Tiada duplicate EA, detector atau NMJE execution engine.

### Pilihan architecture yang dipertimbangkan

| Pilihan | Kesan | Keputusan |
| --- | --- | --- |
| Tambah semua suis tetapi kekalkan penilaian setiap M15 | Perubahan lebih kecil tetapi trigger M1 boleh lewat sehingga beberapa minit. | Tidak sesuai untuk sasaran custom auto-entry pantas. |
| Peluaskan orchestrator kepada event candle tertutup setiap TF; M15 kekal final entry owner | Menyokong trigger M1 dengan owner tunggal; memerlukan pindaan kontrak dan regression luas. | **Disyorkan; menepati arah perbincangan, pindaan tepat masih perlu kelulusan draf.** |
| EA atau detector berasingan untuk setiap slot/TF | Pengasingan nampak mudah tetapi menggandakan state, pengiraan dan execution ambiguity. | Ditolak. |

Maksud M15 dalam dokumen ini ialah **Module 15**, manakala TF M15 ialah candle 15 minit. Pindaan yang dicadangkan mengekalkan Module 15 sebagai sole final authority, tetapi meluaskan cadence CUSTOM daripada TF M15 kepada event TF trigger. Ia tidak boleh diperkenalkan sebagai patch biasa yang kononnya mengekalkan clock lama sepenuhnya.

## 4. Signal registry dan suis

| Shortform input | Maksud | Syarat sebelum digunakan |
| --- | --- | --- |
| RE | Mana-mana Re-Entry Type 1–4 yang owner sahkan | Pilih identity jenis sebenar secara deterministic; tiada pematangan baharu oleh parser. |
| RE1/RE2/RE3/RE4 | Re-Entry jenis khusus | Lifecycle dan entry window jenis tersebut mesti disahkan. |
| EXT | Extreme | Context menggunakan tahap matang yang ditakrifkan; trigger hanya exact entry-ready, bukan RAW. |
| MHV, MLV | Nama domain yang diroute kepada M09 | Jangan anggap sinonim tanpa accepted mapping; kod yang belum resolved ditolak. |
| CSA, CSAK | Istilah Candle Arah/Candle Arah Kukuh | Mapping kepada enum/detector sedia ada perlu reconciliation; jangan guna definisi lama daripada nama sahaja. |
| MOM | Momentum | Exact canonical momentum/CSM mapping perlu disahkan; bukan sekadar close di luar BB. |

Senarai ini ialah vocabulary produk yang dicadangkan, bukan dakwaan semua signal pada semua TF telah siap. Setiap registry row mempunyai owner module, canonical type, supported TF, maturity, context/trigger eligibility, evidence status dan reason jika unavailable. Hanya row VERIFIED/accepted yang lengkap boleh dipilih untuk auto-entry. HOLD tidak boleh dilepaskan oleh suis.

**CADANGAN suis:** `TF_Enable_M1` ... `TF_Enable_D1`, dan `SignalUse_M1_RE` ... bagi matriks signal × TF; `ShowSignals` serta filter paparan berasingan. Registry mengelakkan input alias menghasilkan detector berganda.

OFF bermaksud output tidak boleh dipilih sebagai komponen custom baharu. Dependency dalaman yang diperlukan untuk mengira signal lain atau mengurus posisi terbuka tidak dihentikan. Slot yang merujuk TF/signal OFF ialah configuration error; sistem tidak memadam syarat itu secara senyap daripada formula. Mengubah setting tidak menghapus protective management posisi sedia ada.

## 5. Formula lima slot

### Syntax versi pertama

Atom berbentuk `TF:SIGNAL`. Huruf dinormalisasi kepada uppercase; ruang dibenarkan. Setiap field ialah kumpulan atom yang disambung AND; satu kumpulan boleh mengandungi alternatif OR. Kurungan hanya untuk satu tahap kumpulan OR, bukan arbitrary nesting.

Contoh sah:

```text
Context = D1:RE AND H4:RE
Trigger = M15:MOM OR M5:MOM

Context = D1:RE AND (H4:RE OR H1:RE)
Trigger = M5:MOM AND M1:MOM
```

Formula lengkap sentiasa `Context AND Trigger`. OR dalam Trigger tanpa kurungan luar diterima kerana field itu sendiri sudah bersempadan. Context dan Trigger mesti mempunyai sekurang-kurangnya satu atom dalam versi pertama; single-signal standalone custom belum termasuk skop dipersetujui. Maksimum tujuh **kemunculan atom** merentas kedua-dua field; pendua exact dalam field ditolak, bukan dianggap confirmation tambahan.

Tidak sah: TF tidak dikenali, kod unresolved, kurungan bertingkat, `NOT`, formula kosong, OR dengan operand hilang, komponen disabled, atau lebih tujuh atom. Validation mengembalikan slot, field, posisi token dan sebab. Default yang dicadangkan: sebarang slot enabled yang invalid menyebabkan init ditolak; slot OFF boleh mempunyai field kosong.

### Semantics

- Context = state semasa yang masih owner-valid pada waktu keputusan, bukan signal yang pernah muncul dahulu.
- Trigger = confirmation event baharu yang masih dalam entry window sumber. Tiada generic TTL bagi semua signal.
- Untuk trigger AND berbilang TF: semua komponen mesti entry-eligible pada waktu yang sama dan sekurang-kurangnya satu identity baru disahkan dalam processing event itu. Kehadiran signal sejarah tidak memadai.
- Untuk OR, simpan branch/witness yang benar-benar memenuhi formula. SL source dan dedup mesti mengikat witness yang dipilih, bukan mengambil komponen dari branch yang gagal.
- Formula dinilai berasingan untuk BUY dan SELL. BOTH membenarkan kedua-dua penilaian, bukan campuran BUY/SELL dalam formula sama.
- Semua timeframe menggunakan maklumat yang tersedia pada decision time; historical label tidak boleh menjadi look-ahead.

**CADANGAN D1 gate:** custom juga mengekalkan M11 D1 strategic-direction gate semasa sebagai default wajib. Tidak memasukkan D1 dalam formula tidak mematikannya. Custom setup tidak secara automatik mendapat exception countertrend. Jika pengguna mahu bypass, ia memerlukan keputusan architecture/source berasingan.

## 6. Scheduler, data dan state

Satu orchestrator mengesan perubahan latest closed candle setiap simbol/TF. Tiada tujuh EA atau tujuh independent execution clocks. Event pada timestamp sama diproses dalam satu batch: refresh data dan owner TF tinggi dahulu, kemudian TF rendah, kemudian formula, M15 final authority, M16 revalidation dan downstream risk/execution.

Signal owners dikira sekali bagi `(symbol, TF, closed-bar identity)`. Slot berkongsi immutable snapshot; setiap slot menyimpan formula state sendiri. State key mesti merangkumi resolved symbol, TF, signal type, direction dan owner event/lifecycle ID. Pengiraan tidak boleh menggunakan array satu simbol untuk simbol lain.

OnTick dan timer hanya pencetus kerja pada orchestrator tunggal, dengan reentrancy guard. Timer tidak boleh mencipta candle, harga atau confirmation. Target ialah penilaian pada peristiwa pertama yang layak selepas candle benar-benar ditutup, bukan jaminan fill tepat pada detik penutupan.

M06 mengesahkan warm-up/indikator dan cross-TF coverage. Data hilang/stale, quote tidak sah atau history belum siap menyebabkan simbol terjejas WAIT_DATA; posisi sedia ada terus diurus. Warm-up mencukupi dikira daripada dependency sebenar, bukan satu angka rawak untuk semua signal.

Selepas reconnect/restart, candle terlepas boleh diproses untuk membina state, tetapi trigger sejarah tidak dihantar semula sebagai order baharu. Entry memerlukan event live/tester semasa yang sah selepas recovery selesai. Registry order yang ambiguous perlu reconcile dahulu.

## 7. Simbol dan scope konfigurasi

```text
SymbolMode = CUSTOM_LIST
SymbolList = XAUUSD,GBPUSD,EURUSD,USDJPY
Custom1_Symbols = ALL
Custom2_Symbols = XAUUSD
Custom3_Symbols = GBPUSD,EURUSD
```

Mode utama: CHART_ONLY, MARKET_WATCH, CUSTOM_LIST. ALL bagi slot bermaksud semua ahli universe utama yang telah resolved, bukan semua simbol broker. Slot subset mesti berada dalam universe utama; typo/out-of-universe ialah init error.

Symbol resolver menyokong suffix/prefix melalui pemetaan broker yang deterministic. Jika beberapa simbol sepadan, gunakan override explicit; jangan pilih secara rawak. Exact resolved name, specification, trading availability dan tick freshness direkodkan.

**CADANGAN MARKET_WATCH:** freeze universe pada init supaya perubahan Market Watch di tengah sesi tidak mengubah skop trading secara senyap; refresh melalui reinit. Perubahan universe tidak menanggalkan management posisi yang sudah dimiliki EA. Semua simbol dalam satu slot menggunakan formula, exit profile dan sizing slot yang sama; tuning berasingan memerlukan slot lain atau konfigurasi EA berasingan yang tidak bertindih ownership.

## 8. Candidate, duplicate dan arbitration

Flow: Detection → Candidate → Confirmation → Combination → Validation → Risk Approval → Execution → Trade Lifecycle. State CONFIRMED, READY, SELECTED, RISK_APPROVED, EXECUTED, VOID, EXPIRED dan SUPERSEDED berbeza. Status formula benar bukan broker order.

**CADANGAN:** satu final new-entry decision bagi satu simbol dalam satu event batch. Jika beberapa slot memenuhi setup sama dengan trigger identity sama, hanya satu order dihantar dan semua matching slot direkod sebagai attribution. Slot primary ditentukan secara engineering: `CustomN_Priority` kecil dahulu, kemudian slot ID; ini bukan ranking kualiti BBMA.

Dedup mempunyai dua aras: identity trigger/component fizikal merentas slot, dan identity decision execution/retry. Formula/configuration revision, winning OR witness, source IDs, direction dan symbol dibekukan. Menukar nama slot tidak menjadikan event lama entry baharu. Bukti consumed trigger dipersist merentas restart. Rejected/expired trigger tidak boleh menunggu tanpa had hingga cap portfolio lapang; entry window pemilik tetap wajib.

Had posisi >1 membenarkan event baharu yang benar-benar layak, bukan multi-order daripada event sama. Re-entry memerlukan trigger identity baharu; tiada grid/martingale ditambah oleh reka bentuk ini.

### Aturan consumption trigger yang dicadangkan

Dedup tidak memakan seluruh context D1/H4 selama-lamanya. Setiap trigger mempunyai exact owner event identity; setiap decision memilih satu **fresh anchor event** daripada witness yang memenuhi formula. Untuk trigger AND, event baharu yang melengkapkan kumpulan menjadi anchor; komponen lain boleh kekal eligible mengikut owner tetapi tidak menjadi fresh sekali lagi. Jika beberapa event baharu wujud dalam batch sama, anchor dipilih mengikut confirmation timestamp kemudian susunan canonical `(TF, signal type, owner ID)`; susunan ini engineering bookkeeping sahaja.

Sebelum submission, reserve semua fresh anchor event yang layak daripada formula yang memenuhi batch tersebut bagi simbol/arah itu, termasuk matching slot dan alternatif OR serentak. Selepas execution disahkan, tandakan event-event itu consumed bersama winning decision/witness dalam journal atomic. Ini menghalang losing slot daripada menghantar semula event yang sama pada tick seterusnya. Jika submission ambiguous, reservation kekal HOLD sehingga reconcile. Jika terbukti tiada fill, retry hanya mengikut kontrak execution, revalidation dan entry window asal; ia bukan trigger baharu.

Event baru pada candle/owner ID berbeza boleh menghasilkan entry seterusnya apabila cap membenarkan, walaupun context D1/H4 sama. Contoh: Momentum M1 dan M5 yang sah serentak dalam batch pertama menghasilkan satu order; Momentum M5 yang hanya disahkan lima minit kemudian ialah event baharu dan boleh menghasilkan order kedua. Dengan itu OR bukan bermaksud satu trade sahaja bagi keseluruhan lifecycle context. Jika pengguna mahu satu trade sepanjang parent lifecycle, itu ialah polisi tambahan yang belum termasuk versi ini.

Contoh overlap AND: trigger `M5:MOM AND M1:MOM` lengkap apabila M1 event B baru tiba dan M5 event A masih entry-eligible. B ialah anchor; A tidak boleh sendirian digunakan sebagai anchor baru selepas restart. M1 event C kemudian boleh melengkapkan formula lagi hanya jika A masih eligible menurut owner dan C benar-benar fresh. Journal mengikat consumption kepada physical anchor event, bukan nama slot/config hash sahaja, supaya menyalin slot tidak memintas dedup.

Jika dua arah bersaing dalam batch yang sama: canonical mode mengekalkan aturan konflik sedia ada; custom mode mencadangkan block kedua-dua arah bagi batch tersebut dan log CONFLICT. Hedging ON tidak bermakna dua arah mesti dibuka serentak.

## 9. Exit, SL/TP dan lifecycle

| Mode | SL | TP | Authority |
| --- | --- | --- | --- |
| BBMA_STRUCTURAL | Struktur dari source component yang dipilih dan owner-valid | Destination/lifecycle yang approved untuk setup itu | Canonical mapping yang diterima; tidak diteka daripada TF sahaja. |
| STRUCTURAL_RR | Struktur daripada component/TF pilihan | Entry ± RR × jarak hard SL | Engineering management profile. |
| FIXED_DISTANCE | Jarak input daripada execution reference | Jarak input daripada execution reference | Engineering management profile. |

Untuk structural mode, `SLSource` dan `TPSource` perlu menyebut atom sebenar, contohnya `H4:RE`, bukan sekadar H4. Source mesti menjadi sebahagian witness formula yang lulus. Jika RE wildcard memenuhi beberapa jenis, identity sebenar dan pemilihan deterministic direkodkan. Tidak semua signal menyediakan structural SL/TP. Tiada fallback senyap kepada swing rawak, TF lain atau fixed distance.

Jika approved TP source tiada untuk custom combination, BBMA_STRUCTURAL ditolak sebagai unsupported profile; pengguna boleh memilih RR/distance. Struktur lifecycle dan source buffers diwarisi daripada kontrak current owner, bukan formula wick lama yang mungkin sudah superseded.

**CADANGAN unit fixed distance:** POINTS atau PRICE sahaja, explicit; PRICE 1.00 bermaksud beza harga 1.00, POINTS 100 ialah 100 broker points. Elakkan istilah pip universal untuk emas/CFD. Tick size, digits, quote side dan stop constraints disahkan bagi setiap simbol. Dalam RR mode, jarak menggunakan normalized final hard SL sebelum sizing; TP dibina M17, bukan M21.

Level/source/exit policy dibekukan dalam TradePlan. M17 owns geometry, M21 sizes sahaja. Harga berubah sebelum OrderSend memerlukan preflight dan snapshot baharu melalui owner; execution tidak boleh melebarkan SL untuk memaksa acceptance. Risiko/fill deviation dikawal melalui kontrak execution dan tidak dijanjikan sifar slippage.

**CADANGAN lifecycle:** tiga mode berkongsi protective management. Dynamic canonical exits hanya berjalan jika exact thesis/owner mapping tersedia dan dipilih; RR/distance tidak mewarisi arbitrary BBMA close yang tidak dinyatakan. Emergency protection mempunyai keutamaan; kemudian lifecycle exit yang enabled, BE, trailing. SL tidak dilonggarkan. BE/trailing optional, default OFF; trigger berasaskan initial R yang dibekukan. Offset/step ialah engineering input. Menukar konfigurasi tidak menukar profile trade lama secara retroaktif.

## 10. Sizing, risiko, posisi dan hedging

```text
Custom1_SizeMode = RISK_PERCENT
Custom1_RiskPercent = 1.0
Custom2_SizeMode = FIXED_LOT
Custom2_FixedLot = 0.01
```

M21 menggunakan satu frozen broker/equity/decision snapshot. Risk money = frozen equity × percent/100. Risk per lot menggunakan jarak entry–SL, tick size dalam unit harga dan tick value. Auto lot dibundarkan ke bawah mengikut lot step; di bawah minimum atau di luar had ditolak, bukan dipaksa min/cap secara senyap. Fixed lot yang tidak broker-valid ditolak dan tidak dinormalisasi kepada saiz lain.

Risk % ialah bagi **setiap trade**, bukan dibahagi automatik antara simbol. 1% bagi empat simbol boleh menggunakan sekitar 4% stop risk, tertakluk cap portfolio. Risk money berasaskan hard SL ialah anggaran; gap/slippage boleh melebihi angka tersebut. Tiada dakwaan mengira kos broker tepat sebelum metadata kos disahkan.

Had yang dicadangkan: `CustomN_MaxPositionsPerSymbol`, `MaxPositionsPerSymbol`, `MaxPositionsPortfolio`, `MaxPortfolioRiskPercent`; nilai operasi belum dipilih. Semua cap diperiksa bersama reserved/in-flight exposure supaya dua decision tidak menggunakan bajet sama. Scope default: semua posisi milik deployment EA ini pada akaun, merentas lima slot dan canonical/custom; bukan manual/EA luar yang tidak dapat dibuktikan ownership. Margin check tetap account-wide. Unknown risk pada posisi owned menyebabkan new entry HOLD, bukan dianggap sifar.

Hedging OFF (default cadangan): entry opposite kepada posisi owned pada simbol sama disekat. Hedging ON: opposite entry daripada trigger baharu boleh diterima jika broker/account menyokong dan semua cap lulus. BUY/SELL gross stop risk dijumlah; jangan net menjadi sifar. Hedging tidak membuka position pair secara automatik dan tidak memintas M11 gate. D1 gate semasa boleh menyebabkan sebahagian opposite custom entry tidak eligible walaupun hedging ON.

Posisi perlu key DeploymentID, stable symbol identity, slot attribution dan ticket tanpa collision Magic. Broker comment bukan satu-satunya identity store. Multi-instance duplicate ownership ditolak/HOLD; restart tidak mencipta instance ownership baharu bagi order lama.

## 11. Contoh input produk

**Ilustrasi sahaja, bukan fail .set atau code MQL4 siap.** Input tambahan bukan arahan deployment.

```text
EngineMode = CUSTOM
ExecutionMode = MONITOR_ONLY
SymbolMode = CUSTOM_LIST
SymbolList = XAUUSD,GBPUSD,EURUSD,USDJPY
AllowHedging = false
ShowSignals = true

Custom1_Enable = true
Custom1_Name = D1_H4_RE_MOM
Custom1_Symbols = ALL
Custom1_Context = D1:RE AND H4:RE
Custom1_Trigger = M15:MOM OR M5:MOM
Custom1_Direction = BOTH
Custom1_Priority = 1
Custom1_ExitMode = STRUCTURAL_RR
Custom1_SLSource = H4:RE
Custom1_RR = 2.0
Custom1_SizeMode = RISK_PERCENT
Custom1_RiskPercent = 1.0
Custom1_MaxPositionsPerSymbol = 1
Custom1_BE_Enable = false
Custom1_Trail_Enable = false

Custom2_Enable = false
Custom3_Enable = false
Custom4_Enable = false
Custom5_Enable = false
```

EngineMode dicadangkan CANONICAL, CUSTOM atau BOTH. BOTH melalui candidate collector dan authority yang sama, bukan dua OrderSend engines. ExecutionMode MONITOR_ONLY atau AUTO_ENTRY; produk menyokong auto-entry tetapi contoh awal kekal monitor sehingga acceptance. Tiada default deployment cap risiko dianggap telah dipersetujui.

## 12. Chart label dan Setup Monitor

Signal rendering hanya membaca snapshots authoritative. Filter: chart-TF sahaja atau selected TF, selected signals, BUY/SELL, confirmed sahaja atau candidate+confirmed. Label minimum: symbol, TF, type, direction, status, formation time dan confirmation time apabila berbeza. Candidate yang void tidak dipadam untuk mencantikkan sejarah; status boleh ditanda void/expired.

CADANGAN: label atas chart hanya untuk simbol chart itu; simbol lain dalam Setup Monitor/table. Untuk higher-TF label, gunakan masa source sebenar dan tooltip TF; jangan letak pada candle kecil lebih awal daripada confirmation. Had bilangan object/lookback boleh diinput; cleanup menyentuh object namespace EA sahaja. Mematikan label tidak mengubah eligibility/trade.

Setup Monitor setiap slot/simbol menunjukkan WAIT_DATA, WAIT_CONTEXT, WAIT_TRIGGER, READY, BLOCKED_RISK, BLOCKED_LIMIT, CONFLICT, EXECUTED atau INVALID_CONFIG bersama sebab. Statistik berdasarkan closed trades dengan attribution primary yang jelas; slot padanan sekunder dilaporkan sebagai match, bukan profit diganda.

## 13. Modul dan tanggungjawab

| Owner | Kesan reka bentuk |
| --- | --- |
| M06/M07 | Data tujuh TF, cache, history readiness dan indicator snapshots. |
| M08/M09/M10/M12 | Peluasan TF pada detector/lifecycle canonical yang sama, tanpa detector slot baharu. |
| M11 | Strategic owner tidak dikira semula oleh parser. |
| M12N | Kekal read-only lineage/context; tiada rank/create/reject/execute authority baharu. |
| M13/M14 | Custom collector/formula validation berasingan label daripada canonical signatures; immutable owner outputs. |
| M15/M16 | Single authority, event batching, exact snapshot/freshness revalidation. |
| M17 | Tiga resolver exit, exact structural provenance, geometry dan normalized levels. |
| M19/M20/M21 | Gross risk, limits/reservations, protection dan frozen sizing. |
| M22 | Execution, retry dan ambiguity reconciliation; tidak mentafsir formula. |
| M23/M24 | Lifecycle dan recovery posisi/decision/consumed trigger. |
| M25/M26/M27 | Paparan/init validation dan orchestration; tiada signal authority daripada UI. |

Naming/helper sedia ada dikekalkan jika sepadan. Tiada renumber M01–M27 atau slot numeric baharu bagi M12N. Parser/config ialah engineering facility di bawah owner semasa, bukan strategi baharu yang memintas graph.

## 14. Persistence dan perubahan konfigurasi

Simpan configuration hash, formula revision, source/witness IDs, selected decision, frozen risk snapshot, reservations, consumed trigger, order reconciliation state dan TradePlan bersama schema/build version. Penulisan atomic/generation integrity guna mekanisme canonical yang telah ada.

Recovery reconcile ticket/ownership sebelum entry baharu. Pending ambiguous send tidak dihantar semula secara buta. Configuration mismatch tidak membolehkan trigger lama digunakan semula. Owner state boleh dibina semula daripada closed history jika kontrak membenarkan; trade lama masih guna frozen plan. Corrupt/missing identity menyebabkan HOLD new entries dan diagnostics; protective management diteruskan setakat ownership yang dapat dibuktikan.

## 15. Ujian penerimaan dan batas bukti

| Kumpulan | Bukti wajib |
| --- | --- |
| Formula | AND/OR, grouping, tujuh atom, alias unresolved, OFF dependency, malformed input dan winning witness. |
| Signal | Setiap supported signal × TF mempunyai accepted mapping dan targeted positive/negative/state tests; unsupported tidak executable. |
| Timing | M1/M5/M15/M30/H1/H4/D1 close events; simultaneous high/low TF batch; tiada live candle/look-ahead; quote absent/reconnect. |
| Lifecycle | Context valid/void/superseded; entry window tamat; RE structural lifecycle tidak diberi generic TTL. |
| Dedup | OR dua TF serentak, slot overlap, BOTH engine, restart, repeated ticks/timer dan send ambiguity. |
| Exit/sizing | BUY/SELL geometry, witness-bound source, unsupported structural exit, RR, POINTS/PRICE, frozen risk, below-min/invalid fixed lot. |
| Portfolio | Limits per slot/symbol/global; reserved exposure; hedging ON/OFF; unknown risk; multi-instance ownership. |
| Multi-symbol | Suffix/ambiguity, independent state dan different digits/tick size/session availability. |
| Paparan | Label toggle tidak mengubah trade trace; confirmation time tepat; tiada object luar dihapus. |
| Regression | Canonical konfigurasi lama mengekalkan accepted decisions/order/lifecycle trace pada dataset/build yang sama, kecuali delta yang approved. |

Urutan verification: static → cross-module → native MQL4 strict compile → targeted regression → Strategy Tester → log/state/order validation → demo acceptance. Source/build/EX4/config/data identity direkod; identifier build baharu jika source berubah. PASS hanya dengan output sebenar.

Single-symbol tester dan deterministic multi-symbol harness boleh memberi bukti separa. Full multi-symbol acceptance memerlukan native tester capability yang benar-benar disahkan atau demo runtime dengan history/quote semua simbol. Jangan dakwa harness membuktikan broker execution penuh. P&L memerlukan metadata spread, commission, swap dan slippage serta data coverage yang dilabel dengan jujur; engineering history bukan tick-accurate canonical secara automatik.

Backtest tidak memilih kombinasi terbaik dan mengujinya pada sampel sama sahaja: asingkan development dan OOS sebelum membuat tuntutan prestasi. Tiada target profit/winrate minimum telah dipersetujui dalam draf ini.

## 16. Pelaksanaan berperingkat dan kelulusan

1. Pulihkan exact live baseline/PR/checkpoint; item verified tidak diulang. Buka scoped architecture Issue/branch; simpan design/decision tanpa overwrite canonical contracts.
2. Reconcile registry signal/TF serta schema/input/parser; peluasan detector dan event scheduler dalam mode monitor. Tutup uncertainty mapping sebelum execution.
3. Custom formula/witness/lifecycle, labels, persistence dan dedup; shadow traces dahulu.
4. Tiga exit resolver, sizing, caps, hedging dan auto-entry melalui owners sedia ada.
5. Compile/regression/tester dan isolated demo acceptance, kemudian review release. Tiada real-money activation daripada permintaan draf ini.

Ini ialah susunan kerja cadangan, bukan implementation plan terperinci atau authorization untuk merge/deploy. Selepas design diluluskan, barulah implementation plan dengan atomic exit criteria disediakan. Dokumen repo yang dicadangkan: `docs/superpowers/specs/2026-11-07-custom-mtf-autoentry-design.md`; belum committed kerana baseline implementasi perlu dipulihkan dan pengguna meminta draf sahaja.

### Perkara yang perlu diperhatikan semasa menyemak draf

Keputusan pengguna tentang lima slot, tujuh komponen, syntax/context-trigger, exits/sizing, simbol dan hedging sudah direkod; tidak perlu dipilih semula.

Cadangan teknikal yang diminta kelulusan bersama draf: peluasan cadence CUSTOM melalui satu M15 authority; D1 strategic gate kekal; Context+Trigger tidak kosong; satu order per simbol/event batch; priority engineering bagi slot overlap; fixed-distance POINTS/PRICE; MARKET_WATCH universe frozen; invalid enabled slot menolak init; posisi lama guna frozen TradePlan. Nilai cap portfolio dan BE/trailing boleh dikonfigurasi kemudian dan tidak perlu menghalang perancangan, tetapi execution mesti menolak nilai invalid.

**Kesimpulan status:** spesifikasi produk untuk semakan. EA belum diubah. Pindaan authority/clock dan exit custom memerlukan keputusan serta kontrak baharu yang traceable sebelum executable logic. Semua dakwaan compile/runtime/profit kekal NOT VERIFIED untuk cadangan ini.
