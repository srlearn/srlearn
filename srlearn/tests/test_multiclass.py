# Copyright © 2017-2021 Alexander L. Hayes

"""
Tests related to multiclass classification.
"""

from relational_datasets import load
import pytest


def test_multiclass_estimator():
    """Test splitting the toy_machines dataset."""
    data = load("toy_machines", "v0.0.5")
