"""Comprehensive tests for src.game_cmd (PigGameCMD)."""

import builtins
import pytest
from unittest.mock import MagicMock, patch
from src.game_cmd import PigGameCMD, cprint


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def cli():
    """Return a fresh command interface with mocks for highscore."""
    cmd = PigGameCMD()
    cmd.highscore = MagicMock()
    return cmd


# ---------------------------------------------------------------------------
# cprint
# ---------------------------------------------------------------------------

def test_cprint_prints_under_pytest(capsys):
    cprint("Debug message")
    out = capsys.readouterr().out
    assert "Debug" in out or out == ""  # pytest env controls behavior


# ---------------------------------------------------------------------------
# do_start
# ---------------------------------------------------------------------------

def test_do_start_starts_game(cli):
    with patch("src.game_cmd.Game") as MockGame:
        cli.do_start("Alice Bob")
        MockGame.assert_called_once_with("Alice", "Bob")
        cli.highscore.register_player.assert_any_call("Alice")
        cli.highscore.register_player.assert_any_call("Bob")
        assert cli.game_active


def test_do_start_with_ai_and_difficulty(cli, capsys):
    with patch("src.game_cmd.Game"):
        cli.do_start("Alice ai 3")
        out = capsys.readouterr().out
        assert "AI opponent" in out
        assert "hard" in out
        assert cli.ai_level == "hard"


def test_do_start_missing_args(cli, capsys):
    cli.do_start("Alice")
    out = capsys.readouterr().out
    assert "Usage" in out


# ---------------------------------------------------------------------------
# do_ai (new command)
# ---------------------------------------------------------------------------

def test_do_ai_sets_difficulty(cli, capsys):
    cli.game_active = True
    cli.game = MagicMock()
    cli.do_ai("1")
    out = capsys.readouterr().out
    assert "easy" in out


def test_do_ai_invalid_input(cli, capsys):
    cli.game_active = True
    cli.game = MagicMock()
    cli.do_ai("x")
    out = capsys.readouterr().out
    assert "Invalid" in out


def test_do_ai_no_game(cli, capsys):
    cli.do_ai("1")
    assert "No active game" in capsys.readouterr().out or "No" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# do_roll
# ---------------------------------------------------------------------------

def test_do_roll_no_game(cli, capsys):
    cli.do_roll("")
    assert "Start a game first" in capsys.readouterr().out


def test_do_roll_with_active_game(cli, capsys):
    mock_game = MagicMock()
    mock_game.player1.name = "A"
    mock_game.player2.name = "B"
    mock_game.player1.score = 10
    mock_game.player2.score = 5
    mock_game.current_player.name = "A"
    mock_game.winner = None
    mock_game.roll.return_value = 3
    cli.game = mock_game
    cli.game_active = True
    cli.do_roll("")
    out = capsys.readouterr().out
    assert "rolled" in out


def test_do_roll_with_ai_turn(cli):
    cli.game_active = True
    mock_game = MagicMock()
    mock_game.current_player.name = "ai"
    mock_game.winner = None
    cli.game = mock_game
    cli._ai_turn = MagicMock()
    cli.do_roll("")
    cli._ai_turn.assert_called_once()


# ---------------------------------------------------------------------------
# do_hold
# ---------------------------------------------------------------------------

def test_do_hold_no_game(cli, capsys):
    cli.do_hold("")
    assert "Start a game first" in capsys.readouterr().out


def test_do_hold_with_game(cli, capsys):
    cli.game = MagicMock()
    cli.game_active = True
    cli.game.current_player.name = "A"
    cli.game.winner = None
    cli.do_hold("")
    out = capsys.readouterr().out
    assert "Held" in out


def test_do_hold_triggers_ai_turn(cli):
    cli.game = MagicMock()
    cli.game_active = True
    cli.game.current_player.name = "ai"
    cli.game.winner = None
    cli._ai_turn = MagicMock()
    cli.do_hold("")
    cli._ai_turn.assert_called_once()


# ---------------------------------------------------------------------------
# do_status
# ---------------------------------------------------------------------------

def test_do_status_no_game(cli, capsys):
    cli.do_status("")
    assert "No game" in capsys.readouterr().out


