import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from uzaylidan_kacis_oyunu.scoreboard import ScoreBoard, default_score_path, user_data_dir


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

    def test_default_score_path_uses_appdata_on_windows(self):
        appdata = r"C:\Users\ahmet\AppData\Roaming"
        with patch("sys.platform", "win32"), patch.dict("os.environ", {"APPDATA": appdata}, clear=True):
            path = default_score_path()
            self.assertTrue(str(path).startswith(appdata))
            self.assertEqual(path.name, "scores.txt")
            self.assertEqual(path.parent.name, "UzaylidanKacisOyunu")

    def test_user_data_dir_uses_xdg_on_linux(self):
        with patch("sys.platform", "linux"), patch.dict("os.environ", {"XDG_DATA_HOME": "/tmp/appdata"}, clear=True):
            self.assertEqual(user_data_dir(), Path("/tmp/appdata") / "UzaylidanKacisOyunu")


if __name__ == "__main__":
    unittest.main()
