# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.database.Database
"""

import pathlib
from boostsrl.database import Database


def test_initialize_database_1():
    """
    Test initializing a Database with defualt settings.
    """
    _db = Database()
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


def test_initialize_database_2():
    """
    Test initializing a Database with a specific target.
    """
    _db = Database()
    assert _db.pos == []
    assert _db.neg == []
    assert _db.facts == []


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