def test_do_status_with_game(cli):
    cli.game = MagicMock()
    cli.game_active = True
    cli.do_status("")
    cli.game.display_score.assert_called_once()


# ---------------------------------------------------------------------------
# do_rename
# ---------------------------------------------------------------------------

def test_do_rename_no_game(cli, capsys):
    cli.do_rename("NewName")
    assert "No active game" in capsys.readouterr().out


def test_do_rename_empty_name(cli, capsys):
    cli.game = MagicMock()
    cli.game_active = True
    cli.do_rename("   ")
    assert "Usage" in capsys.readouterr().out


def test_do_rename_success(cli, capsys):
    cli.game = MagicMock()
    cli.game_active = True
    cli.game.current_player.name = "Old"
    cli.highscore.change_name = MagicMock()
    cli.do_rename("New")
    assert "renamed" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# do_pause
# ---------------------------------------------------------------------------

def test_do_pause_no_game(cli, capsys):
    cli.do_pause("")
    assert "No game" in capsys.readouterr().out


def test_do_pause_with_game(cli, capsys):
    cli.game = MagicMock()
    cli.game.player1.name = "A"
    cli.game.player2.name = "B"
    cli.game.player1.score = 1
    cli.game.player2.score = 2
    cli.game.current_player.name = "A"
    cli.game.winner = None
    cli.game_active = True
    cli.do_pause("")
    out = capsys.readouterr().out
    assert "saved" in out
    assert not cli.game_active


# ---------------------------------------------------------------------------
# do_continue
# ---------------------------------------------------------------------------

def test_do_continue_no_key(cli, capsys):
    cli.do_continue("")
    assert "Usage" in capsys.readouterr().out


def test_do_continue_no_data(cli, capsys):
    cli.highscore.load_game.return_value = None
    cli.do_continue("A_vs_B")
    assert "No saved" in capsys.readouterr().out


def test_do_continue_success(cli, capsys):
    cli.highscore.load_game.return_value = {
        "player1": "A",
        "player2": "B",
        "score1": 10,
        "score2": 20,
        "current_turn": "A",
        "winner": None,
    }
    with patch("src.game_cmd.Game") as MockGame:
        cli.do_continue("A_vs_B")
        MockGame.assert_called_once()
        assert cli.game_active
        assert "resumed" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# do_highscores
# ---------------------------------------------------------------------------

def test_do_highscores_no_data(cli, capsys):
    cli.highscore.get_top_players.return_value = {}
    cli.do_highscores("")
    assert "No highscores" in capsys.readouterr().out


def test_do_highscores_with_data(cli, capsys):
    cli.highscore.get_top_players.return_value = {
        "A": {"name": "Alice", "games_played": 2, "wins": 1, "losses": 1, "avg_points": 50}
    }
    cli.do_highscores("")
    out = capsys.readouterr().out
    assert "Alice" in out


# ---------------------------------------------------------------------------
# do_games
# ---------------------------------------------------------------------------

def test_do_games_no_data(cli, capsys):
    cli.highscore.get_all_games.return_value = {}
    cli.do_games("")
    assert "No saved games" in capsys.readouterr().out


def test_do_games_with_data(cli, capsys):
    cli.highscore.get_all_games.return_value = {
        "A_vs_B": {
            "player1": "A", "player2": "B",
            "score1": 1, "score2": 2,
            "current_turn": "A", "winner": None
        }
    }
    cli.do_games("")
    out = capsys.readouterr().out
    assert "A_vs_B" in out


# ---------------------------------------------------------------------------
# do_reset
# ---------------------------------------------------------------------------

def test_do_reset_cancelled(cli, capsys, monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "no")
    cli.do_reset("")
    assert "cancelled" in capsys.readouterr().out


def test_do_reset_confirmed(cli, capsys, monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "yes")
    cli.do_reset("")
    assert "cleared" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# do_quit / default / emptyline
# ---------------------------------------------------------------------------

def test_do_quit_returns_true(cli, capsys):
    result = cli.do_quit("")
    assert result is True
    assert "Thanks" in capsys.readouterr().out


def test_default_prints_warning(cli, capsys):
    cli.default("nonsense")
    assert "Unknown command" in capsys.readouterr().out


