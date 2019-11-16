# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.rdn.RDN
"""

import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal
from boostsrl.rdn import RDN
from boostsrl.background import Background
from boostsrl import example_data


def test_initialize_rdn_1():
    """Initialize an RDN with default parameters."""
    _dn = RDN()
    assert _dn.target == "None"
    assert _dn.n_estimators == 10


@pytest.mark.parametrize("test_input", [4, 10, 20])
def test_initialize_rdn_trees(test_input):
    """Initialize an RDN with various tree numbers."""
    _dn = RDN(n_estimators=test_input)
    assert _dn.n_estimators == test_input


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, bool, int, 1.5, "None", True]
)
def test_initialize_bad_target(test_input):
    """Initialize an RDN with incorrect target values."""
    _dn = RDN(target=test_input)
    with pytest.raises(ValueError):
        _dn.fit(example_data.train)


@pytest.mark.parametrize(
    "test_input", [0, -1, 1, 4, None, bool, int, 1.5, "None", "True", True]
)
def test_initialize_bad_background(test_input):
    """Test bad input for background"""
    _dn = RDN(target="cancer", background=test_input)
    with pytest.raises(ValueError):
        _dn.fit(example_data.train)


@pytest.mark.parametrize(
    "test_input", [0, -1, None, bool, int, 1.5, "None", "True", True, 3.3]
)
def test_initialize_bad_n_estimators(test_input):
    """Test bad values for n_estimators"""
    _dn = RDN(target="cancer", background=Background(), n_estimators=test_input)
    with pytest.raises(ValueError):
        _dn.fit(example_data.train)


def test_bad_shell_command():
    """Test running a shell command which cannot exit 0"""
    _dn = RDN()
    _call = "git bat"
    with pytest.raises(RuntimeError):
        _dn._call_shell_command(_call)


@pytest.mark.parametrize("test_input", [1, 2, 3, 4, 5])
def test_learn_example_dataset_1(test_input):
    """Learn from the example database."""
    _bk = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    _dn = RDN(background=_bk, target="cancer", n_estimators=test_input)
    _dn.fit(example_data.train)
    assert len(_dn.estimators_) == test_input


@pytest.mark.parametrize("test_input", [1, 2, 3, 4, 5])
def test_predict_example_data(test_input):
    """Test learn and predict."""
    _bk = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    _dn = RDN(background=_bk, target="cancer", n_estimators=test_input)
    _dn.fit(example_data.train)
    assert_array_equal(
        _dn.predict(example_data.test), np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    )


def test_predict_proba_test_data():
    """Assert arrays are almost equal on output of predict_proba()"""
    _bk = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    _dn = RDN(background=_bk, target="cancer", n_estimators=5)
    _dn.fit(example_data.train)
    assert_array_almost_equal(
        _dn.predict_proba(example_data.test),
        np.array([0.74, 0.74, 0.74, 0.25, 0.25]),
        decimal=2,
    )
