"""
=====================
Smokes-Friends-Cancer
=====================

The smokes-friends-cancer example is a common first example in probabilistic relational models, here
we use this set to learn a Relational Dependency Network (:class:`srlearn.rdn.RDN`).

This makes use of :class:`srlearn.example_data`, which provides two `srlearn.Database` objects named
``example_data.train`` and ``example_data.test``.

This shows how the margin between positive and negative examples is maximized as the number of
iterations of boosting increases.
"""

from srlearn.rdn import RDN
from srlearn import Background
from srlearn import example_data

import numpy as np
import matplotlib.pyplot as plt

bk = Background(
    modes=example_data.train.modes,
    use_std_logic_variables=True,
)

clf = RDN(
    background=bk,
    target='cancer',
    max_tree_depth=2,
    node_size=2,
    n_estimators=20,
)

clf.fit(example_data.train)

x = np.arange(1, 21)
y_pos = []
y_neg = []
thresholds = []

for n_trees in x:
    clf.set_params(n_estimators=n_trees)
    probs = clf.predict_proba(example_data.test)

    thresholds.append(clf.threshold_)
    y_pos.append(np.mean(probs[np.nonzero(clf.classes_)]))
    y_neg.append(np.mean(probs[clf.classes_ == 0]))

thresholds = np.array(thresholds)
y_pos = np.array(y_pos)
y_neg = np.array(y_neg)

plt.plot(x, y_pos, "b-", label="Mean Probability of positive examples")
plt.plot(x, y_neg, "r-", label="Mean Probability of negative examples")
plt.plot(x, thresholds, "k--", label="Margin")
plt.title("Class Probability vs. Number Trees")
plt.xlabel("Number of Trees")
plt.ylabel("Probability of belonging to Positive Class")
plt.legend(loc="best")
plt.show()
