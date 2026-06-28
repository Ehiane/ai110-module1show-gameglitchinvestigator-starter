def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX ME: The logic breaks here
# Bug: this function has no boundary checking, it accepts any integer without validating it's low and high range. 
# Fix: Add boundary checking to ensure the guess is within the range defined by the difficulty level.
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX ME: The logic breaks here
# Bug: On even numbers it compares string values to int values, using ascii values as the numerical value of the string, causing an unexpected behavior. 
# FIX: Removed string comparison logic that was causing backwards hints on even attempts
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    return current_score


def explain_score(current_score: int, history: list, attempts: int):
    """Generate a human-readable explanation of how the current score was calculated."""
    if not history:
        return "Score starts at 0. Make your first guess!"

    explanation = "Score Breakdown:\n"
    running_score = 0

    for i, guess in enumerate(history):
        attempt_num = i + 1

        if attempt_num == attempts and attempt_num == len(history):
            points = 100 - 10 * (attempt_num + 1)
            if points < 10:
                points = 10
            explanation += f"• Attempt {attempt_num} (Won): +{points} = {running_score + points}\n"
            running_score += points
        else:
            if attempt_num % 2 == 0:
                points = 5
                explanation += f"• Attempt {attempt_num} (Wrong, even): +5 = {running_score + 5}\n"
                running_score += 5
            else:
                points = -5
                explanation += f"• Attempt {attempt_num} (Wrong, odd): -5 = {running_score - 5}\n"
                running_score -= 5

    return explanation
