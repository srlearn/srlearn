# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.background.Background
"""

from boostsrl.background import Background
from boostsrl import example_data
import pytest


def test_initialize_background_knowledge_1():
    """
    Test initializing a Background object with default settings.
    """
    _bk = Background()
    assert _bk.modes is None
    assert not _bk.line_search
    assert not _bk.recursion


def test_initialize_example_background_knowledge_1():
    """Test initializing with example_data"""
    _bk = Background(modes=example_data.train.background)
    assert _bk.modes == example_data.train.background
    assert not _bk.line_search
    assert not _bk.recursion


@pytest.mark.parametrize(
    "test_input", [1.5, 4, "True", "False", bool, int]
)
def test_initialize_bad_background_knowledge_modes(test_input):
    """Incorrect modes settings"""
    with pytest.raises(ValueError):
        _bk = Background(modes=test_input)


@pytest.mark.parametrize(
    "test_input", [1.5, 4, None, "True", "False", bool, int]
)
def test_initialize_bad_background_knowledge_recursion(test_input):
    """Incorrect recursion settings."""
    with pytest.raises(ValueError):
        _bk = Background(recursion=test_input)


@pytest.mark.parametrize(
    "test_input", [1.5, 4, None, "True", "False", bool, int]
)
def test_initialize_bad_background_knowledge_line_search(test_input):
    """Incorrect line_search settings"""
    with pytest.raises(ValueError):
        _bk = Background(line_search=test_input)

