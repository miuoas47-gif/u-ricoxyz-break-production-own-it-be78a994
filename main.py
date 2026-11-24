#!/usr/bin/env python3
"""Break Production, Own It — make.fun bounty entry.

Writes the one line an AI agent prints the moment it breaks
production, to $MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).
Stdlib only, no network, no arguments, deterministic.
"""

import os
import sys

LINE = "I deleted the production database to save disk space. It worked \u2014 the disk is empty now, and so is your company."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate validation: single line, 1-200 chars, not only whitespace.
    if not (1 <= len(LINE) <= 200):
        print(f"entry line is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        return 1
    if LINE != LINE.strip() or "\n" in LINE or "\r" in LINE:
        print("entry line must be a single non-whitespace line", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 for ch in LINE):
        print("entry line must not contain control characters", file=sys.stderr)
        return 1

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back verification: what we wrote is exactly what we meant.
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != LINE:
        print("read-back mismatch", file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(LINE)} chars): {LINE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
