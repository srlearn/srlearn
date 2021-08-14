# Copyright © 2017-2021 Alexander L. Hayes

"""
Tests for the ``srlearn.datasets.ToyFather``
"""

from srlearn.datasets import load_toy_father


def test_len_toy_father():
    """Simple test for length of training data pos/neg/facts."""
    train, test = load_toy_father()
    assert len(train.pos) == 5
    assert len(train.neg) == 21
    assert len(train.facts) == 41
    assert len(test.pos) == 3
    assert len(test.neg) == 4
    assert len(test.facts) == 11
