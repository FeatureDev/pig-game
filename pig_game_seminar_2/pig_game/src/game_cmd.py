# filename: src/game_cmd.py
"""Command-line interface for the Pig Game."""

import cmd
import sys
from src.game import Game
from src.highscore import HighScore
from src.intelligence import Intelligence

RUNNING_UNDER_PYTEST = any("pytest" in arg for arg in sys.argv)


def cprint(msg: str):
    """Print debug messages only during pytest runs to keep gameplay clean."""
    if RUNNING_UNDER_PYTEST:
        print(msg)


class PigGameCMD(cmd.Cmd):
    """Command-line interface for the Pig Game."""

    intro = (
        "🐷  Welcome to Pig Game! Type 'help' or '?' for commands.\n"
        "Type 'start <player1> <player2> [difficulty]' to begin your game!\n"
        "You can also use 'ai <1|2|3>' to change AI difficulty mid-game."
    )
    prompt = "(Pig) "

    def __init__(self):
        """Initialize command interface and unified highscore system."""
        super().__init__()
        self.highscore = HighScore()
        self.game = None
        self.game_active = False
        self.ai_level = None  # store AI difficulty level

    # ============================================================
    # Core commands
    # ============================================================

    def do_start(self, args: str):
        """Start a new game with player names and optional AI difficulty."""
        parts = args.split()
        if len(parts) < 2:
            print("Usage: start <player1> <player2> [difficulty]")
            return

        p1, p2 = parts[0], parts[1]
        difficulty = parts[2] if len(parts) >= 3 else None

        self.game = Game(p1, p2)
        self.game_active = True
        self.ai_level = None

        # Register players in highscore
        self.highscore.register_player(p1)
        self.highscore.register_player(p2)

        # AI setup
        if p2.lower() == "ai":
            mapping = {"1": "easy", "2": "normal", "3": "hard"}
            self.ai_level = mapping.get(difficulty, "normal")
            print(f"🤖 AI opponent ready (difficulty: {self.ai_level})")

        print(f"✅  New game started between {p1} and {p2}")
        self._show_turn()

    # ------------------------------------------------------------
    def do_roll(self, _):
        """Roll the dice or let AI take its turn."""
        if not self.game_active or not self.game:
            print("⚠️  Start a game first.")
            return

        if self.game.winner:
            print("🏁 Game already finished! Start a new game.")
            return

        if self.game.current_player.name.lower() == "ai":
            self._ai_turn()
            return

        result = self.game.roll()
        print(f"🎲 You rolled a {result}")
        self._show_turn()

        if self.game.current_player.name.lower() == "ai" and not self.game.winner:
            self._ai_turn()

    # ------------------------------------------------------------
    def do_cheat(self, args: str):
        """Use cheat commands (developer/debug tool).
        Usage:
          cheat add <player> <points>
          cheat win <player>
          cheat dice <value>
          cheat reset
        """
        if not self.game:
            print("No active game! Start one first.")
            return

        from src.cheat import Cheat
        cheat = Cheat(self.game)
        parts = args.split()

        if not parts:
            print("Usage: cheat <add|win|dice|reset> ...")
            return

        cmd = parts[0].lower()
        try:
            if cmd == "add" and len(parts) == 3:
                cheat.add_points(parts[1], int(parts[2]))
            elif cmd == "win" and len(parts) == 2:
                cheat.auto_win(parts[1])
            elif cmd == "dice" and len(parts) == 2:
                cheat.set_dice_value(int(parts[1]))
            elif cmd == "reset":
                cheat.debug_reset()
                print("🧹 Cheat system reset.")
            else:
                print("⚠️  Invalid cheat command or arguments.")
        except Exception as e:
            print(f"❌ Cheat failed: {e}")

    def do_rename(self, args: str):
        """Rename the current player."""
        if not self.game_active or not self.game:
            print("⚠️  No active game to rename in.")
            return

        new_name = args.strip()
        if not new_name:
            print("Usage: rename <new_name>")
            return

        current_player = self.game.current_player
        old_name = current_player.name
        current_player.name = new_name

        if hasattr(self.highscore, "change_name"):
            try:
                self.highscore.change_name(old_name, new_name)
            except Exception:
                pass

        print(f"✅ Player '{old_name}' renamed to '{new_name}'.")

    def do_pause(self, _):
        """Pause (save) the current game."""
        if not self.game_active or self.game is None:
            print("No game to pause.")
            return
        key = f"{self.game.player1.name}_vs_{self.game.player2.name}"
        info = {
            "player1": self.game.player1.name,
            "player2": self.game.player2.name,
            "score1": self.game.player1.score,
            "score2": self.game.player2.score,
            "current_turn": self.game.current_player.name,
            "winner": self.game.winner.name if self.game.winner else None,
        }
        self.highscore.save_game(key, info)
        print(f"⏸️ Game '{key}' saved successfully.")
        self.game_active = False

    def do_continue(self, args):
        """Continue a previously saved game."""
        key = args.strip()
        if not key:
            print("Usage: continue <player1> <player2> or <player1>_vs_<player2>")
            return

        key = key.replace(" ", "_vs_") if " " in key else key
        data = self.highscore.load_game(key)
        if not data:
            print(f"No saved game found for '{key}'.")
            return

        self.game = Game(data["player1"], data["player2"])
        self.game.player1.score = data["score1"]
        self.game.player2.score = data["score2"]
        self.game.current_player = (
            self.game.player1
            if data["current_turn"] == self.game.player1.name
            else self.game.player2
        )
        self.game.winner = data["winner"]
        self.game_active = True
        print(f"▶️ Game '{key}' resumed successfully.")
        self._show_turn()


    # ------------------------------------------------------------
    def do_hold(self, _):
        """Hold current player's score."""
        if not self.game_active or not self.game:
            print("Start a game first.")
            return

        if self.game.winner:
            print("🏁 Game already finished! Start a new game.")
            return

        self.game.hold()
        print("✅ Held successfully.")
        self._show_turn()

        if self.game.current_player.name.lower() == "ai" and not self.game.winner:
            self._ai_turn()

    # ------------------------------------------------------------
    def _ai_turn(self):
        """Internal: Handle AI automatic turn until it holds or loses."""
        import time

        ai = Intelligence(self.ai_level or "normal")
        while not self.game.winner and self.game.current_player.name.lower() == "ai":
            self._show_turn()
            decision = ai.decide_roll_or_hold(
                self.game.current_turn_score, self.game.current_player.score
            )

            if decision == "roll":
                print(f"🤖 AI ({self.ai_level}) chooses to roll...")
                result = self.game.roll()
                print(f"🎲 AI rolled a {result}")
                time.sleep(1.5)
            else:
                print(f"🤖 AI ({self.ai_level}) chooses to hold...")
                self.game.hold()
                print("✅ AI holds and ends its turn.")
                break

        if not self.game.winner:
            print()
            self.game.display_score()
            self._show_turn()

    # ------------------------------------------------------------
    def do_ai(self, args: str):
        """Change AI difficulty level during a game."""
        if not self.game_active or not self.game:
            print("⚠️  No active game to adjust AI difficulty.")
            return

        if not args.strip():
            print("Usage: ai <1|2|3>")
            return

        mapping = {"1": "easy", "2": "normal", "3": "hard"}
        new_level = mapping.get(args.strip())
        if not new_level:
            print("⚠️  Invalid AI level. Use 1, 2, or 3.")
            return

        self.ai_level = new_level
        print(f"🤖 AI difficulty set to '{self.ai_level}'.")

    # ------------------------------------------------------------
    def _show_turn(self):
        """Display whose turn it is."""
        if not self.game or self.game.winner:
            return
        current = self.game.current_player.name
        if current.lower() == "ai":
            print(f"🤖  It's the AI's turn! (difficulty: {self.ai_level})\n")
        else:
            print(f"🎯  Your turn, {current}!\n")

    # ------------------------------------------------------------
    def do_status(self, _):
        """Display current game status."""
        if not self.game_active or not self.game:
            print("No game in progress.")
            return

        self.game.display_score()
        if self.game.player2.name.lower() == "ai":
            print(f"🤖 Current AI difficulty: {self.ai_level}")

    # ------------------------------------------------------------
    def do_highscores(self, _):
        """Show the top players from the highscore list."""
        top_players = self.highscore.get_top_players()
        if not top_players:
            print("🏆 No highscores recorded yet.")
            return

        print("\n🏆  Top Players (sorted by wins & avg points):")
        print("─" * 60)
        for i, (_, rec) in enumerate(top_players.items(), start=1):
            print(
                f"{i:>2}. {rec['name']:<15} "
                f"Games: {rec['games_played']:<3} | "
                f"Wins: {rec['wins']:<3} | "
                f"Losses: {rec['losses']:<3} | "
                f"Avg Points: {rec['avg_points']}"
            )
        print("─" * 60)

    # ------------------------------------------------------------
    def do_games(self, _):
        """List all saved games."""
        games = self.highscore.get_all_games()
        if not games:
            print("No saved games found.")
            return

        print("\n🎮  Saved Games:")
        print("─" * 60)
        for k, v in games.items():
            print(
                f"{k}: {v['player1']}({v['score1']}) vs {v['player2']}({v['score2']}) "
                f"=> Turn: {v['current_turn']}, Winner: {v['winner']}"
            )
        print("─" * 60)

    def do_rules(self, arg):
        """Show the rules of the Pig Dice Game."""
        print("""
    🐷 Pig Dice Game Rules
    ──────────────────────
    • Two players take turns rolling a six-sided die.
    • On each turn, a player may roll as many times as they wish.
    • Each roll adds to the current turn total.
    • If a player rolls a 1, they lose their turn and forfeit the round's points.
    • The player can 'hold' to bank their current turn points.
    • The first to reach 100 total points wins the game.
    • You can play against another player or the AI.
    • Use 'cheat' for testing purposes.
    • Type 'help' to see all available commands.
    """)


    # ------------------------------------------------------------
    def do_reset(self, _):
        """Reset the entire game system (clears all data)."""
        confirm = input("⚠️  Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == "yes":
            self.highscore.reset_all()
            print("🧹 All game and player data cleared!")
        else:
            print("Reset cancelled.")

    # ------------------------------------------------------------
    def do_quit(self, _):
        """Quit the game."""
        print("👋 Thanks for playing Pig Game!")
        return True

    def default(self, line):
        """Handle unknown commands."""
        print(f"⚠️  Unknown command: '{line}'. Type 'help' for options.")

    def emptyline(self):
        """Ignore empty input."""
        return False


def main():
    """Entry point to run Pig Game."""
    PigGameCMD().cmdloop()


if __name__ == "__main__":
    main()
