import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


class TestCheckGuessOutcomes:
    """Tests for check_guess outcome values."""

    def test_winning_guess(self):
        """Correct guess should return Win."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert "🎉" in message

    def test_guess_too_high_outcome(self):
        """Guess higher than secret should return Too High outcome."""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_too_low_outcome(self):
        """Guess lower than secret should return Too Low outcome."""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"


class TestHighLowMessageBug:
    """Tests specifically for the high/low message bug fix.

    Bug: Messages were reversed. "Too High" was saying "Go HIGHER!" instead of "Go LOWER!"
    """

    def test_too_high_message_says_go_lower(self):
        """When guess is too high, message should tell player to go LOWER."""
        outcome, message = check_guess(100, 50)
        assert outcome == "Too High"
        assert "LOWER" in message
        assert "HIGHER" not in message

    def test_too_low_message_says_go_higher(self):
        """When guess is too low, message should tell player to go HIGHER."""
        outcome, message = check_guess(10, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message
        assert "LOWER" not in message

    def test_correct_message_is_correct(self):
        """Correct guess should show Correct message."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in message


class TestStringConversionBug:
    """Tests for the string conversion bug fix.

    Bug: On even attempts, the code converted secret to string, causing string comparison
    instead of numeric comparison, leading to incorrect high/low logic using ASCII values.
    """

    def test_numeric_comparison_with_integers(self):
        """check_guess should work correctly with integer comparisons."""
        outcome, message = check_guess(75, 50)
        assert outcome == "Too High"

    def test_numeric_comparison_consistency(self):
        """Comparing same values should always give same result."""
        # Test that guess > secret is always treated as "Too High"
        assert check_guess(101, 50)[0] == "Too High"
        assert check_guess(100, 50)[0] == "Too High"
        assert check_guess(99, 50)[0] == "Too High"
        assert check_guess(51, 50)[0] == "Too High"

    def test_numeric_comparison_low_consistency(self):
        """Comparing same values should always give same result for low."""
        # Test that guess < secret is always treated as "Too Low"
        assert check_guess(49, 50)[0] == "Too Low"
        assert check_guess(1, 50)[0] == "Too Low"
        assert check_guess(0, 50)[0] == "Too Low"
        assert check_guess(-10, 50)[0] == "Too Low"

    def test_no_string_conversion_large_numbers(self):
        """Large numbers should still be compared numerically, not as strings."""
        # In string comparison, "9" > "10" (ASCII), but numerically 9 < 10
        outcome, _ = check_guess(9, 10)
        assert outcome == "Too Low"

        outcome, _ = check_guess(90, 10)
        assert outcome == "Too High"


class TestParseGuessValidation:
    """Tests for parse_guess input validation."""

    def test_parse_valid_integer(self):
        """Valid integer string should parse correctly."""
        ok, value, error = parse_guess("42")
        assert ok is True
        assert value == 42
        assert error is None

    def test_parse_float_as_integer(self):
        """Float string should be converted to integer."""
        ok, value, error = parse_guess("42.7")
        assert ok is True
        assert value == 42
        assert error is None

    def test_parse_none_input(self):
        """None input should return error."""
        ok, value, error = parse_guess(None)
        assert ok is False
        assert value is None
        assert error == "Enter a guess."

    def test_parse_empty_string(self):
        """Empty string should return error."""
        ok, value, error = parse_guess("")
        assert ok is False
        assert value is None
        assert error == "Enter a guess."

    def test_parse_non_numeric_input(self):
        """Non-numeric input should return error."""
        ok, value, error = parse_guess("abc")
        assert ok is False
        assert value is None
        assert error == "That is not a number."

    def test_parse_negative_number(self):
        """Negative numbers should parse successfully."""
        ok, value, error = parse_guess("-42")
        assert ok is True
        assert value == -42
        assert error is None

    def test_parse_zero(self):
        """Zero should parse successfully."""
        ok, value, error = parse_guess("0")
        assert ok is True
        assert value == 0
        assert error is None


