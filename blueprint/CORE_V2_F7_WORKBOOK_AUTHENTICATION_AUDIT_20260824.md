# CORE-V2-F7 — BBMA Home Course Workbook Authentication Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Artifact reviewed: `333531988-BBMA-Home-Course.pdf`  
Scope: source authentication / F7 SL-TP provenance  
Status: **STRONG-PROVENANCE COPY / TIER B — NOT YET TIER A AUTHENTICATED ORIGINAL**

## 1. Purpose

Authenticate the newly supplied 19-page `BBMA Home Course Workbook` PDF and determine how much evidentiary authority it may carry under CORE-V2-F7 Path A strict provenance governance.

This audit does **not** change `blueprint/source/BBMA_EA.mq4` and does not promote any workbook-only trading rule directly into authoritative Strategy Core.

## 2. Binary / structural inspection

Local artifact name:
`333531988-BBMA-Home-Course.pdf`

Observed file properties:

- pages: 19;
- page size: A4, approximately 595 x 842 pt on all pages;
- encrypted: no;
- PDF version: 1.3;
- file size: 102,131 bytes;
- SHA-256: `b20b8de38d878fa192d0a2fb9d70aba15b59208b477a3cefe73936974a5c2ee7`;
- Title metadata: `Microsoft Word - Workbook part 1`;
- Author metadata: `user`;
- Creator: `PrimoPDF http://www.primopdf.com`;
- Producer: `Nitro PDF PrimoPDF`;
- CreationDate: `2015-08-21 11:45:18 -08:00`;
- ModDate: same as CreationDate;
- embedded fonts include Calibri / Calibri Bold / Arial;
- no forms, annotations, attachments or JavaScript.

The same creation and modification timestamps are consistent with a one-time Word-to-PDF export. There is no metadata evidence of a later PDF edit, although metadata alone cannot prove that the underlying Word source was authentic.

## 3. Visual / internal consistency inspection

All 19 pages render cleanly with a uniform document template.

Consistent internal markers include:

- page header: `BBMA Home Course Workbook | <page>`;
- footer/domain: `www.bbmahomecourse.com`;
- sequential Lesson structure from Bollinger Band settings through MA5/MA10/MA50, Extreme, MHV, CS Arah, Re-Entry, Momentum and Rumusan;
- consistent typography, margins and numbering;
- no obvious inserted pages, style breaks, rescan pages or later foreign sections.

The PDF is text-native rather than a scan, which is consistent with the `Microsoft Word -> PrimoPDF` metadata.

## 4. Historical product provenance reconciliation

Independent historical 2015 web records pre-date the PDF metadata and establish that a product named `BBMA Home Course Study` was sold as a BBMA/Oma Ally training package.

Contemporaneous records describe the package as including:

1. `DVD BBMA Basic-The Missing Chapter Finale`;
2. `DVD Tutorial BBMA`;
3. `Workbook BBMA`.

A dated CariGold post on 2015-08-08 describes the `Workbook BBMA` as breaking down the DVD explanations one-by-one, providing transcription material and additional checklist content.

The reviewed PDF's lesson-by-lesson, transcription/checklist-like structure is strongly consistent with that historical description. Its PDF CreationDate of 2015-08-21 is also temporally plausible relative to the official July/August 2015 Home Course sales period.

This materially strengthens provenance beyond an unattributed modern derivative PDF.

## 5. Consistency against archived BBMA Finale evidence

The workbook materially overlaps the archived original Finale V05/V06 teaching structure:

- Extreme -> TP Wajib -> MHV -> direction -> Re-Entry -> Momentum -> further Re-Entry;
- Re-Entry is the actual setup/entry after direction;
- Momentum is a close outside the relevant outer BB and proves continuation;
- Momentum creates later Re-Entry opportunities;
- higher/lower timeframe relationships are repeatedly emphasized.

This is not merely a vocabulary overlap; the sequencing and teaching role of the stages agree at a detailed structural level with the archived 2015-era Finale transcript evidence.

## 6. Material F7 exit / TP evidence in the workbook

The workbook contains materially stronger exit evidence than the two existing summary PDFs alone.

### 6.1 MHV / Re-Entry lifecycle

Page 10 states in substance:

- MHV TP is negotiable rather than universally fixed at MA5/10 or Low BB;
- inspect the next candle's close relative to BB;
- if it closes outside BB, allow the position because Momentum exists;
- if it closes inside BB, close because the market is expected to reverse;
- after MHV -> direction -> Re-Entry, if there is no Momentum, TP is mandatory.

### 6.2 Direction / destination context

