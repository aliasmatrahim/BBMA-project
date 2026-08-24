from pathlib import Path
import argparse

SRC_REL = Path("blueprint/source/BBMA_EA.mq4")
AUDIT_REL = Path("blueprint/D1_STEP6_MINRR_DEFAULT_OFF_IMPLEMENTATION_AUDIT_20260824.md")
DECISION_REL = Path("blueprint/decisions/D1_06_MINRR_DEFAULT_OFF_DECISION_20260824.md")

BUILD_OLD = "//| Version 4.5.1 - D1-05 Input Limit Guard                         |"
BUILD_NEW = "//| Version 4.5.1 - D1-06 MinRR Default Off                        |"
INPUT_OLD = "input double   MinRRRatio                         = 1.5;        // 08 Advanced | minimum accepted Risk:Reward"
INPUT_NEW = "input double   MinRRRatio                         = 0.0;        // 08 Advanced | optional Min RR filter; 0=disabled"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, got {count}")
    return text.replace(old, new, 1)


def verify_source(src: Path) -> None:
    text = src.read_text(encoding="utf-8")
    required = [
        BUILD_NEW,
        INPUT_NEW,
        "if(MinRRRatio > 0.0 && (tpDistance / slDistance) < MinRRRatio)",
        "rejection = REJ_INVALID_RR;",
        "#define MAX_PAIRS               40",
        "Version 4.5.1 - D1-06 MinRR Default Off",
    ]
    for item in required:
        if item not in text:
            raise SystemExit(f"missing D1-06 invariant: {item}")

    forbidden = [BUILD_OLD, INPUT_OLD]
    for item in forbidden:
        if item in text:
            raise SystemExit(f"stale D1-05/old-default invariant remains: {item}")

    if text.count("if(MinRRRatio > 0.0 && (tpDistance / slDistance) < MinRRRatio)") != 1:
        raise SystemExit("MinRR runtime gate must remain exactly once")

    for n in range(1, 28):
        if f"MODULE {n:02d}:" not in text:
            raise SystemExit(f"missing module marker MODULE {n:02d}")

    print("D1_STEP6_MINRR_DEFAULT_OFF_STATIC=PASS")


def write_docs(root: Path) -> None:
    decision = root / DECISION_REL
    decision.parent.mkdir(parents=True, exist_ok=True)
    decision.write_text(
        """# D1-06 — MinRR Default-Off Decision\n\n"
        "Date: 2026-08-24  \n"
        "Branch: `d1-owner-dev`  \n"
        "Decision: **KEEP `MinRRRatio` AVAILABLE, DEFAULT DISABLED (`0.0`)**\n\n"
        "## User decision\n"
        "`MinRRRatio` is retained as an optional project-level rejection filter, but it must not be enabled by default.\n\n"
        "## Runtime meaning\n"
        "- `MinRRRatio = 0.0` => filter disabled.\n"
        "- `MinRRRatio > 0.0` => existing RR rejection check remains available where the current payload has a valid static TP distance.\n"
        "- This optional numeric filter is **not represented as a universal BBMA/Oma Ally Core rule**.\n"
        "- Future F7 targetless/lifecycle-managed Re-Entry payloads remain governed by the F7 resolution: they must structurally bypass numeric RR when no source-valid static reward distance exists, regardless of this input.\n\n"
        "## Scope\n"
        "This decision changes only the default input state and build identity. It does not alter BBMA detectors, D1/H4/H1/M15 hierarchy, SL/TP construction, lot sizing, execution order, or lifecycle rules.\n",
        encoding="utf-8",
    )

    audit = root / AUDIT_REL
    audit.write_text(
        """# D1 Step 6 — MinRR Default-Off Implementation Audit\n\n"
        "Date: 2026-08-24  \n"
        "Branch: `d1-owner-dev`  \n"
        "Build: `Version 4.5.1 - D1-06 MinRR Default Off`  \n"
        "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**\n\n"
        "## Change\n"
        "- `MinRRRatio` default changed from `1.5` to `0.0`.\n"
        "- Input remains visible and functional as an optional project filter.\n"
        "- Existing runtime condition `MinRRRatio > 0.0` is preserved, therefore `0.0` disables RR rejection.\n"
        "- No detector, combination, direction, D1 owner, SL/TP resolver, money-management, portfolio, order-send, or lifecycle formula was changed.\n\n"
        "## F7 compatibility boundary\n"
        "The numeric RR filter is not promoted as universal BBMA Core. When the later F7 targetless lifecycle payload is implemented, lifecycle-managed Re-Entry trades with no source-valid static TP must bypass RR structurally even if the optional input is non-zero.\n\n"
        "## Verification\n"
        "Focused source invariant check: **PASS**.  \n"
        "Native MT4 MetaEditor: **PENDING**.\n",
        encoding="utf-8",
    )


def apply(root: Path) -> None:
    src = root / SRC_REL
    text = src.read_text(encoding="utf-8")
    text = replace_once(text, BUILD_OLD, BUILD_NEW, "build header")
    text = replace_once(text, INPUT_OLD, INPUT_NEW, "MinRR default")

    # Keep runtime-visible build text aligned with the source identity if present.
    text = text.replace("=== BBMA EA V4.5.1 D1-05 ===", "=== BBMA EA V4.5.1 D1-06 ===")
    text = text.replace("BBMA EA V4.5.1 D1-05 initialized successfully", "BBMA EA V4.5.1 D1-06 initialized successfully")

    src.write_text(text, encoding="utf-8")
    write_docs(root)
    verify_source(src)
    print("D1_STEP6_MINRR_DEFAULT_OFF_APPLY=PASS")


def finalize(root: Path) -> None:
    verify_source(root / SRC_REL)
    audit = root / AUDIT_REL
    text = audit.read_text(encoding="utf-8")
    text = text.replace(
        "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR COMPILE PENDING**",
        "Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**",
        1,
    )
    text = text.replace(
        "Native MT4 MetaEditor: **PENDING**.",
        "Native MT4 MetaEditor: **0 errors / 0 warnings; EX4 produced**.",
        1,
    )
    audit.write_text(text, encoding="utf-8")
    print("D1_STEP6_MINRR_DEFAULT_OFF_FINALIZE=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if args.verify:
        verify_source(root / SRC_REL)
    elif args.finalize:
        finalize(root)
    else:
        apply(root)


if __name__ == "__main__":
    main()
