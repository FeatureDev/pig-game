"""Cheat system for the Pig Dice Game."""

import os
import sys
try:
    from src.highscore import HighScore
except ModuleNotFoundError:
    from highscore import HighScore


RUNNING_UNDER_PYTEST = (
    "pytest" in " ".join(sys.argv)
    or any("PYTEST_CURRENT_TEST" in k for k in os.environ)
)


def cprint(msg: str):
    if RUNNING_UNDER_PYTEST:
        print(msg)


class Cheat:
    """Provides controlled manipulation of the game state for testing or debugging."""

    def __init__(self, game):
        if game is None or not hasattr(game, "players") or not hasattr(game, "winning_score"):
            raise TypeError("Cheat must be initialized with a valid Game instance.")
        self.game = game
        self.highscore = HighScore()
        cprint("Cheat system initialized.")

        # 🔗 Koppla fusksystemet direkt till spelet
        if not hasattr(game, "cheat"):
            game.cheat = self

    # -----------------------------------------------------------
    # Cheat operations
    # -----------------------------------------------------------

    def add_points(self, player_name: str, points: int):
        """Add points directly to a player's score."""
        player = self._get_player(player_name)
        if player:
            player.score += points
            print(f"💰 {player_name} gained {points} cheat points! (total: {player.score})")
        else:
            print(f"⚠️  Player '{player_name}' not found!")

    def reset_score(self, player_name: str):
        """Reset a player's score to 0."""
        player = self._get_player(player_name)
        if player:
            player.score = 0
            print(f"🔄 {player_name}'s score reset to 0.")
        else:
            print(f"⚠️  Cannot reset; player '{player_name}' not found.")

    def auto_win(self, player_name: str):
        """Force a player to instantly win the game."""
        player = self._get_player(player_name)
        if player:
            player.score = self.game.winning_score
            # Uppdatera highscore
            if hasattr(self.highscore, "save_score"):
                self.highscore.save_score(player.name, player.score)
            else:
                self.highscore.update_score(player.name, True, player.score)
            self.game.winner = player
            print(f"🏆 {player_name} was forced to win the game!")
        else:
            print(f"⚠️  Cannot auto-win; player '{player_name}' not found.")

    def set_dice_value(self, value: int):
        """Force all dice to a given value."""
        if hasattr(self.game, "dice_hand") and hasattr(self.game.dice_hand, "dice_list"):
            for dice in self.game.dice_hand.dice_list:
                dice.value = value
            print(f"🎲 All dice set to {value}.")
        else:
            print("⚠️ Game has no dice_hand attribute!")


    # -----------------------------------------------------------
    # Utilities
    # -----------------------------------------------------------

    def _get_player(self, name: str):
        for player in getattr(self.game, "players", []):
            if player.name == name:
                return player
        return None

    def debug_reset(self):
        """Clear all highscores and game records (debug use only)."""
        try:
            self.highscore.data = {"players": {}, "games": {}}
            self.highscore.save()
            print("🧹 Highscore data reset.")
            return True
        except Exception:
            print("⚠️  Failed to reset highscore.")
            return False

    def __eq__(self, other):
        """Equality based on instance identity, not shared game."""
        return self is other
