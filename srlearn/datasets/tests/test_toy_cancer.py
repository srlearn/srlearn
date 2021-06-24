# Copyright © 2017-2021 Alexander L. Hayes

"""
Tests for the ``srlearn.datasets.ToyCancer``
"""

from srlearn.datasets import load_toy_cancer


def test_train_test_exists():
    """Check that ``ToyCancer.train`` and ``ToyCancer.test`` exist."""
    ToyCancer = load_toy_cancer()
    assert ToyCancer.train is not None
    assert ToyCancer.test is not None


def test_train_database_train_objects_exist():
    """Check for ``ToyCancer.train.pos``, ..., ``ToyCancer.train.facts``"""
    ToyCancer = load_toy_cancer()
    assert ToyCancer.train.pos is not None
    assert ToyCancer.train.neg is not None
    assert ToyCancer.train.facts is not None


def test_train_database_test_objects_exist():
    """Check for ``ToyCancer.test.pos``, ..., ``ToyCancer.test.facts``"""
    ToyCancer = load_toy_cancer()
    assert ToyCancer.test.pos is not None
    assert ToyCancer.test.neg is not None
    assert ToyCancer.test.facts is not None


def test_len_train_pos_and_neg():
    """Simple test for length of training data pos/neg/facts."""
    ToyCancer = load_toy_cancer()
    assert len(ToyCancer.train.pos) == 4
    assert len(ToyCancer.train.neg) == 2
    assert len(ToyCancer.train.facts) == 15


def test_len_test_pos_and_neg():
    """Simple test for length of training data pos/neg/facts."""
    ToyCancer = load_toy_cancer()
    assert len(ToyCancer.test.pos) == 3
    assert len(ToyCancer.test.neg) == 2
    assert len(ToyCancer.test.facts) == 13
