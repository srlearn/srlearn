# Copyright 2021 Alexander L. Hayes

"""
Tests for compatibility with the relational-datasets package.
"""

import pytest
import numpy as np
from numpy.testing import assert_array_equal

from srlearn.datasets import load_toy_cancer
from srlearn.datasets import load_toy_father
from srlearn.background import Background
from srlearn.rdn import BoostedRDNClassifier
from srlearn.rdn import BoostedRDNRegressor

relational_datasets = pytest.importorskip("relational_datasets")


def test_compat_relational_datasets_toy_cancer():
    """Test that relational-datasets/toy_cancer can be loaded."""
    train, test = relational_datasets.load("toy_cancer")

    tc_train, tc_test = load_toy_cancer()

    assert tc_train.pos == train.pos
    assert tc_train.neg == train.neg
    assert tc_train.facts == train.facts

    assert tc_test.pos == test.pos
    assert tc_test.neg == test.neg
    assert tc_test.facts == test.facts


def test_compat_relational_datasets_toy_father():
    """Test that the relational-datasets/toy_father can be loaded."""
    train, test = relational_datasets.load("toy_father")
    f_train, f_test = load_toy_father()

    assert f_train.pos == train.pos
    assert f_train.neg == train.neg
    assert f_train.facts == train.facts

    assert f_test.pos == test.pos
    assert f_test.neg == test.neg
    assert f_test.facts == test.facts

def test_load_toy_cancer_boosted_rdn():
    """Test learning and inference with a loaded RelationalDataset object."""
    train, test = relational_datasets.load("toy_cancer")
    modes, _ = load_toy_cancer()
    bk = Background(modes=modes.modes)
    clf = BoostedRDNClassifier(target="cancer", background=bk, n_estimators=3)
    clf.fit(train)
    pred = clf.predict(test)
    assert len(clf.estimators_) == 3
    assert_array_equal(
        pred, np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    )


def test_load_boston_housing_boosted_rdn_regressor():
    """Test learning and inference with a loaded Boston Housing dataset."""
    train, test = relational_datasets.load("boston_housing")
    bk = Background(
        modes=[
            "crim(+id,#varsrim).",
             "zn(+id,#varzn).",
             "indus(+id,#varindus).",
             "chas(+id,#varchas).",
             "nox(+id,#varnox).",
             "rm(+id,#varrm).",
             "age(+id,#varage).",
             "dis(+id,#vardis).",
             "rad(+id,#varrad).",
             "tax(+id,#vartax).",
             "ptratio(+id,#varptrat).",
             "b(+id,#varb).",
             "lstat(+id,#varlstat).",
             "medv(+id).",
        ]
    )
    clf = BoostedRDNRegressor(background=bk, target="medv", n_estimators=3)
    clf.fit(train)
    pred = clf.predict(test)
    assert len(pred) == 13
