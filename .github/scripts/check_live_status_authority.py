#!/usr/bin/env python3
from pathlib import Path


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing governance marker: {marker}")


def main() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    protocol = Path("docs/LIVE_STATUS_AUTHORITY_PROTOCOL.md").read_text(encoding="utf-8")

    require(
        readme,
        "## Mandatory live-status resolution",
        "docs/LIVE_STATUS_AUTHORITY_PROTOCOL.md",
        "latest project/test-plan update",
        "latest actual test attempt",
        "latest valid PASS evidence",
        "next required test",
        "STATUS CONFLICT / VERIFICATION REQUIRED",
        "Chat memory is never status authority",
    )

    require(
        protocol,
        "Status: **MANDATORY GOVERNANCE FOR STATUS/SEQUENCING QUERIES**",
        "### Gate 1 — Repository governance / branch ownership",
        "### Gate 2 — Canonical current-state records",
        "### Gate 3 — Repository delta / freshness sweep",
        "### Gate 4 — Supersession scan",
        "### Gate 5 — Separate the four clocks",
        "open PRs relevant to the project/workstream",
        "recent repository commits",
        "issue/PR comments",
        "head SHA/build identity",
        "explicit newer owner sequencing/authorization decision",
        "STATUS CONFLICT / VERIFICATION REQUIRED",
        "Chat memory and prior assistant answers are navigation aids only",
        "Regression example — R1 vs C3",
    )

    print("LIVE_STATUS_AUTHORITY_GOVERNANCE=PASS")


if __name__ == "__main__":
    main()