Pages 13–14 state that a strong direction/retracement has a BB outer-band destination in the shown context, and that if no Momentum develops after reaching the area, the trader waits for reverse confirmation/retest rather than assuming indefinite continuation.

The same section also warns that timeframe ownership matters and uses major-trend / higher-timeframe context.

### 6.3 Explicit Momentum decision rule

Page 16 gives the clearest lifecycle rule:

`Arah -> Reentry -> Tiada Momentum -> Close post, market akan reverse.`

It separately states:

`Bila ada Momentum akan ada reentry.`

Pages 17–18 repeat the cycle and state that if Re-Entry is followed by no Momentum, the market makes a rotation / position should be TP; if Momentum occurs, wait for another Re-Entry.

## 7. What the workbook does NOT yet prove

Even with this stronger source, the workbook does **not** cleanly establish the exact current M17 static resolver as written:

- H1 Re-Entry -> H1 Top/Low BB TP;
- REM -> H4 Top/Low BB TP;
- RRE -> D1 Top/Low BB TP;
- REE -> D1 Top/Low BB TP;
- exact mapped Re-Entry source-candle wick +/- one broker point as a universal hard SL.

The workbook instead gives strong lifecycle-oriented TP logic:

`Re-Entry -> Momentum = continuation / later Re-Entry`

and

`Re-Entry -> no Momentum = TP / close / rotation expected`.

It also contains direction-to-BB-destination teaching, but not enough text-only specificity to prove the current one-to-one M17 H1/H4/D1 destination-owner mapping for REM/RRE/REE.

No workbook passage found establishes the exact one-broker-point hard-SL buffer.

## 8. Authentication classification

### Tier A — Authenticated original

Not reached yet.

Missing Tier-A evidence includes one of:

- original purchaser copy directly traceable to the 2015 package;
- original physical workbook scan with purchase provenance;
- official publisher/Oma Ally distribution copy;
- independent authenticated binary/hash match to a known original Home Course package copy.

### Tier B — Strong-provenance copy

**Reached.**

Reasons:

- 19-page internal workbook identity is coherent;
- `www.bbmahomecourse.com` is printed consistently throughout;
- PDF metadata date is contemporaneous with the 2015 product sales period;
- historical 2015 posts independently confirm a `Workbook BBMA` as part of the Home Course package;
- historical description of the workbook matches this file's lesson/transcription/checklist structure;
- detailed content is strongly consistent with archived Finale teaching sequence;
- no obvious later insertion/re-edit artifact was detected in the PDF container/layout.

### Tier C — Derivative/community copy

The artifact is stronger than Tier C due to the evidence above, although its immediate acquisition path is still a third-party Scribd copy rather than a verified original distribution channel.

## 9. F7 governance impact

This workbook materially upgrades F7 evidence, but Path A remains strict.

Current resolution:

- `Re-Entry -> Momentum -> continuation / another Re-Entry`: **STRONGLY CORROBORATED**;
- `Re-Entry -> no Momentum -> TP/close`: **STRONG SOURCE EVIDENCE, Tier-B provenance**;
- normal Extreme TP Wajib: **STRONGLY CORROBORATED**;
- current M17 H1/H4/D1 static outer-BB mapping: **NOT YET FULLY PROVEN**;
- current wick +/- one broker-point hard SL: **EA_SAFETY / NOT PROVEN UNIVERSAL CORE**.

Therefore the workbook should not yet be inserted into `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` as unquestioned Tier-A evidence. It should be retained as a high-value research/evidence source and reconciled rule-by-rule before any Core promotion.

## 10. Recommended next step

The best next source task is a **Workbook Rule Reconciliation Audit** focused only on executable exit semantics:

1. map pages 10, 13–16, 17–18 against Finale V05/V06 and the primary/secondary PDFs;
2. classify each exit statement as `DIRECT`, `CORROBORATED`, `CONTEXTUAL`, `PERSONAL`, or `UNRESOLVED`;
3. determine whether `NO MOMENTUM -> TP` can be promoted into accepted Strategy Core lifecycle semantics;
4. keep static BB destination ownership and hard-SL formula separate unless specifically proven;
5. do not change the frozen P3 EA candidate until runtime evidence B–D is complete.

## Final verdict

**Authentication verdict: TIER B / STRONG-PROVENANCE COPY.**

The supplied PDF is highly likely to be a genuine 2015-era `BBMA Home Course Workbook` copy or a faithful direct export/copy of that workbook, but the available chain of custody is not sufficient to certify it as a Tier-A authenticated original binary.

Its Re-Entry/Momentum/TP lifecycle material is strong enough to justify a dedicated reconciliation audit, but not by itself to silently redefine M17 or the canonical Strategy Core.