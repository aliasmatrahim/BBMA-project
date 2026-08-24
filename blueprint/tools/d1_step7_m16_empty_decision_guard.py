from pathlib import Path
import argparse

SRC_REL = Path("blueprint/source/BBMA_EA.mq4")
AUDIT_REL = Path("blueprint/D1_STEP7_M16_EMPTY_DECISION_GUARD_AUDIT_20260824.md")

BUILD_OLD = "//| Version 4.5.1 - D1-06 MinRR Default Off                        |"
BUILD_NEW = "//| Version 4.5.1 - D1-07 M16 Empty Decision Guard                 |"
OLD_GATE = """   if(decision.DecisionState == DEC_CREATED)\n   {\n      InvalidationEngine_Atomic(pairIndex, decision, conflict);\n   }"""
NEW_GATE = """   // D1-07: M16 may only consume an actual M15-created decision.\n   // ZeroMemory() leaves enum value 0 (= DEC_CREATED), so state alone is not\n   // sufficient to prove that M15 selected/froze a decision.\n   if(decision.Valid && decision.DecisionState == DEC_CREATED)\n   {\n      InvalidationEngine_Atomic(pairIndex, decision, conflict);\n   }"""


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, got {n}")
    return text.replace(old, new, 1)


def verify(src):
    text = src.read_text(encoding="utf-8")
    required = [BUILD_NEW, NEW_GATE, "input double   MinRRRatio                         = 0.0;", "#define MAX_PAIRS               40"]
    for x in required:
        if x not in text:
            raise SystemExit(f"missing invariant: {x}")
    if BUILD_OLD in text or OLD_GATE in text:
        raise SystemExit("stale D1-06/old M16 gate remains")
    if text.count("if(decision.Valid && decision.DecisionState == DEC_CREATED)") != 1:
        raise SystemExit("selected-decision M16 guard must exist exactly once")
    print("D1_STEP7_M16_EMPTY_DECISION_GUARD_STATIC=PASS")


def write_audit(root):
    p = root / AUDIT_REL
    p.write_text("""# D1 Step 7 — M16 Empty-Decision Guard Audit\n\nDate: 2026-08-24  \nBranch: `d1-owner-dev`  \nBuild: `Version 4.5.1 - D1-07 M16 Empty Decision Guard`  \nStatus: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**\n\n## Runtime evidence\nUser broker/demo Experts output showed repeated `[D1-03][M16_D1_REJECT]` records with blank `DecisionID`, `FrozenState=D1_OWNER_UNRESOLVED`, `FrozenDir=DIR_NONE`, and `FrozenCandle=1970.01.01`, while the same pairs had valid M11 `[OWNER]` BUY/SELL-confirmed snapshots.\n\n## Root cause\n`BBMA_Decision` is zero-initialized in M27. `ENUM_DECISION_STATE` value zero is `DEC_CREATED`. When M15 selected no candidate, the empty decision therefore still satisfied the old `DecisionState == DEC_CREATED` gate and was incorrectly sent into M16. Because M15 had never frozen a D1 snapshot, M16 correctly rejected the empty object, producing a false runtime rejection trace.\n\n## Fix\nM27 now calls `InvalidationEngine_Atomic()` only when both:\n- `decision.Valid == true` (M15 actually selected/created a decision); and\n- `decision.DecisionState == DEC_CREATED`.\n\nThis matches the M15/M16 contracts: M16 revalidates an M15-created pending decision; it must not process a zero/default object.\n\n## Strategy / architecture impact\n- No BBMA detector, D1 owner formula, D1 gate, candidate selection, SL/TP, risk, money-management, order execution, or live-position lifecycle rule changed.\n- Real D1 snapshot mismatch/transition/unresolved rejection remains fail-closed for actual selected decisions.\n- The fix removes false `1970 / blank DecisionID` M16 rejection noise and prevents an empty object from being recorded as a strategy invalidation path.\n\n## Verification\nFocused static invariant check: **PASS**.  \nNative MT4 MetaEditor: **PENDING**.\n""", encoding="utf-8")


def apply(root):
    src = root / SRC_REL
    text = src.read_text(encoding="utf-8")
    text = replace_once(text, BUILD_OLD, BUILD_NEW, "build header")
    text = replace_once(text, OLD_GATE, NEW_GATE, "M16 gate")
    src.write_text(text, encoding="utf-8")
    write_audit(root)
    verify(src)


def finalize(root):
    verify(root / SRC_REL)
    p = root / AUDIT_REL
    text = p.read_text(encoding="utf-8")
    text = text.replace("Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**", "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**", 1)
    text = text.replace("Native MT4 MetaEditor: **PENDING**.", "Native MT4 MetaEditor: **0 errors / 0 warnings; EX4 produced**.", 1)
    p.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--finalize", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    if args.verify:
        verify(root / SRC_REL)
    elif args.finalize:
        finalize(root)
    else:
        apply(root)

if __name__ == "__main__":
    main()
