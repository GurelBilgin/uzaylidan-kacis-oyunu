"""Uygulama giriş noktası."""

from __future__ import annotations

import sys
from pathlib import Path


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from uzaylidan_kacis_oyunu.gui import run_app


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
