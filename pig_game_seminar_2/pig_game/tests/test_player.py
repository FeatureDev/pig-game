"""Full coverage tests for src.player (Player logic)."""

import pytest
from src.player import Player, cprint


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def test_init_valid_and_prints(capsys):
    p = Player("Alice")
    assert p.name == "Alice"
    assert p.score == 0
    out = capsys.readouterr().out
    assert "Player created" in out


@pytest.mark.parametrize("bad_name", [None, 123, [], {}])
def test_init_invalid_type_raises(bad_name):
    with pytest.raises(TypeError):
        Player(bad_name)


@pytest.mark.parametrize("empty_name", ["", "   "])
def test_init_empty_name_raises(empty_name):
    with pytest.raises(ValueError):
        Player(empty_name)


# ---------------------------------------------------------------------------
# add_score
# ---------------------------------------------------------------------------

def test_add_score_adds_points(capsys):
    p = Player("Bob")
    p.add_score(10)
    assert p.score == 10
    out = capsys.readouterr().out
    assert "gained" in out


def test_add_score_rejects_negative(capsys):
    p = Player("Carl")
    with pytest.raises(ValueError):
        p.add_score(-5)
    out = capsys.readouterr().out
    assert "invalid" in out


def test_add_score_rejects_non_int():
    p = Player("Dana")
    with pytest.raises(TypeError):
        p.add_score("10")


# ---------------------------------------------------------------------------
# reset_score
# ---------------------------------------------------------------------------

def test_reset_score_sets_to_zero(capsys):
    p = Player("Eve")
    p.score = 30
    p.reset_score()
    assert p.score == 0
    out = capsys.readouterr().out
    assert "reset" in out


# ---------------------------------------------------------------------------
# rename
# ---------------------------------------------------------------------------

def test_rename_valid_and_prints(capsys):
    p = Player("Frank")
    p.rename("Freddy")
    assert p.name == "Freddy"
    out = capsys.readouterr().out
    assert "renamed" in out


def test_rename_invalid_type():
    p = Player("Greg")
    with pytest.raises(TypeError):
        p.rename(123)


def test_rename_empty_string_raises(capsys):
    p = Player("Helen")
    with pytest.raises(ValueError):
        p.rename("   ")
    out = capsys.readouterr().out
    assert "ignored" in out


# ---------------------------------------------------------------------------
# Equality & Representation
# ---------------------------------------------------------------------------

def test_eq_same_and_different():
    p1 = Player("Ivy")
    p2 = Player("Ivy")
    p3 = Player("Jack")
    p2.score = 5
    p1.score = 5
    assert p1 == p2
    assert p1 != p3
    assert not p1.__eq__("not_player")


def test_repr_and_str():
    p = Player("Karl")
    text = repr(p)
    assert "Player" in text
    s = str(p)
    assert "Karl" in s and "p" in s


# ---------------------------------------------------------------------------
# clone
# ---------------------------------------------------------------------------

def test_clone_creates_new_identical_player(capsys):
    p1 = Player("Liam")
    p1.add_score(12)
    p2 = p1.clone()

    # Same values, but different objects
    assert p1 == p2
    assert p1 is not p2

    out = capsys.readouterr().out
    assert "Cloned player" in out


# ---------------------------------------------------------------------------
# cprint behavior
# ---------------------------------------------------------------------------

def test_cprint_writes_under_pytest(capsys):
    cprint("Hello test!")
    out = capsys.readouterr().out
    assert isinstance(out, str)
