# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.rdn.BoostedRDN
"""

import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal
from srlearn.rdn import BoostedRDN
from srlearn.background import Background
from srlearn.datasets import load_toy_cancer


def test_initialize_rdn_1():
    """Initialize an RDN with default parameters."""
    _dn = BoostedRDN()
    assert _dn.target == "None"
    assert _dn.n_estimators == 10


@pytest.mark.parametrize("test_input", [4, 10, 20])
def test_initialize_rdn_trees(test_input):
    """Initialize an RDN with various tree numbers."""
    _dn = BoostedRDN(n_estimators=test_input)
    assert _dn.n_estimators == test_input


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, bool, int, 1.5, "None", True]
)
def test_initialize_bad_target(test_input):
    """Initialize an RDN with incorrect target values."""
    _dn = BoostedRDN(target=test_input)
    toy_cancer = load_toy_cancer()
    with pytest.raises(ValueError):
        _dn.fit(toy_cancer.train)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, bool, int, 1.5, "None", "True", True]
)
def test_initialize_bad_background(test_input):
    """Test bad input for background"""
    _dn = BoostedRDN(target="cancer", background=test_input)
    toy_cancer = load_toy_cancer()
    with pytest.raises(ValueError):
        _dn.fit(toy_cancer.train)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, bool, int, 1.5, "None", "True", True, 3.3]
)
def test_initialize_bad_n_estimators(test_input):
    """Test bad values for n_estimators"""
    _dn = BoostedRDN(target="cancer", background=Background(), n_estimators=test_input)
    toy_cancer = load_toy_cancer()
    with pytest.raises(ValueError):
        _dn.fit(toy_cancer.train)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, bool, int, "None", "True", True]
)
def test_initialize_bad_neg_pos_ratio(test_input):
    """Tests bad values for neg_pos_ratio"""
    _dn = BoostedRDN(target="cancer", background=Background(), neg_pos_ratio=test_input)
    toy_cancer = load_toy_cancer()    
    with pytest.raises(ValueError):
        _dn.fit(toy_cancer.train)


def test_bad_shell_command():
    """Test running a shell command which cannot exit 0"""
    _dn = BoostedRDN()
    _call = "git bat"
    with pytest.raises(RuntimeError):
        _dn._call_shell_command(_call)


@pytest.mark.parametrize("test_input", [1, 2, 3, 4, 5])
def test_learn_example_dataset_1(test_input):
    """Learn from the example database."""
    toy_cancer = load_toy_cancer()
    _bk = Background(modes=toy_cancer.train.modes)
    _dn = BoostedRDN(background=_bk, target="cancer", n_estimators=test_input)
    _dn.fit(toy_cancer.train)
    assert len(_dn.estimators_) == test_input


@pytest.mark.parametrize("test_input", [1, 2, 3, 4, 5])
def test_predict_example_data(test_input):
    """Test learn and predict."""
    toy_cancer = load_toy_cancer()
    _bk = Background(modes=toy_cancer.train.modes)
    _dn = BoostedRDN(background=_bk, target="cancer", n_estimators=test_input)
    _dn.fit(toy_cancer.train)
    assert_array_equal(
        _dn.predict(toy_cancer.test), np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    )


def test_predict_proba_test_data():
    """Assert arrays are almost equal on output of predict_proba()"""
    toy_cancer = load_toy_cancer()
    _bk = Background(modes=toy_cancer.train.modes)
    _dn = BoostedRDN(background=_bk, target="cancer", n_estimators=5)
    _dn.fit(toy_cancer.train)
    assert_array_almost_equal(
        _dn.predict_proba(toy_cancer.test),
        np.array([0.74, 0.74, 0.74, 0.25, 0.25]),
        decimal=2,
    )
