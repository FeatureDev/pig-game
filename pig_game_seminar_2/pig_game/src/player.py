"""Player logic for the Pig Dice Game."""

import sys

# Detect if running under pytest (for conditional printing)
RUNNING_UNDER_PYTEST = any("pytest" in arg for arg in sys.argv)


def cprint(msg: str):
    """Print messages only during pytest runs for coverage tracing."""
    if RUNNING_UNDER_PYTEST:
        print(msg)


class Player:
    """Represents a single Pig game player."""

    def __init__(self, name: str):
        """Initialize a player with a validated name and starting score 0."""
        if not isinstance(name, str):
            raise TypeError("Player name must be a string.")
        if not name.strip():
            raise ValueError("Player name cannot be empty.")
        self.name = name.strip()
        self.score = 0
        cprint(f"[Coverage] Player created: {self.name}")

    # ------------------------------------------------------------------
    # Score management
    # ------------------------------------------------------------------

    def add_score(self, points: int):
        """Add points to the player's total score.

        Raises:
            ValueError: if `points` is negative.
        """
        if not isinstance(points, int):
            raise TypeError("Points must be an integer.")
        if points < 0:
            cprint(f"[Coverage] Ignored invalid score addition ({points}) for {self.name}.")
            raise ValueError("Score addition cannot be negative.")
        self.score += points
        cprint(f"[Coverage] {self.name} gained {points} points (total={self.score}).")

    def reset_score(self):
        """Reset the player's score to 0."""
        self.score = 0
        cprint(f"[Coverage] {self.name} score reset.")

    # ------------------------------------------------------------------
    # Name management
    # ------------------------------------------------------------------

    def rename(self, new_name: str):
        """Change the player's name safely."""
        if not isinstance(new_name, str):
            raise TypeError("New name must be a string.")
        if not new_name.strip():
            cprint("[Coverage] Rename attempt ignored — empty name.")
            raise ValueError("Name cannot be empty.")
        old = self.name
        self.name = new_name.strip()
        cprint(f"[Coverage] Player renamed from {old} to {self.name}.")

    # ------------------------------------------------------------------
    # Equality and representation
    # ------------------------------------------------------------------

    def __eq__(self, other):
        """Check equality based on name and score."""
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.score == other.score

    def __repr__(self):
        """Detailed representation for debugging."""
        return f"Player(name={self.name}, score={self.score})"

    def __str__(self):
        """Human-readable player representation."""
        return f"{self.name} ({self.score}p)"

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    def clone(self):
        """Return a new Player instance with the same name and score.

        Used in tests or to duplicate player state without references.
        """
        new_player = Player(self.name)
        new_player.score = self.score
        cprint(f"[Coverage] Cloned player {self.name} with score {self.score}.")
        return new_player
