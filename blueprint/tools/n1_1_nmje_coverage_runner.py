from pathlib import Path

patcher = Path("blueprint/tools/n1_1_nmje_coverage_patch.py")
code = patcher.read_text(encoding="utf-8")

start = code.find("def patch_update_journey(block: str) -> str:\n")
end = code.find("\ntext = replace_block(\n    text,\n    r\"(?m)^void\\s+UpdateNestedJourneyObservation", start)
if start < 0 or end < 0:
    raise SystemExit("Unable to isolate patch_update_journey in N1.1 patcher")

fixed = '''def patch_update_journey(block: str) -> str:\n    lines = block.splitlines(keepends=True)\n    out = []\n    count = 0\n    for line in lines:\n        out.append(line)\n        if line.strip() == "g_nested_journeys[pairIndex] = journey;":\n            indent = line[:len(line) - len(line.lstrip())]\n            out.append(indent + "NMJE_PrintCoverageOverlay(journey);\\n")\n            count += 1\n    if count < 2:\n        die(f"Expected multiple journey assignments, got {count}")\n    return "".join(out)\n'''

patched_code = code[:start] + fixed + code[end:]
compile(patched_code, str(patcher), "exec")
exec(patched_code, {"__name__": "__main__", "__file__": str(patcher)})
