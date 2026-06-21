"""Tkinter arayüzü."""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox

from .game_logic import DEFAULT_GUESS_SECONDS, GameState, GuessResult, choose_sentence
from .resources import asset_path, read_lines
from .scoreboard import ScoreBoard
from .sound import SoundPlayer


class UzayliKacisApp:
    """Uzaylıdan Kaçış oyununun Tkinter uygulaması."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Uzaylıdan Kaçış")
        self.root.geometry("620x560")
        self.root.minsize(580, 520)
        self.root.configure(bg="#121212")
        self._set_icon()

        self.sentences = read_lines("cumleler.txt")
        self.scoreboard = ScoreBoard()
        self.sound_player = SoundPlayer()
        self.state: GameState | None = None
        self.turn_started_at = time.time()
        self.after_id: str | None = None
        self.game_active = False

        self.font_title = ("Segoe UI", 26, "bold")
        self.font_label = ("Segoe UI", 14)
        self.font_button = ("Segoe UI", 13, "bold")

        self.show_home_screen()

    def _set_icon(self) -> None:
        try:
            with asset_path("app_icon.ico") as path:
                self.root.iconbitmap(str(path))
        except Exception:
            pass

    def _play_sound(self, filename: str) -> None:
        with asset_path(filename) as path:
            self.sound_player.play(path)

    def _clear_window(self) -> None:
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home_screen(self) -> None:
        self.game_active = False
        self._clear_window()

        title = tk.Label(
            self.root,
            text="🚀 Uzaylıdan Kaçış 🚀",
            font=self.font_title,
            bg="#121212",
            fg="#00ffe7",
        )
        title.pack(pady=(45, 25))

        subtitle = tk.Label(
            self.root,
            text="Cümleyi süre dolmadan tahmin et, uzaylı sana yetişmesin!",
            font=("Segoe UI", 12),
            bg="#121212",
            fg="#e0f7fa",
        )
        subtitle.pack(pady=(0, 20))

        self._create_button("Oyunu Başlat", self.start_game, "#00bfa5", "#121212").pack(pady=12)
        self._create_button("Skorları Göster", self.show_scores, "#00796b", "white").pack(pady=5)

    def _create_button(self, text: str, command, bg: str, fg: str) -> tk.Button:
        return tk.Button(
            self.root,
            text=text,
            font=self.font_button,
            bg=bg,
            fg=fg,
            activebackground="#00e5ff",
            activeforeground="#121212",
            relief="flat",
            padx=24,
            pady=9,
            command=command,
        )

    def show_scores(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Skorlar")
        window.geometry("560x360")
        window.configure(bg="#121212")

        tk.Label(window, text="Skor Kayıtları", font=self.font_title, bg="#121212", fg="#00ffe7").pack(pady=15)
        text_area = tk.Text(window, height=14, width=64, bg="#263238", fg="#e0f7fa", font=self.font_label, relief="flat")
        text_area.pack(padx=15, pady=10)
        text_area.insert("1.0", self.scoreboard.read_text())
        text_area.config(state="disabled")

    def start_game(self) -> None:
        sentence = choose_sentence(self.sentences)
        self.state = GameState(sentence=sentence)
        self.turn_started_at = time.time()
        self.game_active = True
        self._build_game_screen()
        self._start_timer()

    def _build_game_screen(self) -> None:
        self._clear_window()
        self.root.configure(bg="#121212")

        self.sentence_label = tk.Label(
            self.root,
            text=self.state.display_text if self.state else "",
            font=("Consolas", 25, "bold"),
            bg="#121212",
            fg="#00ffe7",
            wraplength=560,
        )
        self.sentence_label.pack(pady=20)

        guess_frame = tk.Frame(self.root, bg="#121212")
        guess_frame.pack(pady=10)

        self.guess_entry = tk.Entry(
            guess_frame,
            font=("Segoe UI", 20),
            width=3,
            justify="center",
            bg="#263238",
            fg="#e0f7fa",
            relief="flat",
            insertbackground="white",
        )
        self.guess_entry.pack(side="left", padx=(0, 10))
        self.guess_entry.bind("<Return>", self.handle_guess)
        self.guess_entry.focus_set()

        tk.Button(
            guess_frame,
            text="Tahmin Et",
            command=self.handle_guess,
            bg="#00bfa5",
            fg="#121212",
            relief="flat",
            padx=20,
            pady=8,
            font=self.font_button,
        ).pack(side="left")

        self.timer_label = tk.Label(self.root, text=f"Süre: {DEFAULT_GUESS_SECONDS}", font=self.font_label, bg="#121212", fg="#e0f7fa")
        self.timer_label.pack(pady=(15, 0))

        self.alien_label = tk.Label(
            self.root,
            text=self.state.alien_distance_text() if self.state else "",
            font=("Consolas", 28),
            bg="#121212",
            fg="#00ffe7",
        )
        self.alien_label.pack(pady=20)

        self.hint_button = tk.Button(
            self.root,
            text="İpucu Al (1 hakkın var)",
            command=self.reveal_hint,
            bg="#00796b",
            fg="white",
            relief="flat",
            padx=15,
            pady=7,
            font=self.font_button,
        )
        self.hint_button.pack(pady=(0, 20))

        self.guessed_label = tk.Label(self.root, text="Tahmin Edilen Harfler: ", font=self.font_label, bg="#121212", fg="#e0f7fa")
        self.guessed_label.pack(pady=5)

    def _start_timer(self) -> None:
        if not self.game_active or self.state is None:
            return

        elapsed = int(time.time() - self.turn_started_at)
        remaining = max(DEFAULT_GUESS_SECONDS - elapsed, 0)
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.config(text=f"Süre: {remaining}")

        if remaining <= 0:
            outcome = self.state.apply_timeout_penalty()
            if outcome.result == GuessResult.LOST:
                self.finish_game(won=False)
                return
            self._next_turn()
        else:
            self.after_id = self.root.after(250, self._start_timer)

    def handle_guess(self, event=None) -> None:
        if not self.game_active or self.state is None:
            return

        letter = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END)
        outcome = self.state.guess(letter)

        if outcome.result in {GuessResult.INVALID, GuessResult.REPEATED}:
            return

        self._update_game_labels()
        if outcome.result in {GuessResult.CORRECT, GuessResult.WON}:
            self._play_sound("correct.wav")
        else:
            self._play_sound("wrong.wav")

        if outcome.result == GuessResult.WON:
            self.finish_game(won=True)
        elif outcome.result == GuessResult.LOST:
            self.finish_game(won=False)
        else:
            self._next_turn()

    def _update_game_labels(self) -> None:
        if self.state is None:
            return
        self.sentence_label.config(text=self.state.display_text)
        self.alien_label.config(text=self.state.alien_distance_text())
        self.guessed_label.config(text="Tahmin Edilen Harfler: " + self.state.guessed_text)

    def _next_turn(self) -> None:
        self._update_game_labels()
        self.turn_started_at = time.time()
        self._start_timer()

    def reveal_hint(self) -> None:
        if not self.game_active or self.state is None:
            return
        if self.state.reveal_hint():
            self._update_game_labels()
            self.hint_button.config(state="disabled")
            if self.state.is_lost:
                self.finish_game(won=False)
            elif self.state.is_won:
                self.finish_game(won=True)

    def finish_game(self, won: bool) -> None:
        if self.state is None:
            return
        self.game_active = False
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        result = "KAZANDI" if won else "KAYBETTİ"
        elapsed_seconds = self.state.elapsed_seconds
        self.scoreboard.append(result=result, sentence=self.state.sentence, elapsed_seconds=elapsed_seconds)
        self._play_sound("win.wav" if won else "lose.wav")

        self._clear_window()
        message = f"{result}!\nSüre: {elapsed_seconds} saniye"
        if not won:
            message += f"\nDoğru Cevap: {self.state.sentence}"

        tk.Label(self.root, text=message, font=("Segoe UI", 18, "bold"), bg="#121212", fg="#00ffe7").pack(pady=40)
        self._create_button("Oyunu Tekrar Oyna", self.start_game, "#00bfa5", "#121212").pack(pady=10)
        self._create_button("Ana Menüye Dön", self.show_home_screen, "#00796b", "white").pack(pady=5)


def run_app() -> None:
    """Tkinter uygulamasını başlatır."""
    root = tk.Tk()
    UzayliKacisApp(root)
    root.mainloop()
