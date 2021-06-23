# Copyright © 2020 Alexander L. Hayes

"""
Tests for srlearn.plotting
"""

from srlearn.rdn import BoostedRDN
from srlearn.background import Background
from srlearn import example_data
from srlearn.plotting import export_digraph
import pytest


@pytest.mark.parametrize("test_input", [1, 1.5, bool, int, True])
def test_cannot_export_bad_data(test_input):
    with pytest.raises(TypeError):
        _ = export_digraph(test_input, tree_index=0)


def test_cannot_read_outside_length_of_dotfiles():
    bkg = Background(modes=example_data.train.modes)
    clf = BoostedRDN(target="cancer", background=bkg)
    clf.fit(example_data.train)
    for test_input in [-10, -5, -1, 10]:
        with pytest.raises(IndexError):
            _ = export_digraph(clf, tree_index=test_input)
