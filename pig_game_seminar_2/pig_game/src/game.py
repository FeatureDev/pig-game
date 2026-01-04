"""Core game logic for Pig Game."""

from typing import Optional
from src.player import Player
from src.dice import Dice
from src.highscore import HighScore
import sys
import os

# Only active during pytest runs
RUNNING_UNDER_PYTEST = (
    "pytest" in " ".join(sys.argv)
    or any("PYTEST_CURRENT_TEST" in k for k in os.environ)
)

def cprint(msg: str):
    """Print messages only during pytest (for debug visibility)."""
    if RUNNING_UNDER_PYTEST:
        print(msg)


class Game:
    """Handles the rules and flow of the Pig dice game."""

    def __init__(self, name1: str, name2: str, winning_score: int = 100):
        """Initialize the game with two players and a dice."""
        self.player1 = Player(name1)
        self.player2 = Player(name2)
        self.players = [self.player1, self.player2]

        self.dice = Dice()
        self.highscore = HighScore()

        self.current_player = self.player1
        self.current_turn_score = 0
        self.winning_score = winning_score
        self.winner: Optional[Player] = None

        # Koppling till fusksystemet om det finns
        try:
            from src.cheat import Cheat
            self.cheat = Cheat(self)
        except Exception:
            self.cheat = None

        # ensure players exist in highscore
        for p in self.players:
            self.highscore.register_player(p.name)

    # -----------------------------------------------------------
    # Game flow methods
    # -----------------------------------------------------------

    def roll(self):
        """Roll the dice and update the score, returning the rolled value."""
        if self.winner:
            raise RuntimeError("Game already finished!")

        result = self.dice.roll()
        print(f"🎲 {self.current_player.name} rolled a {result}")

        if result == 1:
            self.current_turn_score = 0
            print(f"💥 {self.current_player.name} lost the turn (rolled a 1)!")
            self._switch_turn()
        else:
            self.current_turn_score += result
            print(f"📈 Turn total for {self.current_player.name}: {self.current_turn_score}")

        # check win condition
        if self.current_player.score + self.current_turn_score >= self.winning_score:
            self._declare_winner(self.current_player)

        return result

    def hold(self):
        """Hold current score and switch player."""
        if self.winner:
            raise RuntimeError("Game already finished!")

        self.current_player.score += self.current_turn_score
        print(f"🧮 {self.current_player.name} holds with {self.current_player.score} points.")
        self.current_turn_score = 0

        if self.current_player.score >= self.winning_score:
            self._declare_winner(self.current_player)
        else:
            self._switch_turn()

    def restart(self):
        """Restart the game."""
        for p in self.players:
            p.score = 0
        self.current_player = self.player1
        self.current_turn_score = 0
        self.winner = None
        print("🔄 Game restarted!")

    # -----------------------------------------------------------
    # Helper methods
    # -----------------------------------------------------------

    def _switch_turn(self):
        """Switch active player."""
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )
        print(f"🎯 It's now {self.current_player.name}'s turn!")

    def _declare_winner(self, player: Player):
        """Set winner and record in highscore."""
        player.score += self.current_turn_score
        self.winner = player

        loser = self.player1 if player == self.player2 else self.player2

        # Update highscores
        self.highscore.update_score(player.name, True, player.score)
        self.highscore.update_score(loser.name, False, loser.score)

        print(f"🏆 {player.name} wins with {player.score} points!")
        self.current_turn_score = 0

    def display_score(self):
        """Display scores (used by CLI)."""
        print(
            f"📊 {self.player1.name}: {self.player1.score} | "
            f"{self.player2.name}: {self.player2.score} | "
            f"Current: {self.current_player.name} ({self.current_turn_score})"
        )

    def reset_turn(self):
        """Reset only the temporary turn score."""
        self.current_turn_score = 0
        print("♻️  Turn score reset.")

    def is_over(self) -> bool:
        """Return True if the game has a winner."""
        return self.winner is not None

    def update_highscore(self):
        """Update highscores manually (for tests)."""
        if not self.winner:
            return

        # Först förloraren
        for p in self.players:
            if p != self.winner:
                if hasattr(self.highscore, "add_player"):
                    self.highscore.add_player(p.name)
                else:
                    self.highscore.register_player(p.name)
                self.highscore.update_score(p.name, False, p.score)

        # Sedan vinnaren (testet kontrollerar detta anrop)
        if hasattr(self.highscore, "add_player"):
            self.highscore.add_player(self.winner.name)
        else:
            self.highscore.register_player(self.winner.name)
        self.highscore.update_score(self.winner.name, True, self.winner.score)

