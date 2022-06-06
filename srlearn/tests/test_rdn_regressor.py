# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.rdn.BoostedRDNRegressor
"""

from srlearn.rdn import BoostedRDNRegressor
from srlearn.background import Background
from relational_datasets import load


_boston_housing_modes = """crim(+id,#varsrim).
zn(+id,#varzn).
indus(+id,#varindus).
chas(+id,#varchas).
nox(+id,#varnox).
rm(+id,#varrm).
age(+id,#varage).
dis(+id,#vardis).
rad(+id,#varrad).
tax(+id,#vartax).
ptratio(+id,#varptrat).
b(+id,#varb).
lstat(+id,#varlstat).
medv(+id).
"""


def test_regression_boostsrl_backend():
    train, test = load("boston_housing", "v0.0.5")
    _bk = Background(modes=_boston_housing_modes.splitlines())
    _dn = BoostedRDNRegressor(background=_bk, target="medv", solver="BoostSRL", n_estimators=5)
    _dn.fit(train)
    _dn.predict(test)


def test_classification_srlboost_backend():
    train, test = load("boston_housing", "v0.0.5")
    _bk = Background(modes=_boston_housing_modes.splitlines())
    _dn = BoostedRDNRegressor(background=_bk, target="medv", solver="SRLBoost", n_estimators=5)
    _dn.fit(train)
    _dn.predict(test)
