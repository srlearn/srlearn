# Copyright © 2017-2021 Alexander L. Hayes

"""
===========================
Family Relationships Domain
===========================

**Overview**: This example motivates learning about family relationships from
examples of *Harry Potter* characters, then applies those rules to characters
from *Pride and Prejudice*.
"""

from srlearn.datasets import load_toy_father

train, test = load_toy_father()

# %%
# The training examples in the "*Toy Father*" dataset describes relationships and facts about
# *Harry Potter* characters.
#
# The first *positive* example: ``father(harrypotter,jamespotter).`` means
# "*James Potter is the father of Harry Potter.*"
#
# The first *negative* example: ``father(harrypotter,mrgranger).`` can be interpreted as
# "*Mr. Granger is not the father of Harry Potter.*"

print(train.pos[0], "→    James Potter is the father of Harry Potter.")
print(train.neg[0], "  → Mr. Granger is not the father of Harry Potter.")

# %%
# The *facts* contain three additional predicates: describing ``children``, ``male``,
# and who is a ``siblingof``.

train.facts

# %%
# Our aim is to learn about what a "*father*" is in terms of the facts we have available.
# This process is usually called *induction,* and is often portrayed as "learning a
# definition of an object."

from srlearn.rdn import BoostedRDNClassifier
from srlearn import Background

bk = Background(
    modes=[
        "male(+name).",
        "father(+name,+name).",
        "childof(+name,+name).",
        "siblingof(+name,+name)."
    ],
    number_of_clauses=8,
)

clf = BoostedRDNClassifier(
    background=bk,
    target="father",
    node_size=1,
    n_estimators=5,
)

clf.fit(train)

# %%
# It's important to check whether we actually learn something useful.
# We'll visually inspect the relational regression trees to see what
# they learned.

from srlearn.plotting import plot_digraph
from srlearn.plotting import export_digraph

plot_digraph(export_digraph(clf, 0), format="html")

# %%
# There is some variance between runs, but in the concept that the
# trees pick up on is roughly that "*A father has a child and is male.*"

plot_digraph(export_digraph(clf, 1), format="html")

# %%
# Here the data is fairly complete, and the concept that "*A father has a
# child and is male*" seems sufficient for the purposes of this data.
# Let's apply our learned model to the test data, which includes facts
# about characters from Jane Austen's *Pride and Prejudice.*

predictions = clf.predict_proba(test)

print("{:<35} {}".format("Predicate", "Probability of being True"), "\n", "-" * 60)
for predicate, prob in zip(test.pos + test.neg, predictions):
    print("{:<35} {:.2f}".format(predicate, prob))

# %%
# The confidence might be a little low, which is a good excuse to mention
# one of the hyperparameters. "Node Size," or ``node_size`` corresponds to
# the maximum number of predicates that can be used as a split in the
# dependency network. We set ``node_size=1`` above for demonstration, but the
# concept that seems to be learned: ``father(A, B) = [childof(B, A), male(B)]``
# is of size 2.
#
# We might be able to learn a better model by taking this new information
# into account:

bk = Background(
    modes=[
        "male(+name).",
        "father(+name,+name).",
        "childof(+name,+name).",
        "siblingof(+name,+name)."
    ],
    number_of_clauses=8,
)

clf = BoostedRDNClassifier(
    background=bk,
    target="father",
    node_size=2,                # <--- Changed from 1 to 2
    n_estimators=5,
)

clf.fit(train)

plot_digraph(export_digraph(clf, 0), format="html")

# %%
# This seems to be much more stable, which should also be reflected in the
# probabilities assigned on test examples.

predictions = clf.predict_proba(test)

print("{:<35} {}".format("Predicate", "Probability of being True"), "\n", "-" * 60)
for predicate, prob in zip(test.pos + test.neg, predictions):
    print("{:<35} {:.2f}".format(predicate, prob))
