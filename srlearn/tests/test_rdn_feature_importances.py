# Copyright © 2020 Alexander L. Hayes

"""
Tests for srlearn.rdn.feature_importances_
"""

import pytest
from srlearn.rdn import BoostedRDN
from srlearn.background import Background
from srlearn import example_data


def test_feature_importances_before_fit():
    """Test that one cannot get feature importances before fit."""
    rdn = BoostedRDN()
    with pytest.raises(ValueError):
        rdn.feature_importances_


def test_feature_importances_toy_cancer():
    """Test getting the feature importances from the Toy-Cancer set."""
    bkg = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    rdn = BoostedRDN(
        target="cancer",
        background=bkg,
        n_estimators=10,
    )
    rdn.fit(example_data.train)
    _features = rdn.feature_importances_
    assert _features.most_common(1)[0] == ("smokes", 10)
