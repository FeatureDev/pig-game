"""Unit tests for src/__init__.py (package integrity)."""
import importlib
import pkgutil
import sys
from pathlib import Path
import pytest
import src


def test_src_package_importable():
    """The src package should be importable."""
    assert "src" in sys.modules or importlib.import_module("src")


def test_src_has_expected_modules():
    """All core modules should be present in src."""
    expected = {
        "cheat", "dice", "game", "game_cmd",
        "highscore", "intelligence", "player"
    }
    found = {m.name for m in pkgutil.iter_modules(src.__path__)}
    assert expected.issubset(found)


def test_module_imports_individually():
    """Each submodule should import without errors."""
    for mod in ["cheat", "dice", "game", "game_cmd", "highscore", "intelligence", "player"]:
        imported = importlib.import_module(f"src.{mod}")
        assert imported.__name__.endswith(mod)
        assert hasattr(imported, "__doc__")


def test_src_doc_and_file_exist():
    """The src package should have a __doc__ and __file__."""
    assert hasattr(src, "__doc__")
    assert hasattr(src, "__file__")
    assert src.__file__.endswith("__init__.py")


def test_src_path_points_to_directory():
    """src.__path__ should point to an existing directory."""
    path = Path(src.__path__[0])
    assert path.exists()
    assert path.is_dir()


def test_no_circular_imports():
    """Ensure importing src modules doesn't cause circular import errors."""
    for name in ["dice", "player", "game", "cheat", "intelligence", "highscore"]:
        module = importlib.import_module(f"src.{name}")
        assert module is not None


def test_src_can_be_reloaded():
    """Reloading src should not raise any errors."""
    importlib.reload(src)
    assert "src" in sys.modules


def test_src_all_modules_have_docstrings():
    """All src submodules should contain at least a short docstring."""
    for mod in ["dice", "player", "game", "cheat", "intelligence", "highscore", "game_cmd"]:
        module = importlib.import_module(f"src.{mod}")
        doc = getattr(module, "__doc__", "")
        assert isinstance(doc, str)
        assert len(doc.strip()) > 10


def test_src_directory_contains_init():
    """Ensure __init__.py physically exists in src directory."""
    init_path = Path(src.__path__[0]) / "__init__.py"
    assert init_path.exists()
    assert init_path.is_file()


def test_src_module_listing_stable():
    """The number of modules in src should stay consistent."""
    modules = list(pkgutil.iter_modules(src.__path__))
    assert len(modules) >= 7
