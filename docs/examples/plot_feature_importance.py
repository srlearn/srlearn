# Copyright © 2017-2021 Alexander L. Hayes

"""
Estimating Feature Importance
=============================

This demonstrates how to estimate feature importance based on how often
features are used as splitting criteria.
"""

# %%
# ``webkb`` is available in the 
# `relational-datasets package <https://srlearn.github.io/relational-datasets/>`_.
# A `brief webkb overview <https://srlearn.github.io/relational-datasets/dataset_descriptions/webkb/>`_ 
# is available with the relational-datasets documentation.
# 
# Calling ``load`` will return training and test folds:

from relational_datasets import load

train, test = load("webkb", fold=1)

# %%
# We'll set up the learning problem and fit the classifier:

from srlearn.rdn import BoostedRDN
from srlearn import Background

bkg = Background(
    modes=[
        "courseprof(-course,+person).",
        "courseprof(+course,-person).",
        "courseta(+course,-person).",
        "courseta(-course,+person).",
        "project(-proj,+person).",
        "project(+proj,-person).",
        "sameperson(-person,+person).",
        "faculty(+person).",
        "student(+person).",
    ],
    number_of_clauses=8,
)

clf = BoostedRDN(
    background=bkg,
    target="faculty",
    max_tree_depth=3,
    node_size=3,
    n_estimators=10,
)

clf.fit(train)

# %%
# The built-in ``feature_importances_`` attribute of a fit classifier is a
# Counter of how many times a features appears across the trees:

clf.feature_importances_

# %%
# These should generally be looked at while looking at the trees, so we'll
# plot the first tree here as well.
#
# It appears that the only features needed to determine if someone is a
# faculty member can roughly be stated as: "*Is this person a student?*" and
# "*Do these two names refer to the same person?*"
#
# This might be surprising, but shows that we can induce concepts like
# "*a faculty member is NOT a student.*"

from srlearn.plotting import export_digraph, plot_digraph

plot_digraph(export_digraph(clf, 0), format='html')
