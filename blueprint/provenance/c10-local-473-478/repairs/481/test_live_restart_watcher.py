from pathlib import Path
import re

WATCHER = Path(__file__).with_name("live_physical_restart_automation_20260908.ps1")


def test_post_restart_waits_for_runtime_recovery_markers():
    text = WATCHER.read_text(encoding="utf-8-sig")
    post_loop = text.split("$postDeadline=", 1)[1].split("if(!$postMatch)", 1)[0]

    stale_break = re.search(
        r"if\s*\(\$postMatch\s*\)\s*\{\s*break\s*\}",
        post_loop,
        re.IGNORECASE | re.DOTALL,
    )
    assert stale_break is None, "stale checkpoint row must not end post-restart wait"

    combined_gate = re.search(
        r"if\s*\(\$postMatch\s*-and\s*\$recoverySeen\s*-and\s*\$readySeen\s*\)\s*\{\s*break\s*\}",
        post_loop,
        re.IGNORECASE | re.DOTALL,
    )
    assert combined_gate is not None, "restart gate must require checkpoint + recovery + ready markers"


def test_post_restart_timeout_rejects_partial_proof():
    text = WATCHER.read_text(encoding="utf-8-sig")
    timeout_gate = re.search(
        r"if\s*\(!\$postMatch\s*-or\s*!\$recoverySeen\s*-or\s*!\$readySeen\s*\)",
        text,
        re.IGNORECASE,
    )
    assert timeout_gate is not None, (
        "timeout must fail when checkpoint, recovery, or ready proof is missing"
    )
