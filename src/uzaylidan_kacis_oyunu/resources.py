"""Paket içi varlık dosyalarına erişim yardımcıları."""

from __future__ import annotations

from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from typing import Iterator

_PACKAGE = "uzaylidan_kacis_oyunu.assets"


@contextmanager
def asset_path(filename: str) -> Iterator[Path]:
    """Paket içindeki bir asset dosyası için geçici/fiziksel dosya yolu döndürür."""
    resource = resources.files(_PACKAGE).joinpath(filename)
    with resources.as_file(resource) as path:
        yield path


def read_lines(filename: str) -> list[str]:
    """Paket içindeki metin dosyasını satır listesi olarak okur."""
    text = resources.files(_PACKAGE).joinpath(filename).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]
