# Copyright © 2017-2021 Alexander L. Hayes

"""
Tests for the ``srlearn.datasets.ToyCancer``
"""

from srlearn.datasets import load_toy_cancer


def test_train_test_exists():
    """Check that ``ToyCancer.train`` and ``ToyCancer.test`` exist."""
    train, test = load_toy_cancer()
    assert train is not None
    assert test is not None


def test_train_database_train_objects_exist():
    """Check for ``ToyCancer.train.pos``, ..., ``ToyCancer.train.facts``"""
    train, test = load_toy_cancer()
    assert train.pos is not None
    assert train.neg is not None
    assert train.facts is not None
    assert test.pos is not None
    assert test.neg is not None
    assert test.facts is not None


def test_len_train_pos_and_neg():
    """Simple test for length of training data pos/neg/facts."""
    train, test = load_toy_cancer()
    assert len(train.pos) == 4
    assert len(train.neg) == 2
    assert len(train.facts) == 15
    assert len(test.pos) == 3
    assert len(test.neg) == 2
    assert len(test.facts) == 13