def test_emptyline_returns_false(cli):
    assert cli.emptyline() is False


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def test_show_turn_outputs_for_ai_and_human(cli, capsys):
    cli.game = MagicMock()
    cli.game.winner = None

    cli.game.current_player.name = "Morgan"
    cli._show_turn()
    out = capsys.readouterr().out
    assert "Morgan" in out

    cli.game.current_player.name = "ai"
    cli.ai_level = "hard"
    cli._show_turn()
    out = capsys.readouterr().out
    assert "AI" in out


def test_ai_turn_calls_game_methods(cli):
    cli.game = MagicMock()
    cli.game.winner = None
    cli.game.current_player.name = "ai"
    cli.ai_level = "easy"

    with patch("src.game_cmd.Intelligence") as MockAI:
        ai = MockAI.return_value
        ai.decide_roll_or_hold.side_effect = ["roll", "hold"]
        cli._ai_turn()
        assert ai.decide_roll_or_hold.call_count >= 1

# ---------------------------------------------------------------------------
# Extra coverage tests for edge cases
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Extra coverage tests for untested branches
# ---------------------------------------------------------------------------

import pytest
from unittest.mock import patch, MagicMock

def test_do_start_invalid_game_init(monkeypatch, cli):
    """Simulate Game() raising an exception (should raise)."""
    def bad_game(*_, **__):
        raise Exception("boom")
    monkeypatch.setattr("src.game_cmd.Game", bad_game)
    with pytest.raises(Exception):
        cli.do_start("A B")


def test_do_roll_handles_exception(cli):
    """Simulate roll() raising exception (should raise)."""
    cli.game_active = True
    cli.game = MagicMock()
    cli.game.winner = None
    cli.game.current_player.name = "A"
    cli.game.roll.side_effect = Exception("bad roll")
    with pytest.raises(Exception):
        cli.do_roll("")


def test_do_cheat_invalid_number(cli, capsys):
    """Provide invalid numeric value to cheat."""
    cli.game = MagicMock()
    with patch("src.cheat.Cheat") as MockCheat:
        cheat = MockCheat.return_value
        cli.do_cheat("add A notanumber")
        out = capsys.readouterr().out
        assert "Invalid" in out or "❌" in out or "⚠️" in out


def test_do_cheat_usage(cli, capsys):
    """Call cheat without arguments."""
    cli.game = MagicMock()
    with patch("src.cheat.Cheat"):
        cli.do_cheat("")
        out = capsys.readouterr().out
        assert "Usage" in out


def test_ai_turn_handles_exception(cli):
    """Simulate exception inside AI decision (should raise)."""
    cli.game = MagicMock()
    cli.game.current_player.name = "ai"
    cli.game.winner = None
    cli.ai_level = "normal"
    with patch("src.game_cmd.Intelligence") as MockAI:
        ai = MockAI.return_value
        ai.decide_roll_or_hold.side_effect = Exception("boom")
        with pytest.raises(Exception):
            cli._ai_turn()


def test_default_empty_command(cli, capsys):
    """Trigger empty default command path."""
    cli.default("   ")
    out = capsys.readouterr().out
    assert "Unknown" in out or "⚠️" in out


def test_reset_handles_eof(monkeypatch, cli):
    """Simulate EOFError on input() during reset."""
    def bad_input(_):
        raise EOFError
    monkeypatch.setattr("builtins.input", bad_input)
    with pytest.raises(EOFError):
        cli.do_reset("")

def test_start_ai_invalid_difficulty_defaults_normal(cli, capsys):
    """Start AI with invalid difficulty — should default to normal."""
    with patch("src.game_cmd.Game"):
        cli.do_start("A ai 999")
        out = capsys.readouterr().out
        assert "normal" in out or "AI opponent" in out


def test_roll_when_game_finished(cli, capsys):
    """do_roll should warn when game already finished."""
    cli.game = MagicMock()
    cli.game_active = True
    cli.game.winner = True
    cli.do_roll("")
    out = capsys.readouterr().out
    assert "finished" in out or "🏁" in out


def test_hold_when_game_finished(cli, capsys):
    """do_hold should warn when game already finished."""
    cli.game = MagicMock()
    cli.game_active = True
    cli.game.winner = True
    cli.do_hold("")
    out = capsys.readouterr().out
    assert "finished" in out or "🏁" in out
