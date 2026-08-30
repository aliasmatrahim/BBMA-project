#!/usr/bin/env python3
"""Model the C3 exact-chart tester shortcut and unchanged live resolver."""


def remove_suffix(symbol: str) -> str:
    pos = symbol.find(".")
    return symbol[:pos] if pos > 0 else symbol


def baseline_resolve(requested: str, catalog: list[str], selectable: set[str]) -> str:
    requested = requested.strip()
    if not requested:
        return ""

    for name in catalog:
        if name != requested:
            continue
        return name if name in selectable else ""

    base = remove_suffix(requested)
    matches = [
        name for name in catalog
        if remove_suffix(name) == base or name.startswith(base)
    ]
    if len(matches) != 1:
        return ""
    return matches[0] if matches[0] in selectable else ""


def current_resolve(
    requested: str,
    is_testing: bool,
    chart_symbol: str,
    catalog: list[str],
    selectable: set[str],
) -> str:
    requested = requested.strip()
    if not requested:
        return ""
    if is_testing and requested == chart_symbol:
        return requested
    return baseline_resolve(requested, catalog, selectable)


def pair_enabled(resolved: str, broker_spec_valid: bool) -> bool:
    return bool(resolved) and broker_spec_valid


def main() -> None:
    cases = 0

    live_matrix = (
        ("GBPUSD", ["GBPUSD"], {"GBPUSD"}),
        ("GBPUSD", ["GBPUSD"], set()),
        ("GBPUSD", ["GBPUSD.a"], {"GBPUSD.a"}),
        ("GBPUSD", ["GBPUSD.a", "GBPUSD.b"], {"GBPUSD.a", "GBPUSD.b"}),
        (" GBPUSD ", ["GBPUSD"], {"GBPUSD"}),
        ("EURUSD", [], set()),
        ("", ["GBPUSD"], {"GBPUSD"}),
    )
    for requested, catalog, selectable in live_matrix:
        assert current_resolve(
            requested, False, "GBPUSD", catalog, selectable
        ) == baseline_resolve(requested, catalog, selectable)
        cases += 1

    assert current_resolve("GBPUSD", True, "GBPUSD", [], set()) == "GBPUSD"
    cases += 1
    assert current_resolve(" GBPUSD ", True, "GBPUSD", [], set()) == "GBPUSD"
    cases += 1
    assert current_resolve("EURUSD", True, "GBPUSD", [], set()) == ""
    cases += 1
    assert current_resolve("GBPUSD.a", True, "GBPUSD", [], set()) == ""
    cases += 1
    assert current_resolve(
        "EURUSD", True, "GBPUSD", ["EURUSD"], {"EURUSD"}
    ) == "EURUSD"
    cases += 1

    tester_symbol = current_resolve("GBPUSD", True, "GBPUSD", [], set())
    assert pair_enabled(tester_symbol, True)
    cases += 1
    assert not pair_enabled(tester_symbol, False)
    cases += 1

    print(f"C3_OFFLINE_TESTER_SYMBOL_RESOLUTION_MODEL=PASS cases={cases}")


if __name__ == "__main__":
    main()
