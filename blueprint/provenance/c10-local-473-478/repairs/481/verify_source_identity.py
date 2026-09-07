#!/usr/bin/env python3
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = (HERE / "../../source_view/BBMA_EA.mq4").resolve()
EXPECTED_FILE = "5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57"
EXPECTED_EMBEDDED = "D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D"
raw = SRC.read_bytes()
file_hash = hashlib.sha256(raw).hexdigest().upper()
if file_hash != EXPECTED_FILE:
    raise SystemExit(f"FILE_SHA_MISMATCH {file_hash}")
text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
match = re.search(r'(#define C10_SOURCE_HASH\s+")([A-F0-9]{64})(")', text)
if not match or match.group(2) != EXPECTED_EMBEDDED:
    raise SystemExit("EMBEDDED_HASH_LITERAL_MISMATCH")
canonical = text[:match.start(2)] + ("0" * 64) + text[match.end(2):]
computed = hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()
if computed != EXPECTED_EMBEDDED:
    raise SystemExit(f"EMBEDDED_HASH_RECOMPUTE_MISMATCH {computed}")
if '"4.80"' in text or '"4.79"' in text or '"4.78"' in text:
    raise SystemExit("STALE_BUILD_LITERAL")
print("C10_481_SOURCE_FILE_SHA=PASS")
print("C10_481_EMBEDDED_SOURCE_HASH=PASS")
print("C10_481_NO_STALE_BUILD_LITERAL=PASS")
