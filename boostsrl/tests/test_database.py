# Copyright 2017, 2018, 2019 Alexander L. Hayes

from boostsrl.database import database
import pytest


def test_initialize_database_1():
    _db = database()
    assert _db.target == "None"
    assert _db.trees == 10
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


def test_initialize_database_2():
    _db = database("cancer")
    assert _db.target == "cancer"
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


def test_initialize_database_switch_target_1():
    _db = database()
    assert _db.target == "None"
    _db.target = "cancer"
    assert _db.target == "cancer"
    _db.target = "smokes"
    assert _db.target == "smokes"


def test_initialize_database_switch_trees_1():
    _db = database()
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
    _db = database()
    _db.trees = test_input
    assert _db.trees == expected


@pytest.mark.parametrize(
    "test_input", [(1.5), (15 / 4), (10 / 3), (None), ("0"), ("None"), ("1")]
)
def test_tree_property_raises(test_input):
    _db = database()
    with pytest.raises(Exception):
        _db.trees = test_input


@pytest.mark.parametrize("test_input", [(0), (1), (10 / 3), (None)])
def test_target_property_raises(test_input):
    _db = database()
    with pytest.raises(Exception):
        _db.target = test_input


def test_write_to_location_1(tmpdir):
    _db = database()
    _db.add_pos("a(b).")
    _db.add_neg("a(c).")
    _db.add_fact("d(b,c).")
    _db.write(location=tmpdir)
    assert tmpdir.join(f"{_db.file_prefix}_pos.txt").read() == "a(b).\n"
    assert tmpdir.join(f"{_db.file_prefix}_neg.txt").read() == "a(c).\n"
    assert tmpdir.join(f"{_db.file_prefix}_facts.txt").read() == "d(b,c).\n"


def test_write_to_location_2(tmpdir):
    _db = database()
    _db.pos = ["a(b)."]
    _db.neg = ["a(c)."]
    _db.facts = ["d(b,c)."]
    _db.write(location=tmpdir)
    assert tmpdir.join(f"{_db.file_prefix}_pos.txt").read() == "a(b).\n"
    assert tmpdir.join(f"{_db.file_prefix}_neg.txt").read() == "a(c).\n"
    assert tmpdir.join(f"{_db.file_prefix}_facts.txt").read() == "d(b,c).\n"
