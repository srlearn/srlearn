# Copyright © 2020 Alexander L. Hayes

"""
Tests for serializing models to json with
``srlearn.base.BaseBoostedRelationalModel``,,
and anything which extends this class.
"""

import numpy as np
from numpy.testing import assert_array_equal
from srlearn.rdn import BoostedRDN
from srlearn.rdn import BoostedRDNRegressor
from srlearn.background import Background
from srlearn.database import Database
from srlearn.datasets import load_toy_cancer


def test_serialize_BoostedRDN(tmpdir):
    """Test that inference is possible after loading from json"""
    output_json = tmpdir.join("ToyCancerRDN.json")
    train, test = load_toy_cancer()
    bkg = Background(modes=train.modes)
    rdn = BoostedRDN(background=bkg, target="cancer", n_estimators=5)
    rdn.fit(train)
    rdn.to_json(output_json)

    # New BoostedRDN instance, loading from file, and running.
    rdn2 = BoostedRDN()
    rdn2.from_json(output_json)

    _predictions = rdn2.predict(test)
    assert len(rdn2.estimators_) == 5
    assert_array_equal(
        _predictions, np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    )


def test_serialize_BoostedRDNRegressor(tmpdir):
    """Test serializing and inference with a regressor object."""
    output_json = tmpdir.join("BostonHousingRDN.json")

    train = Database.from_files(
        pos="datasets/Boston/train/pos.pl",
        neg="datasets/Boston/train/neg.pl",
        facts="datasets/Boston/train/facts.pl",
    )

    bkg = Background(
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

    rdn = BoostedRDNRegressor(background=bkg, target="medv", n_estimators=5)
    rdn.fit(train)
    rdn.to_json(output_json)

    # New BoostedRDN instance, loading from file, and running.
    rdn2 = BoostedRDNRegressor()
    rdn2.from_json(output_json)

    test = Database.from_files(
        pos="datasets/Boston/test/pos.pl",
        neg="datasets/Boston/test/neg.pl",
        facts="datasets/Boston/test/facts.pl",
    )

    _predictions = rdn2.predict(test)
    assert len(_predictions) == 13
