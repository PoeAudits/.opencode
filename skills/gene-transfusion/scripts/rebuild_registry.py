#!/usr/bin/env python3

"""Deprecated wrapper.

Use:
  ~/.agents/skills/gene-development/scripts/rebuild_registry.py
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    target = (
        Path.home()
        / ".agents"
        / "skills"
        / "gene-development"
        / "scripts"
        / "rebuild_registry.py"
    )
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
