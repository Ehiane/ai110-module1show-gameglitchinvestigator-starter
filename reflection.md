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
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
