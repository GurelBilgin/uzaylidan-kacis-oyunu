"""Skor kayıt işlemleri."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


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
    """Skorları düz metin dosyasında saklar."""

    def __init__(self, path: Path | str = "scores.txt") -> None:
        self.path = Path(path)

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
