# Copyright 2020 Alexander L. Hayes

"""
``to_json`` from pull request prior to 0.5.2

This will hopefully help catch if backwards-incompatible changes occur.
"""

from srlearn.rdn import BoostedRDN
from srlearn.rdn import BoostedRDNRegressor
from srlearn.database import Database
from srlearn.datasets import load_toy_cancer
from numpy.testing import assert_array_equal
import numpy as np
import pytest


@pytest.mark.parametrize("test_input", ["0.5.5-dev", "0.5.5a-dev"])
def test_toy_cancer_predict_after_load(test_input):
    """Load a ToyCancer json file and predict."""
    clf = BoostedRDN()
    clf.from_json("srlearn/tests/regression_tests/json/toy_cancer_{0}.json".format(test_input))
    toy_cancer = load_toy_cancer()
    _predictions = clf.predict(toy_cancer.test)
    assert_array_equal(_predictions, np.array([1.0, 1.0, 1.0, 0.0, 0.0]))


@pytest.mark.parametrize("test_input", ["0.5.2", "0.5.3", "0.5.4", "0.5.5-dev"])
def test_boston_predict_after_load(test_input):
    """Load a 0.5.2 BostonHousing json file and predict."""
    clf = BoostedRDNRegressor()
    clf.from_json("srlearn/tests/regression_tests/json/boston_{0}.json".format(test_input))

    test = Database.from_files(
        pos="datasets/Boston/test/pos.pl",
        neg="datasets/Boston/test/neg.pl",
        facts="datasets/Boston/test/facts.pl",
    )

    _predictions = clf.predict(test)
    assert len(_predictions) == 13
