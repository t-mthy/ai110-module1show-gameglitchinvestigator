import ast
import os
from logic_utils import check_guess

# --- Tests for Bug Fix: Attempt counter initialization ---
# These tests parse the actual app.py source to verify the attempt counter
# is initialized to 0. If someone reverts the fix, these tests will FAIL.

APP_PATH = os.path.join(os.path.dirname(__file__), "..", "app.py")


def _get_attempts_init_value():
    """Parse app.py's AST and extract the value assigned to
    st.session_state.attempts in the initialization block."""
    with open(APP_PATH) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        # Look for: st.session_state.attempts = <value>
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Attribute)
            and node.targets[0].attr == "attempts"
            and isinstance(node.value, ast.Constant)
        ):
            return node.value.value
    raise RuntimeError("Could not find attempts initialization in app.py")


def test_attempts_initialized_to_zero():
    """Verify app.py initializes the attempt counter to 0, not 1."""
    init_value = _get_attempts_init_value()
    assert init_value == 0, (
        f"app.py initializes attempts to {init_value}, expected 0"
    )


def test_attempts_left_matches_limit():
    """With the real init value from app.py, attempts-left should equal the
    full limit before any guess is made."""
    attempt_limit = 8  # Normal difficulty
    init_value = _get_attempts_init_value()

    attempts_left = attempt_limit - init_value
    assert attempts_left == attempt_limit, (
        f"Before any guess, attempts left ({attempts_left}) should equal "
        f"the limit ({attempt_limit}), but attempts starts at {init_value}"
    )


def test_attempts_left_decreases_after_guess():
    """After one guess, attempts left should be limit - 1."""
    attempt_limit = 8
    attempts = _get_attempts_init_value()

    # Simulate one guess
    attempts += 1

    assert attempt_limit - attempts == 7, (
        "After one guess, attempts left should be 7 for Normal difficulty"
    )

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
