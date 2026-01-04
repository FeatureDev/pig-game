"""Full coverage tests for src.intelligence (AI decision engine)."""

import pytest
import random
from unittest.mock import patch
from src.intelligence import Intelligence


# ---------------------------------------------------------------------------
# Initialization & basic structure
# ---------------------------------------------------------------------------

def test_init_valid_levels(capsys):
    for level in ("easy", "normal", "hard"):
        ai = Intelligence(level)
        assert ai.level == level
        out = capsys.readouterr().out
        assert "Intelligence initialized" in out


@pytest.mark.parametrize("level", ["noob", "", None])
def test_init_invalid_level_raises(level):
    with pytest.raises(ValueError):
        Intelligence(level)


# ---------------------------------------------------------------------------
# Strategy tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("turn_score,expected", [(3, "roll"), (8, "hold")])
def test_easy_strategy_decision(turn_score, expected):
    ai = Intelligence("easy")
    result = ai.decide_roll_or_hold(turn_score, 0)
    assert result == expected


def test_normal_strategy_threshold(monkeypatch):
    ai = Intelligence("normal")
    monkeypatch.setattr(random, "randint", lambda a, b: 15)
    # below threshold
    assert ai.decide_roll_or_hold(10, 0) == "roll"
    # at threshold
    assert ai.decide_roll_or_hold(15, 0) == "hold"


@pytest.mark.parametrize(
    "turn,total,expected",
    [
        (5, 50, "roll"),   # early game
        (25, 50, "hold"),
        (10, 80, "roll"),  # mid game
        (15, 80, "hold"),
        (8, 95, "hold"),   # late game (AI plays safe near win)
        (12, 95, "hold"),
    ],
)
def test_hard_strategy_branches(turn, total, expected):
    ai = Intelligence("hard")
    result = ai.decide_roll_or_hold(turn, total)
    assert result == expected


def test_win_condition_triggers_hold():
    ai = Intelligence("easy")
    assert ai.decide_roll_or_hold(5, 99) == "hold"


# ---------------------------------------------------------------------------
# Utility methods
# ---------------------------------------------------------------------------

def test_set_level_and_invalid(capsys):
    ai = Intelligence("easy")
    ai.set_level("hard")
    assert ai.level == "hard"
    out = capsys.readouterr().out
    assert "AI level set" in out

    with pytest.raises(ValueError):
        ai.set_level("invalid")


def test_repr_and_str_methods():
    ai = Intelligence("normal")
    r = repr(ai)
    s = str(ai)
    assert "Intelligence" in r
    assert "AI" in s


def test_should_hold_valid_and_invalid(monkeypatch):
    ai = Intelligence("normal")

    dummy_game = type(
        "G", (),
        {"current_player": type("P", (), {"score": 20})(), "turn_score": 10}
    )()
    # valid call
    result = ai.should_hold(dummy_game)
    assert isinstance(result, bool)

    # force an exception branch
    monkeypatch.setattr(ai, "decide_roll_or_hold", lambda *_: (_ for _ in ()).throw(Exception("boom")))
    result = ai.should_hold(dummy_game)
    assert result is False


def test_debug_force_decision_valid_and_fallback(monkeypatch):
    ai = Intelligence("easy")
    # valid
    result = ai.debug_force_decision(turn=5, total=50)
    assert isinstance(result, bool)

    # simulate internal failure
    monkeypatch.setattr(ai, "should_hold", lambda *_: (_ for _ in ()).throw(Exception("fail")))
    assert ai.debug_force_decision(turn=5) is False


def test_cover_all_strategies_runs_all():
    ai = Intelligence("normal")
    assert ai._cover_all_strategies() is True


# ---------------------------------------------------------------------------
# Edge paths / redundant coverage
# ---------------------------------------------------------------------------

def test_invalid_internal_level_path(monkeypatch):
    ai = Intelligence("normal")
    ai.level = "unknown"
    result = ai.decide_roll_or_hold(10, 50)
    assert result == "roll"
