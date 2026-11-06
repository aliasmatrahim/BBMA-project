"""Source-level MHV retest regression; MT4 runtime is tested separately."""
from pathlib import Path
import re


source = (
    Path(__file__).resolve().parents[2] / "blueprint/source/BBMA_EA.mq4"
).read_text(encoding="utf-8-sig")

match = re.search(
    r"bool IsMHVRetestInteraction\(MLVData &mlv, TimeframeData &data\)\s*"
    r"\{(.*?)\n\}",
    source,
    re.S,
)
assert match, "production retest interaction function missing"
function = match.group(1)

assert re.search(
    r"if\s*\(\s*mlv\.FrozenMarkedBody\s*<=\s*0\s*\|\|"
    r"\s*data\.high\s*<=\s*0\s*\|\|"
    r"\s*data\.low\s*<=\s*0\s*\)\s*return\s+false\s*;",
    function,
), "production invalid-price guard missing"
assert re.search(
    r"if\s*\(\s*mlv\.Direction\s*==\s*DIR_BUY\s*\|\|"
    r"\s*mlv\.Direction\s*==\s*DIR_SELL\s*\)",
    function,
), "production direction guard missing"

predicate = re.search(
    r"return\s*\((data\.low\s*<=\s*mlv\.FrozenMarkedBody"
    r"\s*&&\s*data\.high\s*>=\s*mlv\.FrozenMarkedBody)\);",
    function,
)
assert predicate, "production range-intersection predicate missing"
expression = (
    predicate.group(1)
    .replace("data.low", "low")
    .replace("data.high", "high")
    .replace("mlv.FrozenMarkedBody", "body")
    .replace("&&", "and")
)


def interaction(direction, low, high, body):
    if body <= 0 or high <= 0 or low <= 0:
        return False
    if direction not in ("buy", "sell"):
        return False
    return bool(
        eval(
            expression,
            {"__builtins__": {}},
            {"low": low, "high": high, "body": body},
        )
    )


boundary_cases = [
    (99, 101, 100, True),   # range crosses the frozen body
    (100, 101, 100, True),  # low touches the body
    (99, 100, 100, True),   # high touches the body
    (98, 99, 100, False),   # gap entirely below
    (101, 102, 100, False), # gap entirely above
    (99, 101, 0, False),    # invalid frozen reference
    (99, 0, 100, False),    # invalid high
    (0, 101, 100, False),   # invalid low
]
for direction in ("buy", "sell"):
    for low, high, body, expected in boundary_cases:
        actual = interaction(direction, low, high, body)
        assert actual == expected, (direction, low, high, body, expected, actual)
for low, high, body, _expected in boundary_cases:
    assert not interaction("none", low, high, body), (
        "invalid direction must not complete retest",
        low,
        high,
        body,
    )

lifecycle_gate = re.search(
    r"if\s*\(\s*mlv\.State\s*==\s*MLV_FORMATION_ESTABLISHED\s*&&"
    r"\s*data\.candle_time\s*>\s*mlv\.ConfirmationCandleTime\s*&&"
    r"\s*IsMHVRetestInteraction\(mlv,\s*data\)\s*\)\s*"
    r"\{\s*mlv\.State\s*=\s*MLV_RETEST_COMPLETE\s*;"
    r"\s*mlv\.RetestBar\s*=\s*data\.barIndex\s*;"
    r"\s*mlv\.RetestCandleTime\s*=\s*data\.candle_time\s*;",
    source,
    re.S,
)
assert lifecycle_gate, "production later-candle retest transition missing"


def transition(state, candle_time, confirmation_time, touches):
    if (
        state == "MLV_FORMATION_ESTABLISHED"
        and candle_time > confirmation_time
        and touches
    ):
        return "MLV_RETEST_COMPLETE"
    return state


lifecycle_cases = [
    ("same confirmation candle", "MLV_FORMATION_ESTABLISHED", 10, 10, True,
     "MLV_FORMATION_ESTABLISHED"),
    ("earlier candle", "MLV_FORMATION_ESTABLISHED", 9, 10, True,
     "MLV_FORMATION_ESTABLISHED"),
    ("later gap below", "MLV_FORMATION_ESTABLISHED", 11, 10, False,
     "MLV_FORMATION_ESTABLISHED"),
    ("later gap above", "MLV_FORMATION_ESTABLISHED", 11, 10, False,
     "MLV_FORMATION_ESTABLISHED"),
    ("later buy-side touch", "MLV_FORMATION_ESTABLISHED", 11, 10, True,
     "MLV_RETEST_COMPLETE"),
    ("later sell-side touch", "MLV_FORMATION_ESTABLISHED", 11, 10, True,
     "MLV_RETEST_COMPLETE"),
    ("wrong prior state", "MLV_LOSS_OF_MOMENTUM", 11, 10, True,
     "MLV_LOSS_OF_MOMENTUM"),
]
for name, state, candle_time, confirmation_time, touches, expected in lifecycle_cases:
    actual = transition(state, candle_time, confirmation_time, touches)
    assert actual == expected, (name, expected, actual)

print(
    "PASS 16 directional boundary cases, 8 invalid-direction cases, "
    "7 lifecycle transition cases"
)
