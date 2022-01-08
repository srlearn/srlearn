# Copyright © 2020 Alexander L. Hayes

"""
Tests for srlearn.plotting
"""

import pytest

from srlearn.rdn import BoostedRDNClassifier
from srlearn.background import Background
from srlearn.datasets import load_toy_cancer
from srlearn.plotting import export_digraph


@pytest.mark.parametrize("test_input", [1, 1.5, bool, int, True])
def test_cannot_export_bad_data(test_input):
    """Test that a TypeError is raised when wrong instances are passed."""
    with pytest.raises(TypeError):
        _ = export_digraph(test_input, tree_index=0)


def test_cannot_read_outside_length_of_dotfiles():
    """Test that invalid tree indexes raise errors."""
    train, _ = load_toy_cancer()
    bkg = Background(modes=train.modes)
    clf = BoostedRDNClassifier(target="cancer", background=bkg)
    clf.fit(train)
    for test_input in [-10, -5, -1, 10]:
        with pytest.raises(IndexError):
            _ = export_digraph(clf, tree_index=test_input)
