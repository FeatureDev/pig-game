"""Unit tests for src/game.py (Game class and logic)."""
import pytest
from unittest.mock import MagicMock, patch
from src.game import Game, cprint


def test_game_initialization_creates_players_and_dice():
    """Game initializes with two players and a dice."""
    game = Game("Alice", "Bob")
    assert isinstance(game, Game)
    assert len(game.players) == 2
    assert hasattr(game, "dice")
    assert game.players[0].name == "Alice"
    assert game.players[1].name == "Bob"


def test_roll_adds_to_current_score(monkeypatch):
    """Rolling a number > 1 should add to temporary score."""
    game = Game("A", "B")
    monkeypatch.setattr("src.dice.random.randint", lambda a, b: 4)
    prev_score = game.current_turn_score
    game.roll()
    assert game.current_turn_score == prev_score + 4


def test_roll_one_switches_turn(monkeypatch):
    """Rolling a 1 resets temp score and switches player."""
    game = Game("A", "B")
    monkeypatch.setattr("src.dice.random.randint", lambda a, b: 1)
    game.current_player = game.players[0]
    game.roll()
    assert game.current_turn_score == 0
    assert game.current_player == game.players[1]


def test_hold_adds_score_and_switches_player():
    """Holding should add current score to total and change turn."""
    game = Game("A", "B")
    game.current_turn_score = 12
    current_player = game.current_player
    game.hold()
    assert current_player.score == 12
    assert game.current_player != current_player


def test_win_condition_sets_winner():
    """A player reaching 100 or more wins the game."""
    game = Game("A", "B")
    game.current_turn_score = 100
    current_player = game.current_player
    game.hold()
    assert game.winner == current_player
    assert game.is_over()


def test_restart_resets_state():
    """restart() should reset all scores and game state."""
    game = Game("A", "B")
    game.players[0].score = 50
    game.current_turn_score = 12
    game.restart()
    assert all(p.score == 0 for p in game.players)
    assert game.current_turn_score == 0
    assert game.winner is None


def test_cprint_only_outputs_in_pytest_context(capsys):
    """cprint() should print only when RUNNING_UNDER_PYTEST is True."""
    cprint("Hello, pytest!")
    captured = capsys.readouterr()
    assert "Hello" in captured.out


def test_add_highscore_entry(monkeypatch, tmp_path):
    """After a win, player should be added to highscore."""
    hs_file = tmp_path / "score.json"
    monkeypatch.setattr("src.highscore.HighScore.filepath", hs_file)
    game = Game("X", "Y")
    game.highscore = MagicMock()
    game.winner = game.players[0]
    game.update_highscore()
    game.highscore.add_player.assert_called_with(game.winner.name)
    game.highscore.update_score.assert_called()


def test_invalid_player_roll_raises():
    """roll() should raise if called after game over."""
    game = Game("A", "B")
    game.winner = game.players[0]
    with pytest.raises(RuntimeError):
        game.roll()


def test_reset_turn_score_does_not_affect_total():
    """Resetting turn should not change player's total score."""
    game = Game("A", "B")
    current_player = game.current_player
    current_player.score = 40
    game.current_turn_score = 10
    game.reset_turn()
    assert game.current_turn_score == 0
    assert current_player.score == 40
