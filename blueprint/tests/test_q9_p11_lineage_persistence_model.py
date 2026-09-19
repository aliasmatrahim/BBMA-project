#!/usr/bin/env python3

NONE = 0
FIRST = 1
CONTINUATION = 2
NEW_JOURNEY = 3

def save(lineage_class, root_hash="", previous_hash=""):
    out = {}
    has_lineage = lineage_class in (FIRST, CONTINUATION, NEW_JOURNEY) and len(root_hash) == 16
    if not has_lineage:
        return out
    if lineage_class == NEW_JOURNEY and len(previous_hash) != 16:
        raise ValueError("new journey requires previous root")
    out["LC"] = lineage_class
    out["L"] = root_hash
    out["LP"] = 1 if len(previous_hash) == 16 else 0
    if out["LP"]:
        out["N"] = previous_hash
    return out

def load(record):
    if "LC" not in record:
        return NONE, "", ""
    lineage_class = record["LC"]
    if lineage_class not in (FIRST, CONTINUATION, NEW_JOURNEY):
        raise ValueError("invalid class")
    root = record.get("L", "")
    if len(root) != 16 or "LP" not in record:
        raise ValueError("invalid root persistence")
    previous = record.get("N", "") if record["LP"] else ""
    if record["LP"] and len(previous) != 16:
        raise ValueError("invalid previous root")
    if lineage_class == NEW_JOURNEY and not previous:
        raise ValueError("new journey missing previous root")
    return lineage_class, root, previous

def main():
    a="A"*16
    b="B"*16
    assert load({}) == (NONE, "", "")
    assert load(save(FIRST,a)) == (FIRST,a,"")
    assert load(save(CONTINUATION,a)) == (CONTINUATION,a,"")
    assert load(save(NEW_JOURNEY,b,a)) == (NEW_JOURNEY,b,a)
    try:
        save(NEW_JOURNEY,b,"")
        raise AssertionError("missing previous root accepted")
    except ValueError:
        pass
    print("Q9_P11_LINEAGE_PERSISTENCE_MODEL=PASS")

if __name__ == "__main__":
    main()
