"""Oyunun arayüzden bağımsız mantık katmanı."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
import time

TRAP_LETTERS = {"x", "z", "j", "q"}
DEFAULT_MAX_MISTAKES = 6
DEFAULT_GUESS_SECONDS = 20


class GuessResult(str, Enum):
    """Tahmin işleminden dönen sonuç türleri."""

    CORRECT = "correct"
    WRONG = "wrong"
    REPEATED = "repeated"
    INVALID = "invalid"
    WON = "won"
    LOST = "lost"


@dataclass(slots=True)
class GuessOutcome:
    """Tek bir tahmin işleminin sonucunu temsil eder."""

    result: GuessResult
    mistake_delta: int = 0
    revealed: bool = False


@dataclass(slots=True)
class GameState:
    """Uzaylıdan Kaçış oyununun anlık durumunu tutar."""

    sentence: str
    max_mistakes: int = DEFAULT_MAX_MISTAKES
    trap_letters: set[str] = field(default_factory=lambda: set(TRAP_LETTERS))
    guessed_letters: set[str] = field(default_factory=set)
    mistakes: int = 0
    hint_used: bool = False
    started_at: float = field(default_factory=time.time)
    hidden_sentence: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.sentence = self.sentence.lower()
        self.hidden_sentence = ["_" if char != " " else " " for char in self.sentence]

    @property
    def display_text(self) -> str:
        """Gizlenmiş cümlenin ekranda gösterilecek halini döndürür."""
        return " ".join(self.hidden_sentence)

    @property
    def guessed_text(self) -> str:
        """Tahmin edilen harfleri sıralı metin olarak döndürür."""
        return ", ".join(sorted(self.guessed_letters))

    @property
    def is_won(self) -> bool:
        """Tüm harflerin bulunup bulunmadığını döndürür."""
        return "_" not in self.hidden_sentence

    @property
    def is_lost(self) -> bool:
        """Hata hakkının dolup dolmadığını döndürür."""
        return self.mistakes >= self.max_mistakes

    @property
    def elapsed_seconds(self) -> int:
        """Oyunun toplam süresini saniye olarak döndürür."""
        return int(time.time() - self.started_at)

    def alien_distance_text(self) -> str:
        """Hata sayısına göre uzaylı yakınlığını gösteren metni üretir."""
        remaining = max(self.max_mistakes - self.mistakes, 0)
        return "🚀" + "-" * remaining + "👽"

    def guess(self, raw_letter: str) -> GuessOutcome:
        """Tek harflik tahmini işler."""
        letter = raw_letter.strip().lower()
        if len(letter) != 1 or not letter.isalpha():
            return GuessOutcome(GuessResult.INVALID)
        if letter in self.guessed_letters:
            return GuessOutcome(GuessResult.REPEATED)

        self.guessed_letters.add(letter)
        found = False
        for index, char in enumerate(self.sentence):
            if char == letter:
                self.hidden_sentence[index] = letter
                found = True

        if found:
            if self.is_won:
                return GuessOutcome(GuessResult.WON, revealed=True)
            return GuessOutcome(GuessResult.CORRECT, revealed=True)

        mistake_delta = 2 if letter in self.trap_letters else 1
        self.mistakes += mistake_delta
        if self.is_lost:
            return GuessOutcome(GuessResult.LOST, mistake_delta=mistake_delta)
        return GuessOutcome(GuessResult.WRONG, mistake_delta=mistake_delta)

    def apply_timeout_penalty(self) -> GuessOutcome:
        """Süre dolduğunda hata puanı ekler."""
        self.mistakes += 1
        if self.is_lost:
            return GuessOutcome(GuessResult.LOST, mistake_delta=1)
        return GuessOutcome(GuessResult.WRONG, mistake_delta=1)

    def reveal_hint(self) -> bool:
        """İlk harfi ipucu olarak açar ve bir hata cezası uygular."""
        if self.hint_used:
            return False
        first_letter = next((char for char in self.sentence if char != " "), "")
        if not first_letter:
            return False
        for index, char in enumerate(self.sentence):
            if char == first_letter:
                self.hidden_sentence[index] = first_letter
        self.guessed_letters.add(first_letter)
        self.hint_used = True
        self.mistakes += 1
        return True


def choose_sentence(sentences: list[str]) -> str:
    """Boş olmayan cümle listesinden rastgele bir cümle seçer."""
    clean_sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    if not clean_sentences:
        raise ValueError("En az bir cümle bulunmalıdır.")
    return random.choice(clean_sentences)
