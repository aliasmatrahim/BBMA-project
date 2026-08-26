#!/usr/bin/env python3
from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import v458_runtime_variant_builder as b


def sample() -> str:
    return "\n".join([
        b.BUILD_MARKER,
        b.VERSION_MARKER,
        b.D1_GATE_OFF,
        b.C044_GATE_OFF,
        "void OnTick(){}",
        "",
    ])


def main() -> int:
    src = sample()
    baseline, ch = b.build_variant_from_text(src, "baseline")
    assert baseline == src and ch == []
    r1, ch = b.build_variant_from_text(src, "r1-d1tpw")
    assert r1.count(b.D1_GATE_ON) == 1 and r1.count(b.C044_GATE_OFF) == 1 and len(ch) == 1
    r2, ch = b.build_variant_from_text(src, "r2-c044")
    assert r2.count(b.C044_GATE_ON) == 1 and r2.count(b.D1_GATE_OFF) == 1 and len(ch) == 1
    try:
        b.build_variant_from_text(src.replace(b.D1_GATE_OFF, b.D1_GATE_ON), "r1-d1tpw")
    except ValueError:
        pass
    else:
        raise AssertionError("builder must fail closed when source gate baseline is not exact")
    print("V458_RUNTIME_VARIANT_BUILDER_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
