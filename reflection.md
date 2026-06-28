# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  * It felt broken. It prompting me to go lower until I eventually got to 1 and it still told me to go lower. At the end of my chances, the correct answer was 88, which was in fact higher than my previous answer. 

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  *  The hints are incorrect.
  *  Boundaries of the guesses are not being identified. (e.g. 1< answers and >100 answers being accepted)
  *  After the game ends, the terminal logs show a connection ResetError. This doesn't fix itself until I reload the page. 


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|guess of 50 | "Go Higher"  | "Go Lower" |  None|
|guess of -15  | "Out of bounds" | "Go Lower" | None|
|new game  | whole new game session | it was stuck on the "Game over. Start new game to try again." | ```ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host```  |
|... | ...  | ... |  ... |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  * Claude Haiku
  
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  * Claude suggested that the reason the comparisons were off was because of how Even attempts were being judged based of their ascii value rather than their numerical value. 

  Here is Claude's response:
    ```
    The Core Bug: Backwards Hints

    The main issue is in app.py:158-161. On every even-numbered attempt, the secret number is converted to a string:


    if st.session_state.attempts % 2 == 0:
        secret = str(st.session_state.secret)
    else:
        secret = st.session_state.secret
    This causes the comparison in check_guess() to flip:

    Odd attempts (1, 3, 5...): Normal comparison works correctly (int vs int)
    Even attempts (2, 4, 6...): The secret becomes a string, so check_guess() falls into the TypeError exception handler that does string comparison (lines 42-47 in app.py)
    Why String Comparison Gives Backwards Hints:

    When comparing strings lexicographically:

    "50" > "88" is True (because "5" > "8" alphabetically) ❌
    But numerically, 50 < 88 ✓
    So when you guess 50 and the secret is 88:

    Attempt 2 (even): Secret becomes "88", code compares "50" > "88" → True → returns "Go HIGHER!" (backwards!)
    Attempt 3 (odd): Secret is 88 (int), code compares 50 > 88 → False → returns "Go LOWER!" (backwards!)
    ```

    I verivied the result by rerunning streamlit and playing a session, and it worked as expected. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  * An example that was misleading was during the test. It provided the incorrect expected answer for a test because it didn't fully understand the logic behind `update_score`

  ```
  The tests are failing because the scoring formula is different than expected. Let me check the actual update_score function to see what the correct values should be:

  Read c:...\CodePath\AI-110\ai110-module1show-gameglitchinvestigator-starter\logic_utils.py (lines 52-67)
  I see! The formula is 100 - 10 * (attempt_number + 1). Let me verify:

  Attempt 1: 100 - 10 * (1 + 1) = 100 - 20 = 80 (not 90)
  Attempt 2: 100 - 10 * (2 + 1) = 100 - 30 = 70 (not 80)
  Let me fix the tests to match the actual formula:
  ...
  ```

  ```
  Perfect! I've fixed the three failing tests. The issue was with the scoring formula - it uses 100 - 10 * (attempt_number + 1), so:

  Attempt 1 win: 100 - 10(2) = 80 points (was expecting 90)
  Attempt 2 win: 100 - 10(3) = 70 points (was expecting 80)
  Attempt 3 win: 100 - 10(4) = 60 points (was expecting 70)
  ```

  I verified the correction by rerunning the pytest and all tests passed. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  * I ran that same exact scenario through the game and it provided the correct result after claude claimed to fix the bug. 

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  This test class `TestCheckGuessOutcomes` that I ran through pytest, verified the comparison problem I was having prior to the fix. It was needed to verify that the hints being provided to the user are actually correct and not misleading. 
  
  ```
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
  ```
- Did AI help you design or understand any tests? How?

  * Yes, I used this prompt in the same chat session of my refactoring changes:
    ```
    generate a pytest cases in test/test_game_logic.py that specifically targets the bugs we just fixed
    ```
    That way claude had the exact context needed to generate the test needed to verify not only the refactoring change, but the logical changes as well. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
