"""Full coverage tests for src.highscore (100% coverage)."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from src.highscore import HighScore
import builtins
import tempfile


# ---------------------------------------------------------------------------
# Initialization & I/O
# ---------------------------------------------------------------------------

def test_initialization_creates_file(tmp_path):
    file_path = tmp_path / "scores.json"
    hs = HighScore(file_path)
    assert file_path.exists()
    assert "players" in hs.data and "games" in hs.data


def test_initialization_loads_existing(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text(json.dumps({"players": {}, "games": {}}))
    hs = HighScore(file_path)
    assert isinstance(hs.data, dict)


def test_initialization_invalid_data_resets(tmp_path):
    file_path = tmp_path / "scores.json"
    file_path.write_text("invalid json!!")
    hs = HighScore(file_path)
    assert hs.data == {"players": {}, "games": {}}


def test_load_handles_corrupt_file(tmp_path):
    file_path = tmp_path / "broken.json"
    file_path.write_text("corrupt")
    hs = HighScore(file_path)
    with patch("builtins.open", side_effect=OSError("fail")):
        hs.load()
    assert "players" in hs.data


def test_save_handles_ioerror(monkeypatch, tmp_path):
    file_path = tmp_path / "hs.json"
    hs = HighScore(file_path)

    def fail(*a, **kw):
        raise OSError("fail")

    monkeypatch.setattr("builtins.open", fail)
    hs.save()  # should not crash


# ---------------------------------------------------------------------------
# Player management
# ---------------------------------------------------------------------------

def test_register_player_adds_new(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    hs.register_player("Alice")
    assert "Alice" in hs.data["players"]


def test_register_player_existing_does_not_duplicate(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    hs.data["players"]["Bob"] = {"name": "Bob"}
    hs.register_player("Bob")
    assert len(hs.data["players"]) == 1


def test_update_score_updates_wins_and_avg(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    hs.update_score("Alice", True, 50)
    hs.update_score("Alice", False, 30)
    rec = hs.data["players"]["Alice"]
    assert rec["games_played"] == 2
    assert rec["wins"] == 1
    assert rec["losses"] == 1
    assert 0 <= rec["avg_points"] <= 50


def test_save_score_alias_calls_update_score(tmp_path):
    file_path = tmp_path / "f.json"
    hs = HighScore(file_path)
    hs.save_score("Zelda", 42)
    assert "Zelda" in hs.data["players"]


def test_change_name_success_and_persists(tmp_path):
    file_path = tmp_path / "f.json"
    hs = HighScore(file_path)
    hs.register_player("Old")
    hs.save_game("Old_vs_Bob", {
        "player1": "Old",
        "player2": "Bob",
        "winner": "Old",
    })

    hs.change_name("Old", "New")

    # confirm memory update
    assert "New" in hs.data["players"]
    assert "Old" not in hs.data["players"]

    # confirm game data updated
    game = list(hs.data["games"].values())[0]
    assert "New" in game.values()

    # confirm persisted to file
    data = json.loads(file_path.read_text())
    assert "New" in data["players"]


def test_change_name_ignores_invalid(tmp_path):
    file_path = tmp_path / "f.json"
    hs = HighScore(file_path)
    hs.change_name("Missing", "New")
    hs.change_name("Missing", "")
    assert "players" in hs.data  # no crash


# ---------------------------------------------------------------------------
# Game management
# ---------------------------------------------------------------------------

def test_save_and_load_game(tmp_path):
    file_path = tmp_path / "save.json"
    hs = HighScore(file_path)
    key = "A_vs_B"
    info = {"player1": "A", "player2": "B", "score1": 10, "score2": 20}
    hs.save_game(key, info)
    loaded = hs.load_game(key)
    assert loaded == info


def test_get_all_games_returns_dict(tmp_path):
    file_path = tmp_path / "g.json"
    hs = HighScore(file_path)
    hs.save_game("match1", {"player1": "A"})
    games = hs.get_all_games()
    assert "match1" in games


def test_get_top_players_sorted(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    hs.register_player("A")
    hs.register_player("B")
    hs.data["players"]["A"]["wins"] = 3
    hs.data["players"]["B"]["wins"] = 1
    top = hs.get_top_players()
    assert list(top.keys())[0] == "A"


def test_get_top_players_empty(tmp_path):
    file_path = tmp_path / "t.json"
    hs = HighScore(file_path)
    hs.data["players"] = {}
    hs.save()
    assert hs.get_top_players() == {}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def test_reset_all_clears_data(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    hs.data["players"]["X"] = {"wins": 5}
    hs.data["games"]["A_vs_B"] = {}
    hs.reset_all()
    assert not hs.data["players"] and not hs.data["games"]


def test_repr_displays_counts(tmp_path):
    file_path = tmp_path / "h.json"
    hs = HighScore(file_path)
    text = repr(hs)
    assert "HighScore" in text

from src.highscore import HighScore
import json, tempfile
from pathlib import Path

def test_load_invalid_file_resets_data(tmp_path):
    """Invalid JSON file should reset to defaults."""
    badfile = tmp_path / "bad.json"
    badfile.write_text("not json")
    hs = HighScore(badfile)
    assert hs.data == {"players": {}, "games": {}}


def test_change_name_missing_player(tmp_path):
    """change_name should handle non-existent player gracefully."""
    hs = HighScore(tmp_path / "test.json")
    hs.change_name("ghost", "newname")  # no error expected
    assert isinstance(hs.data, dict)


def test_save_game_and_load(tmp_path):
    """save_game and load_game should persist correctly."""
    hs = HighScore(tmp_path / "data.json")
    key = "Alice_vs_Bob"
    hs.save_game(key, {"player1": "A", "player2": "B"})
    loaded = hs.load_game(key)
    assert loaded["player1"] == "A"

def test_save_handles_exception(monkeypatch, tmp_path):
    """Force save() to raise exception and ensure it fails silently."""
    hs = HighScore(tmp_path / "dummy.json")

    def bad_open(*_, **__):
        raise OSError("disk full")

    monkeypatch.setattr(builtins, "open", bad_open)
    # Should not raise any error
    hs.save()


def test_load_handles_invalid_json(tmp_path):
    """Invalid JSON should reset data to defaults."""
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json}")
    hs = HighScore(bad)
    assert "players" in hs.data and "games" in hs.data


def test_reset_all_creates_fresh_data(tmp_path):
    """Ensure reset_all clears all previous data."""
    hs = HighScore(tmp_path / "reset.json")
    hs.data["players"]["Bob"] = {"wins": 5}
    hs.reset_all()
    assert hs.data == {"players": {}, "games": {}}

def test_load_file_structure_invalid(tmp_path):
    """If JSON structure is wrong, HighScore resets data."""
    badfile = tmp_path / "weird.json"
    badfile.write_text(json.dumps({"invalid": "structure"}))
    hs = HighScore(badfile)
    # Should reset because "players"/"games" missing
    assert "players" in hs.data and "games" in hs.data


def test_repr_and_save_failure(monkeypatch, tmp_path):
    """Force save() to fail and ensure repr() still works."""
    hs = HighScore(tmp_path / "repr.json")
    hs.data["players"]["A"] = {"wins": 1}
    hs_str = repr(hs)
    assert "<HighScore" in hs_str

    def bad_open(*_, **__): raise IOError("disk error")
    monkeypatch.setattr("builtins.open", bad_open)
    hs.save()  # should fail silently
