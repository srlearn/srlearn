# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.database.Database
"""

import pytest
import pathlib
from boostsrl.database import Database


def test_initialize_database_1():
    """
    Test initializing a Database with defualt settings.
    """
    _db = Database()
    assert _db.target == "None"
    assert _db.trees == 10
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


def test_initialize_database_2():
    """
    Test initializing a Database with a specific target.
    """
    _db = Database("cancer")
    assert _db.target == "cancer"
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


def test_initialize_database_switch_target_1():
    """
    Test switching the target value in a Database instance.
    """
    _db = Database()
    assert _db.target == "None"
    _db.target = "cancer"
    assert _db.target == "cancer"
    _db.target = "smokes"
    assert _db.target == "smokes"


def test_initialize_database_switch_trees_1():
    """
    Test switching the number of trees in a Database instance.
    """
    _db = Database()
    assert _db.trees == 10
    _db.trees = 15
    assert _db.trees == 15
    _db.trees = 5
    assert _db.trees == 5


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (10, 10),
        (5, 5),
        (1, 1),
        pytest.param(1, 2, marks=pytest.mark.xfail),
        pytest.param(10, 20, marks=pytest.mark.xfail),
        pytest.param(11, 10, marks=pytest.mark.xfail),
    ],
)
def test_tree_property(test_input, expected):
    """
    Test several parametrizations of the trees, with several that should not pass.
    """
    _db = Database()
    _db.trees = test_input
    assert _db.trees == expected


@pytest.mark.parametrize(
    "test_input", [1.5, (15 / 4), (10 / 3), None, "0", "None", "1"]
)
def test_tree_property_raises(test_input):
    """
    Test that exceptions are raised when invalid tree values are set.
    """
    _db = Database()
    with pytest.raises(Exception):
        _db.trees = test_input


@pytest.mark.parametrize("test_input", [(0), (1), (10 / 3), (None)])
def test_target_property_raises(test_input):
    """
    Test that exceptions are raised when invalid target values are set.
    """
    _db = Database()
    with pytest.raises(Exception):
        _db.target = test_input


def test_write_to_location_1(tmpdir):
    """
    Test that predicates are written to files in a target location with add_pos syntax.
    """
    _db = Database()
    _db.add_pos("a(b).")
    _db.add_neg("a(c).")
    _db.add_fact("d(b,c).")
    _db.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_pos.txt").read() == "a(b).\n"
    assert tmpdir.join("train_neg.txt").read() == "a(c).\n"
    assert tmpdir.join("train_facts.txt").read() == "d(b,c).\n"


def test_write_to_location_2(tmpdir):
    """
    Test that predicates are written to files in a target location with pos = [] syntax.
    """
    _db = Database()
    _db.pos = ["a(b)."]
    _db.neg = ["a(c)."]
    _db.facts = ["d(b,c)."]
    _db.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_pos.txt").read() == "a(b).\n"
    assert tmpdir.join("train_neg.txt").read() == "a(c).\n"
    assert tmpdir.join("train_facts.txt").read() == "d(b,c).\n"
