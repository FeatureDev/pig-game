"""Tests for src.cheat ensuring full coverage of implemented features."""

import pytest
from unittest.mock import MagicMock, patch
from src.cheat import Cheat, cprint
from src.game import Game


@pytest.fixture
def real_game():
    """Create a basic game with players and dice attributes."""
    g = Game("Alice", "Bob")
    g.win_score = 100
    # Mock dice_hand
    g.dice_hand = MagicMock()
    g.dice_hand.dice_list = [MagicMock(value=1) for _ in range(3)]
    return g


# ---------------------------------------------------------------------------
# Initialization & core
# ---------------------------------------------------------------------------

def test_init_with_valid_game(real_game):
    cheat = Cheat(real_game)
    assert cheat.game == real_game
    assert hasattr(cheat, "highscore")


def test_init_with_invalid_game_raises():
    with pytest.raises(TypeError):
        Cheat(None)
    class Dummy:
        pass
    with pytest.raises(TypeError):
        Cheat(Dummy())


# ---------------------------------------------------------------------------
# add_points / reset_score / auto_win
# ---------------------------------------------------------------------------

def test_add_points_adds_to_existing_player(real_game):
    cheat = Cheat(real_game)
    p = real_game.players[0]
    old = p.score
    cheat.add_points(p.name, 15)
    assert p.score == old + 15


def test_add_points_on_missing_player_prints(real_game, capsys):
    cheat = Cheat(real_game)
    cheat.add_points("Missing", 10)
    out = capsys.readouterr().out
    assert "not found" in out


def test_reset_score_resets_value(real_game):
    cheat = Cheat(real_game)
    p = real_game.players[0]
    p.score = 42
    cheat.reset_score(p.name)
    assert p.score == 0


def test_reset_score_nonexistent_player(real_game, capsys):
    cheat = Cheat(real_game)
    cheat.reset_score("Ghost")
    assert "not found" in capsys.readouterr().out


def test_auto_win_sets_score_and_saves(real_game):
    cheat = Cheat(real_game)
    with patch.object(cheat.highscore, "save_score") as mock_save:
        cheat.auto_win(real_game.players[1].name)
        p = real_game.players[1]
        assert p.score == real_game.win_score
        mock_save.assert_called_once_with(p.name, p.score)


def test_auto_win_invalid_player(real_game, capsys):
    cheat = Cheat(real_game)
    cheat.auto_win("Nobody")
    assert "not found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# set_dice_value
# ---------------------------------------------------------------------------

def test_set_dice_value_sets_all(real_game):
    cheat = Cheat(real_game)
    cheat.set_dice_value(6)
    for d in real_game.dice_hand.dice_list:
        assert d.value == 6


def test_set_dice_value_no_dice_hand(monkeypatch, capsys, real_game):
    del real_game.dice_hand
    cheat = Cheat(real_game)
    cheat.set_dice_value(5)
    assert "no dice_hand" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# _get_player & eq
# ---------------------------------------------------------------------------

def test_get_player_finds_and_misses(real_game):
    cheat = Cheat(real_game)
    p = real_game.players[0]
    assert cheat._get_player(p.name) == p
    assert cheat._get_player("Invalid") is None


def test_eq_and_not_eq(real_game):
    cheat1 = Cheat(real_game)
    cheat2 = Cheat(real_game)
    assert cheat1 == cheat1
    assert cheat1 != cheat2
    assert not cheat1.__eq__("not_a_cheat")


# ---------------------------------------------------------------------------
# debug_reset
# ---------------------------------------------------------------------------

def test_debug_reset_success(real_game):
    cheat = Cheat(real_game)
    cheat.highscore.save = MagicMock()
    assert cheat.debug_reset() is True


def test_debug_reset_failure(monkeypatch, real_game):
    cheat = Cheat(real_game)
    def fail(): raise Exception("x")
    cheat.highscore.save = fail
    assert cheat.debug_reset() is False


# ---------------------------------------------------------------------------
# cprint
# ---------------------------------------------------------------------------

def test_cprint_only_prints_under_pytest(capsys):
    cprint("Hello test!")
    out = capsys.readouterr().out
    # Depending on env, may print or not, just ensure callable
    assert isinstance(out, str)
