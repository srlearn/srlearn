# Copyright © 2020 Alexander L. Hayes

"""
Estimating Feature Importance
=============================

This demonstrates how to estimate feature importance based on how often
features are used as splitting criteria.
"""

from srlearn.rdn import BoostedRDN
from srlearn import Background
from srlearn.database import Database

import numpy as np
import matplotlib.pyplot as plt

webkb_train = Database.from_files(
    pos="../../datasets/webkb/train1/train1_pos.txt",
    neg="../../datasets/webkb/train1/train1_neg.txt",
    facts="../../datasets/webkb/train1/train1_facts.txt",
)

bkg = Background(
    modes=[
        "courseprof(-Course, +Person).",
        "courseprof(+Course, -Person).",
        "courseta(+Course, -Person).",
        "courseta(-Course, +Person).",
        "project(-Proj, +Person).",
        "project(+Proj, -Person).",
        "sameperson(-Person, +Person).",
        "faculty(+Person).",
        "student(+Person).",
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

clf.fit(webkb_train)
print(clf.feature_importance())
