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


def test_initialize_from_files_lazy_strings():
    """Test initializing from string filename with lazy loading."""
    _db = Database.from_files(
        pos="datasets/ToyFather/train/pos.pl",
        neg="datasets/ToyFather/train/neg.pl",
        facts="datasets/ToyFather/train/facts.pl",
        lazy_load=True,
    )
    assert _db.pos == "datasets/ToyFather/train/pos.pl"
    assert _db.neg == "datasets/ToyFather/train/neg.pl"
    assert _db.facts == "datasets/ToyFather/train/facts.pl"


def test_initialize_from_files_lazy_paths():
    """Test initializing from pathlib.Path filenames with lazy loading."""
    _db = Database.from_files(
        pos=pathlib.Path("datasets/ToyFather/train/pos.pl"),
        neg=pathlib.Path("datasets/ToyFather/train/neg.pl"),
        facts=pathlib.Path("datasets/ToyFather/train/facts.pl"),
        lazy_load=True,
    )
    assert _db.pos == pathlib.Path("datasets/ToyFather/train/pos.pl")
    assert _db.neg == pathlib.Path("datasets/ToyFather/train/neg.pl")
    assert _db.facts == pathlib.Path("datasets/ToyFather/train/facts.pl")


def test_initialize_from_files_not_lazy():
    """Test initializing from files without lazy loading."""

    _pos = "datasets/ToyFather/train/pos.pl"
    _neg = "datasets/ToyFather/train/neg.pl"
    _facts = "datasets/ToyFather/train/facts.pl"
    _db = Database.from_files(pos=_pos, neg=_neg, facts=_facts, lazy_load=False)

    assert isinstance(_db.pos, list)
    assert isinstance(_db.neg, list)
    assert isinstance(_db.facts, list)
    assert _db.pos == open(_pos).read().splitlines()
    assert _db.neg == open(_neg).read().splitlines()
    assert _db.facts == open(_facts).read().splitlines()


def test_initialize_mix(tmpdir):
    """Test initializing from a mix of lazy and lists."""

    _pos = "datasets/ToyFather/train/pos.pl"
    _neg = "datasets/ToyFather/train/neg.pl"
    _facts = pathlib.Path("datasets/ToyFather/train/facts.pl")
    _db = Database.from_files(pos=_pos, neg=_neg, facts=_facts, lazy_load=True)

    _db.neg = ["father(harrypotter,ronweasley)."]

    assert isinstance(_db.pos, str)
    assert isinstance(_db.neg, list)
    assert isinstance(_db.facts, pathlib.Path)


def test_lazy_write(tmpdir):
    """Test writing to a location after a lazy load."""

    _pos = "datasets/ToyFather/train/pos.pl"
    _neg = "datasets/ToyFather/train/neg.pl"
    _facts = "datasets/ToyFather/train/facts.pl"
    _db = Database.from_files(pos=_pos, neg=_neg, facts=_facts, lazy_load=True)

    assert isinstance(_db.pos, str)
    assert isinstance(_db.neg, str)
    assert isinstance(_db.facts, str)

    _db.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_pos.txt").read() == open(_pos).read()
    assert tmpdir.join("train_neg.txt").read() == open(_neg).read()
    assert tmpdir.join("train_facts.txt").read() == open(_facts).read()


def test_nonlazy_write(tmpdir):
    """Test writing to a location after a non-lazy load."""

    _pos = "datasets/ToyFather/train/pos.pl"
    _neg = "datasets/ToyFather/train/neg.pl"
    _facts = "datasets/ToyFather/train/facts.pl"
    _db = Database.from_files(pos=_pos, neg=_neg, facts=_facts, lazy_load=False)

    assert isinstance(_db.pos, list)
    assert isinstance(_db.neg, list)
    assert isinstance(_db.facts, list)

    _db.write(filename="train", location=pathlib.Path(tmpdir))
    assert tmpdir.join("train_pos.txt").read() == open(_pos).read()
    assert tmpdir.join("train_neg.txt").read() == open(_neg).read()
    assert tmpdir.join("train_facts.txt").read() == open(_facts).read()


def test_mixed_write(tmpdir):
    """Test writing to a location with a mix of lazy, non-lazy, and lists."""

    _pos = "datasets/ToyFather/train/pos.pl"
    _neg = "datasets/ToyFather/train/neg.pl"
    _facts = pathlib.Path("datasets/ToyFather/train/facts.pl")
    _db = Database.from_files(pos=_pos, neg=_neg, facts=_facts, lazy_load=True)

    _db.neg = ["father(harrypotter,ronweasley)."]

    assert isinstance(_db.pos, str)
    assert isinstance(_db.neg, list)
    assert isinstance(_db.facts, pathlib.Path)

    _db.write(filename="test", location=pathlib.Path(tmpdir))
    assert tmpdir.join("test_pos.txt").read() == open(_pos).read()
    assert tmpdir.join("test_neg.txt").read() == "father(harrypotter,ronweasley).\n"
    assert tmpdir.join("test_facts.txt").read() == open(_facts).read()


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
