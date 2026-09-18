from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PYTHON = "3.12.14"
EXPECTED_REQUIREMENTS = [
    "asgiref==3.12.1",
    "Django==5.2.17",
    "sqlparse==0.6.0",
]

failures: list[str] = []

def expect(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)

python_version = ".".join(map(str, sys.version_info[:3]))
expect(
    python_version == EXPECTED_PYTHON,
    f"Python must be {EXPECTED_PYTHON}; got {python_version}",
)

python_version_file = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
expect(
    python_version_file == EXPECTED_PYTHON,
    f".python-version must pin {EXPECTED_PYTHON}",
)

requirements = [
    line.strip()
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
expect(
    requirements == EXPECTED_REQUIREMENTS,
    "requirements.txt must match the verified B1 runtime graph exactly",
)

tracked = subprocess.check_output(
    ["git", "ls-files"],
    cwd=ROOT,
    text=True,
).splitlines()

for path in tracked:
    expect("__pycache__/" not in path, f"tracked Python cache found: {path}")
    expect(not path.endswith(".pyc"), f"tracked bytecode found: {path}")
    expect(not path.endswith("db.sqlite3"), f"tracked local SQLite state found: {path}")

expect((ROOT / "trabajocero" / "polls" / "migrations" / "0001_initial.py").exists(),
       "schema migration authority must remain tracked")

if failures:
    print("B1 repository hygiene contract failed:", file=sys.stderr)
    for failure in failures:
        print(f"- {failure}", file=sys.stderr)
    raise SystemExit(1)

print("B1 repository hygiene contract passed.")
print(f"python={python_version}")
print("requirements=exact")
print("tracked-python-cache=0")
print("tracked-local-sqlite=0")
