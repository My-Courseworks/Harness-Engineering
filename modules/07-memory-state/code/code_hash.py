"""The hash of the code a pass runs on: every file under code/ except evidence, var and caches, one sha256 per file
and one over the list.

    python code_hash.py            # prints the per-file lines and the combined hash
    python code_hash.py --short    # the combined hash only

A declared-final pass records the output before it starts (evidence/final-pass-code.sha256) and checks it unchanged
after; anyone can recompute it on the commit the pass names.
"""

import hashlib
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
SKIP = ("evidence", "var", ".venv", "__pycache__")


def file_lines() -> list[str]:
    lines = []
    for path in sorted(CODE_DIR.rglob("*")):
        rel = path.relative_to(CODE_DIR)
        if not path.is_file() or any(part in SKIP for part in rel.parts) or rel.name == "README.md":
            continue
        if path.suffix not in (".py", ".md", ".json", ".txt"):
            continue
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  ./{rel.as_posix()}")
    return lines


def main() -> None:
    lines = file_lines()
    combined = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    if "--short" in sys.argv:
        print(combined)
        return
    print("\n".join(lines))
    print(f"combined sha256: {combined}")


if __name__ == "__main__":
    main()
