#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: fix_zenfix_extras.py /path/to/vlc")

root = Path(sys.argv[1]).resolve()
path = root / "modules/gui/qt/dialogs/dialogs_provider.cpp"
lines = path.read_text(encoding="utf-8").splitlines()

matches = 0
for i, line in enumerate(lines):
    if line.strip().startswith("safeOutput.replace("):
        lines[i] = '    safeOutput.replace(QStringLiteral("\'"), QStringLiteral("\\\\\'"));'
        matches += 1

if matches != 1:
    raise RuntimeError(f"expected one safeOutput.replace line, found {matches}")

path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Zenfix trim quote escaping fixed")
