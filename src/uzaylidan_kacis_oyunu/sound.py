"""Ses çalma yardımcıları."""

from __future__ import annotations

from pathlib import Path


class SoundPlayer:
    """Pygame kullanarak ses çalar; ses altyapısı yoksa sessiz çalışır."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self._pygame = None
        if enabled:
            try:
                import pygame

                pygame.mixer.init()
                self._pygame = pygame
            except Exception:
                self.enabled = False
                self._pygame = None

    def play(self, path: Path) -> None:
        """Verilen ses dosyasını çalmayı dener."""
        if not self.enabled or self._pygame is None or not path.exists():
            return
        try:
            self._pygame.mixer.music.load(str(path))
            self._pygame.mixer.music.play()
        except Exception:
            # Ses hataları oyunun çalışmasını engellememeli.
            return
