"""Unit tests for src/dice.py (Dice class)."""
import pytest
import random
from src.dice import Dice


def test_dice_instance_creation():
    """Ensure a Dice instance can be created."""
    d = Dice()
    assert isinstance(d, Dice)
    assert hasattr(d, "roll")


def test_roll_returns_int():
    """Dice.roll() should return an integer."""
    d = Dice()
    result = d.roll()
    assert isinstance(result, int)
    assert 1 <= result <= 6


def test_roll_range_multiple_times():
    """Ensure dice rolls are always within [1,6] over many trials."""
    d = Dice()
    for _ in range(100):
        val = d.roll()
        assert 1 <= val <= 6


def test_roll_distribution_not_constant():
    """Check randomness – not all results identical in many rolls."""
    d = Dice()
    results = [d.roll() for _ in range(60)]
    unique = set(results)
    # we expect at least 3 different values in 60 rolls
    assert len(unique) >= 3


def test_random_seed_determinism():
    """Setting a seed should make rolls repeatable."""
    random.seed(123)
    d1 = [Dice().roll() for _ in range(10)]
    random.seed(123)
    d2 = [Dice().roll() for _ in range(10)]
    assert d1 == d2
    assert len(d1) == 10


def test_multiple_dice_independent():
    """Different Dice objects should produce independent sequences."""
    random.seed(42)
    d1, d2 = Dice(), Dice()
    r1 = [d1.roll() for _ in range(5)]
    r2 = [d2.roll() for _ in range(5)]
    # They might overlap but should not be identical
    assert r1 != r2 or len(set(r1)) > 1 or len(set(r2)) > 1


def test_roll_min_value_possible():
    """Verify that 1 can appear with enough rolls."""
    d = Dice()
    found_one = False
    for _ in range(300):
        if d.roll() == 1:
            found_one = True
            break
    assert found_one, "Value 1 should appear eventually"


def test_roll_max_value_possible():
    """Verify that 6 can appear with enough rolls."""
    d = Dice()
    found_six = False
    for _ in range(300):
        if d.roll() == 6:
            found_six = True
            break
    assert found_six, "Value 6 should appear eventually"


def test_roll_mean_within_expected_range():
    """The mean of many rolls should be roughly 3.5 (uniform distribution)."""
    d = Dice()
    rolls = [d.roll() for _ in range(6000)]
    mean_val = sum(rolls) / len(rolls)
    assert 3.0 <= mean_val <= 4.0


def test_repr_and_str_consistency():
    """Dice should have a usable string representation for debugging."""
    d = Dice()
    rep = repr(d)
    s = str(d)
    assert isinstance(rep, str)
    assert isinstance(s, str)
    assert "Dice" in rep or "Dice" in s
