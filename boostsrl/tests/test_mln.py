# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for boostsrl.mln.MLNClassifier
"""

import pytest
import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal
from boostsrl.mln import MLNClassifier
from boostsrl.background import Background
from boostsrl import example_data


def test_initialize_mln_1():
    """Initialize an MLNClassifier with default parameters."""
    _mln = MLNClassifier()
    assert _mln.target == "None"
    assert _mln.n_estimators == 10


@pytest.mark.parametrize("test_input", [4, 10, 20])
def test_initialize_mln_trees(test_input):
    """Initialize an MLNClassifier with various tree numbers."""
    _mln = MLNClassifier(n_estimators=test_input)
    assert _mln.n_estimators == test_input
