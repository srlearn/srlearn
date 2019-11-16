# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.base.BaseBoostedRelationalModel
"""

import pytest
from srlearn.base import BaseBoostedRelationalModel


def test_initialize_base_classifier():
    """Initialize a base classifier with default parameters."""
    _bm = BaseBoostedRelationalModel()
    assert _bm.target == "None"
    assert _bm.n_estimators == 10


@pytest.mark.parametrize("test_input", [4, 10, 20])
def test_initialize_base_classifier_trees(test_input):
    """Initialize a BaseModel with various tree numbers."""
    _bm = BaseBoostedRelationalModel(n_estimators=test_input)
    assert _bm.n_estimators == test_input


def test_bad_fit():
    """Check that fit raises a NotImplementedError"""
    _bm = BaseBoostedRelationalModel()
    with pytest.raises(NotImplementedError):
        _bm.fit("database")


def test_bad_predict():
    """Check that predict raises a NotImplementedError"""
    _bm = BaseBoostedRelationalModel()
    with pytest.raises(NotImplementedError):
        _bm.predict("database")


def test_bad_predict_proba():
    """Check that predict_proba raises a NotImplementedError"""
    _bm = BaseBoostedRelationalModel()
    with pytest.raises(NotImplementedError):
        _bm.predict_proba("database")
