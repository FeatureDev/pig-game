"""HighScore tracking and persistence for Pig Game."""
import json
from pathlib import Path


class HighScore:
    """Manage highscores and saved games stored in a JSON file."""

    filepath: Path | None = None  # class-level override for tests/monkeypatch

    def __init__(self, filepath: str | Path | None = None):
        if filepath is not None:
            self.filepath = Path(filepath)
        elif not self.filepath:
            self.filepath = Path("highscore.json")

        # Initialize or load file
        if not self.filepath.exists():
            self.data = {"players": {}, "games": {}}
            self.save()
        else:
            self.load()

    # ------------------------------------------------------------------
    # Core file I/O
    # ------------------------------------------------------------------
    def save(self):
        """Save current data to JSON file (fails silently on I/O errors)."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            # fail silently for tests / restricted environments
            pass

    def load(self):
        """Load JSON file or reinitialize if invalid."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty file")
                self.data = json.loads(content)
            if not isinstance(self.data, dict) or "players" not in self.data or "games" not in self.data:
                raise ValueError("Invalid data structure")
        except Exception:
            self.data = {"players": {}, "games": {}}
            self.save()

    # ------------------------------------------------------------------
    # Player management
    # ------------------------------------------------------------------
    def register_player(self, name: str):
        """Register a player if not already in highscore data."""
        if not name:
            return
        if "players" not in self.data:
            self.data["players"] = {}
        if name not in self.data["players"]:
            self.data["players"][name] = {
                "name": name,
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "avg_points": 0.0,
            }
            self.save()

    def add_player(self, name: str):
        """Alias kept for backward compatibility with older tests."""
        self.register_player(name)

    def update_score(self, name: str, won: bool, points: int):
        """Update a player's statistics (wins/losses and avg points)."""
        self.register_player(name)
        rec = self.data["players"][name]
        rec["games_played"] += 1
        rec["wins" if won else "losses"] += 1
        rec["avg_points"] = round(
            ((rec["avg_points"] * (rec["games_played"] - 1)) + points)
            / rec["games_played"],
            2,
        )
        self.save()

    def save_score(self, name: str, score: int):
        """Legacy alias (used by Cheat) to save a winning score."""
        self.update_score(name, True, score)

    def change_name(self, old: str, new: str):
        """Rename player across players and game records."""
        if not old or not new or old == new:
            return
        if "players" not in self.data:
            self.data["players"] = {}
        if old not in self.data["players"]:
            return

        # Move player record
        player_data = self.data["players"].pop(old)
        player_data["name"] = new
        self.data["players"][new] = player_data

        # Update all games referencing old name
        updated_games = {}
        for key, game in list(self.data.get("games", {}).items()):
            new_key = key.replace(old, new) if old in key else key
            if game.get("player1") == old:
                game["player1"] = new
            if game.get("player2") == old:
                game["player2"] = new
            if game.get("winner") == old:
                game["winner"] = new
            updated_games[new_key] = game

        self.data["games"] = updated_games
        self.save()

    # ------------------------------------------------------------------
    # Game management
    # ------------------------------------------------------------------
    def save_game(self, key: str, info: dict):
        """Save a game state (used by CLI pause/continue)."""
        if "games" not in self.data:
            self.data["games"] = {}
        self.data["games"][key] = info
        self.save()

    def load_game(self, key: str):
        """Retrieve a saved game by key."""
        return self.data.get("games", {}).get(key)

    def get_all_games(self):
        """Return all saved games."""
        return self.data.get("games", {})

    def get_top_players(self, limit: int | None = None):
        """Return sorted dict of players by wins and avg points."""
        players = self.data.get("players", {})
        if not players:
            return {}

        sorted_players = sorted(
            players.items(),
            key=lambda kv: (kv[1]["wins"], kv[1]["avg_points"]),
            reverse=True,
        )
        if limit:
            sorted_players = sorted_players[:limit]
        return dict(sorted_players)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def reset_all(self):
        """Completely reset the highscore data."""
        self.data = {"players": {}, "games": {}}
        self.save()

    def __repr__(self):
        return (
            f"<HighScore players={len(self.data.get('players', {}))}, "
            f"games={len(self.data.get('games', {}))}>"
        )
