# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.rdn.RDN
"""

from boostsrl.rdn import RDN
from boostsrl.background import Background
from boostsrl import example_data
import pytest


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


def test_learn_example_dataset_1():
    """Learn from the example database."""

    _bk = Background(modes=example_data.train.modes)
    _dn = RDN(background=_bk, target="cancer", n_estimators=3)
    _dn.fit(example_data.train)
