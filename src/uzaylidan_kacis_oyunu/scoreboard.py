"""Skor kayıt işlemleri."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

APP_DIR_NAME = "UzaylidanKacisOyunu"
SCORE_FILE_NAME = "scores.txt"


def user_data_dir(app_name: str = APP_DIR_NAME) -> Path:
    """Kullanıcıya özel uygulama veri klasörünü döndürür.

    EXE dosyasının bulunduğu klasöre yazmak yerine skor dosyası kullanıcı
    profilindeki uygulama veri klasöründe tutulur. Böylece kullanıcı EXE'yi
    masaüstünden, indirilenlerden veya salt okunur bir klasörden çalıştırsa bile
    skor kaydı güvenli şekilde oluşturulur.
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / app_name
        return Path.home() / "AppData" / "Roaming" / app_name

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / app_name

    base = os.environ.get("XDG_DATA_HOME")
    if base:
        return Path(base) / app_name
    return Path.home() / ".local" / "share" / app_name


def default_score_path() -> Path:
    """Varsayılan skor dosyası yolunu döndürür."""
    return user_data_dir() / SCORE_FILE_NAME


@dataclass(slots=True)
class ScoreRecord:
    """Tek bir oyun sonucunu temsil eder."""

    date: str
    result: str
    sentence: str
    elapsed_seconds: int

    def to_line(self) -> str:
        return f"{self.date} | {self.result} | {self.sentence} | {self.elapsed_seconds} saniye"


class ScoreBoard:
    """Skorları kullanıcı veri klasöründeki düz metin dosyasında saklar."""

    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path is not None else default_score_path()

    def append(self, result: str, sentence: str, elapsed_seconds: int) -> None:
        """Yeni skor kaydı ekler."""
        record = ScoreRecord(
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            result=result,
            sentence=sentence,
            elapsed_seconds=elapsed_seconds,
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(record.to_line() + "\n")

    def read_text(self) -> str:
        """Skor dosyasının içeriğini döndürür."""
        if not self.path.exists():
            return "Henüz hiç skor kaydedilmedi."
        content = self.path.read_text(encoding="utf-8").strip()
        return content or "Henüz hiç skor kaydedilmedi."