class TestGetRangeForDifficulty:
    """Tests for difficulty range selection."""

    def test_easy_range(self):
        """Easy difficulty should return 1-20 range."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_normal_range(self):
        """Normal difficulty should return 1-100 range."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_hard_range(self):
        """Hard difficulty should return 1-50 range."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50

    def test_unknown_difficulty_defaults_to_normal(self):
        """Unknown difficulty should default to Normal range."""
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1
        assert high == 100


class TestUpdateScore:
    """Tests for score update logic."""

    def test_winning_score_first_attempt(self):
        """Winning on first attempt should give 80 points."""
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_winning_score_second_attempt(self):
        """Winning on second attempt should give 70 points."""
        new_score = update_score(0, "Win", 2)
        assert new_score == 70

    def test_winning_score_caps_at_10(self):
        """Winning after many attempts should cap at 10 points."""
        new_score = update_score(0, "Win", 20)
        assert new_score == 10

    def test_too_high_even_attempt_adds_points(self):
        """Too High on even attempt should add 5 points."""
        new_score = update_score(0, "Too High", 2)
        assert new_score == 5

    def test_too_high_odd_attempt_subtracts_points(self):
        """Too High on odd attempt should subtract 5 points."""
        new_score = update_score(10, "Too High", 1)
        assert new_score == 5

    def test_too_low_always_subtracts_points(self):
        """Too Low should always subtract 5 points."""
        assert update_score(10, "Too Low", 1) == 5
        assert update_score(10, "Too Low", 2) == 5
        assert update_score(10, "Too Low", 10) == 5

    def test_score_accumulation(self):
        """Score should accumulate correctly over multiple outcomes."""
        score = 0
        score = update_score(score, "Too High", 2)  # +5
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 3)   # -5
        assert score == -5


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_game_flow_win(self):
        """Test a complete game flow from guess to win."""
        secret = 50

        # First guess too low
        ok, guess1, _ = parse_guess("30")
        assert ok
        outcome1, _ = check_guess(guess1, secret)
        assert outcome1 == "Too Low"

        # Second guess too high
        ok, guess2, _ = parse_guess("70")
        assert ok
        outcome2, _ = check_guess(guess2, secret)
        assert outcome2 == "Too High"

        # Third guess correct
        ok, guess3, _ = parse_guess("50")
        assert ok
        outcome3, _ = check_guess(guess3, secret)
        assert outcome3 == "Win"

    def test_score_accumulation_with_real_guesses(self):
        """Test score accumulation through a realistic game."""
        secret = 50
        score = 0
        attempt = 1

        # Attempt 1: Too low
        ok, guess, _ = parse_guess("30")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -5

        # Attempt 2: Too high
        attempt = 2
        ok, guess, _ = parse_guess("70")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == 0  # -5 + 5

        # Attempt 3: Correct
        attempt = 3
        ok, guess, _ = parse_guess("50")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == 60  # 0 + (100 - 10*(3+1)) = 0 + 60


class TestDebugInfoAccuracy:
    """Tests for Debug Info display accuracy.

    Bug: Developer Debug Info was showing stale state values when placed early in page render.
    This test ensures the final score calculation is always accurate for display purposes.
    """

    def test_win_score_displayed_correctly_after_multiple_wrong_guesses(self):
        """Final score should reflect all wrong guesses plus win bonus."""
        secret = 52
        score = 0
        attempt = 1

        # Wrong guess 1: Too Low
        ok, guess, _ = parse_guess("25")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -5

        # Wrong guess 2: Too Low
        attempt = 2
        ok, guess, _ = parse_guess("50")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -10

        # Wrong guess 3: Too High (odd attempt)
        attempt = 3
        ok, guess, _ = parse_guess("75")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -15

        # Wrong guess 4: Too High (even attempt, +5)
        attempt = 4
        ok, guess, _ = parse_guess("65")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -10

        # Wrong guess 5: Too Low
        attempt = 5
        ok, guess, _ = parse_guess("55")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        assert score == -15

        # Winning guess 6
        attempt = 6
        ok, guess, _ = parse_guess("52")
        outcome, _ = check_guess(guess, secret)
        score = update_score(score, outcome, attempt)
        # Win bonus: 100 - 10*(6+1) = 100 - 70 = 30
        assert score == 15

    def test_score_consistency_across_attempt_numbers(self):
        """Score should be consistent regardless of when it's displayed."""
        secret = 50
        score = 0

        # Simulate several attempts
        for attempt in range(1, 6):
            score = update_score(score, "Too Low", attempt)

        # After 5 "Too Low" attempts, score should be -25
        assert score == -25

        # Win on attempt 6 should add exactly 30 points
        win_score = update_score(score, "Win", 6)
        assert win_score == 5
