import unittest

from uzaylidan_kacis_oyunu.game_logic import GameState, GuessResult, choose_sentence


class GameStateTests(unittest.TestCase):
    def test_sentence_hidden_with_spaces_preserved(self):
        state = GameState("uzay gemisi")
        self.assertEqual(state.display_text, "_ _ _ _   _ _ _ _ _ _")

    def test_correct_guess_reveals_all_matching_letters(self):
        state = GameState("masa")
        outcome = state.guess("a")
        self.assertEqual(outcome.result, GuessResult.CORRECT)
        self.assertEqual(state.display_text, "_ a _ a")

    def test_wrong_guess_increases_mistake(self):
        state = GameState("masa")
        outcome = state.guess("b")
        self.assertEqual(outcome.result, GuessResult.WRONG)
        self.assertEqual(state.mistakes, 1)

    def test_trap_letter_adds_two_mistakes(self):
        state = GameState("masa")
        outcome = state.guess("x")
        self.assertEqual(outcome.result, GuessResult.WRONG)
        self.assertEqual(state.mistakes, 2)

    def test_repeated_guess_is_ignored(self):
        state = GameState("masa")
        state.guess("m")
        outcome = state.guess("m")
        self.assertEqual(outcome.result, GuessResult.REPEATED)
        self.assertEqual(state.mistakes, 0)

    def test_invalid_guess_is_ignored(self):
        state = GameState("masa")
        outcome = state.guess("ab")
        self.assertEqual(outcome.result, GuessResult.INVALID)
        self.assertEqual(state.mistakes, 0)

    def test_hint_reveals_first_letter_and_adds_penalty(self):
        state = GameState("merhaba")
        revealed = state.reveal_hint()
        self.assertTrue(revealed)
        self.assertEqual(state.hidden_sentence[0], "m")
        self.assertEqual(state.mistakes, 1)
        self.assertFalse(state.reveal_hint())

    def test_win_condition(self):
        state = GameState("a")
        outcome = state.guess("a")
        self.assertEqual(outcome.result, GuessResult.WON)
        self.assertTrue(state.is_won)

    def test_timeout_penalty_can_lose_game(self):
        state = GameState("abc", max_mistakes=1)
        outcome = state.apply_timeout_penalty()
        self.assertEqual(outcome.result, GuessResult.LOST)
        self.assertTrue(state.is_lost)

    def test_choose_sentence_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            choose_sentence([])


if __name__ == "__main__":
    unittest.main()
