# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The first time running the game, it has settings to adjust difficulty levels of the game on the left pane. The main window/view has a title, subtitle, info showing the game stats, developer debug info dropdown (closed by default), input box to enter a player's guess, two buttons to submit guess and reset a new game, and a checkbox to choose to show hint. The difficulty settings on the left pane has 3 options: Easy, Normal, Hard. Opening the Developer Debug Info, it reveals the secret, attempts, score, difficulty selected, and a history list. When running first time, the game loaded, it already showed something wrong before I even made a guess. The "attempts left" display was off by one, since it said 7 instead of 8 on Normal difficulty. The info banner said "Guess a number between 1 and 100" no matter which difficulty was selected, so Easy and Hard modes showed the wrong range. Overall, the game looked like it ran without crashing, but the information it showed the player was incorrect right from the start.

- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

  First bug is that the "Attempts left" showing on the info bar below the subtitle "Make a guess" is 1 less than the "Attempts allowed" shown on the left pane settings. The expected behavior is that "Attempts left" should match "Attempts allowed", which means that the game should start with full attempts and usually count only when actual guesses made. The code-level cause for this bug is the immediate initialization to 1 in app.py in line 96. Second bug is that the game/the info bar display always says "between 1 and 100" regardless of changing the difficulty settings. The expected behavior is that the main UI info bar display should reflect the actual low/high values for selected difficulty. The code-level cause for this bug is the hardcoded st.info in app.py in line 110. Third bug is that the hint directions are reversed. A high guess returns "Too High" but message says "Go HIGHER!"; low guess says "Go LOWER!". This leads the player in the wrong direction. The expected behavior is that high guess should say go lower; low guess should say go higher. The code-level cause for this bug is the reversed logic in app.py from line 37 to 40.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude Code (Anthropic's CLI tool) as my AI pair-programming partner throughout the project. Claude Code was able to read the entire codebase, identify bugs, suggest fixes, and generate test cases all within the same conversation. It worked like having a second pair of eyes that could scan every file at once and spot issues I might have missed on my own.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude correctly identified that the hint messages in `check_guess()` were swapped, when a guess was too high, the code returned "Go HIGHER!" instead of "Go LOWER!". I verified this by running `check_guess(75, 50)` directly in Python and seeing that it returned "Go HIGHER!" when the guess was above the secret. After applying the fix and clearing the Python bytecode cache, re-running the same call returned "Go LOWER!" as expected, confirming the fix was correct.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  When Claude first generated pytest cases for the attempt counter bug, the tests only used local variables (like `state = {}` and `state["attempts"] = 0`) instead of actually checking the real `app.py` source code. These tests would always pass even if the bug came back, because they were just testing themselves, but not the actual application. I caught this by reviewing the test logic and realizing the tests had no connection to `app.py` at all. After pointing this out, Claude rewrote the tests to parse the real `app.py` file using Python's `ast` module, which made them true verification tests.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  For each fix, I followed a 2-step check. First, I ran the pytest cases to make sure they passed with the fix in place, and then I temporarily reverted the fix to confirm the tests would actually fail. This "break it on purpose" step was important because it proved the tests were truly tied to the real code and not just passing by coincidence. If a test still passes after you undo the fix, it is not really testing anything useful. This approach gave me confidence that the tests would catch the bug if someone accidentally reintroduced it later.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

  I ran `test_too_high_hint_says_go_lower`, which calls `check_guess(75, 50)` and checks that the returned message contains "LOWER" and does not contain "HIGHER". When I first ran it after fixing the source code, it still failed. This was confusing since the file looked correct. It turned out Python was loading a stale `.pyc` cache file with the old buggy code. After clearing the `__pycache__` directory and re-running, the test passed. This taught me that editing a `.py` file does not always mean Python will use the updated version right away.

- Did AI help you design or understand any tests? How?

  Yes, Claude designed all the pytest cases, but the first round needed correction. Claude initially wrote tests that used hardcoded local variables instead of reading from the actual source files, which meant they were not real verification tests. After I pointed out the problem, Claude rewrote them using Python's `ast` module to parse the real `app.py` and `logic_utils.py` source code. This was a good example of how AI can get you 80% of the way there quickly, but you still need to review its output to make sure the logic actually makes sense.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit works differently from most web apps. For each time you click a button or change an input, the entire Python script runs again from top to bottom. This means that any regular variable you set will get reset to its starting value on every interaction, which would make it impossible to keep track of things like the player's score or guess count. That is where `st.session_state` comes in: it is like a special dictionary that survives between reruns, so you can store values there and they will still be there the next time the script runs. I'd like to think of it like a notebook sitting next to your code. Where the code starts fresh every time, but it can read and write to the notebook to remember what happened before.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  The "break it on purpose" testing habit is something I want to keep using. After writing a test for a bug fix, I will temporarily undo the fix to make sure the test actually fails. But if it does not fail, the test is useless. This takes only a few seconds but gives real confidence that the test is doing its job. It also helps catch cases where tests look correct on the surface but are actually testing local variables instead of the real code.

- What is one thing you would do differently next time you work with AI on a coding task?

  I would review AI-generated test cases more carefully before accepting them. In this project, the first set of tests Claude wrote looked reasonable at a glance, but they were not actually connected to the source code they were supposed to verify. Next time, I would ask myself: "If I undo the fix, would this test still pass?" before moving on. Treating AI output as a first draft that needs human review, rather than a finished product, saves time in the long run.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  This project showed me that AI-generated code can be helpful and fast, but it is not automatically correct. You still have to verify it just like you would verify code from any other teammate. The AI is great at scanning a large codebase and spotting patterns quickly, but the human still needs to check the logic and make sure the output actually solves the right problem.
