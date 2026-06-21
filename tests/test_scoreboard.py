import tempfile
import unittest
from pathlib import Path

from uzaylidan_kacis_oyunu.scoreboard import ScoreBoard


class ScoreBoardTests(unittest.TestCase):
    def test_empty_scoreboard_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = ScoreBoard(Path(tmp) / "scores.txt")
            self.assertIn("Henüz", board.read_text())

    def test_append_score_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scores.txt"
            board = ScoreBoard(path)
            board.append("KAZANDI", "uzay gemisi", 42)
            content = board.read_text()
            self.assertIn("KAZANDI", content)
            self.assertIn("uzay gemisi", content)
            self.assertIn("42 saniye", content)


if __name__ == "__main__":
    unittest.main()
