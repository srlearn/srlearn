# Copyright 2020 Alexander L. Hayes

"""
``to_json`` from pull request prior to 0.5.2

This will hopefully help catch if backwards-incompatible changes occur.
"""

from srlearn.rdn import BoostedRDN
from srlearn.rdn import BoostedRDNRegressor
from srlearn.database import Database
from srlearn import example_data
from numpy.testing import assert_array_equal
import numpy as np


def test_toy_cancer_predict_after_load():
    """Load a 0.5.2 ToyCancer json file and predict."""
    clf = BoostedRDN()
    clf.from_json("srlearn/tests/regression_tests/json/toy_cancer_0.5.2.json")
    _predictions = clf.predict(example_data.test)
    assert_array_equal(_predictions, np.array([1.0, 1.0, 1.0, 0.0, 0.0]))


def test_boston_predict_after_load():
    """Load a 0.5.2 BostonHousing json file and predict."""
    clf = BoostedRDNRegressor()
    clf.from_json("srlearn/tests/regression_tests/json/boston_0.5.2.json")

    test = Database.from_files(
        pos="datasets/Boston/test/pos.pl",
        neg="datasets/Boston/test/neg.pl",
        facts="datasets/Boston/test/facts.pl",
    )

    _predictions = clf.predict(test)
    assert len(_predictions) == 13
