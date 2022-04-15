# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
A BoostSRL database with the "Toy-Cancer" dataset.

Importing this module makes ``example_data.train`` and ``example_data.test`` available
in the namespace.

Examples
--------

>>> from srlearn import example_data
>>> print(example_data.train)
Positive Examples:
['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
Negative Examples:
['cancer(dan).', 'cancer(earl).']
Facts:
['friends(alice, bob).', 'friends(alice, fred).', ..., 'smokes(bob).']

Ellipsis added to the facts for easier reading.

>>> from srlearn import example_data
>>> print(example_data.test)
Positive Examples:
['cancer(zod).', 'cancer(xena).', 'cancer(yoda).']
Negative Examples:
['cancer(voldemort).', 'cancer(watson).']
Facts:
['friends(zod, xena).', 'friends(xena, watson).', ..., 'smokes(yoda).']

"""

import warnings
from .database import Database

warnings.simplefilter("default")
warnings.warn("`example_data` moved to `srlearn.datasets.load_toy_cancer`, to be removed in 0.6")

# pylint: disable=invalid-name
train = Database()
test = Database()

train.modes = [
    "friends(+person,-person).",
    "friends(-person,+person).",
    "smokes(+person).",
    "cancer(+person).",
]
train.pos = ["cancer(alice).", "cancer(bob).", "cancer(chuck).", "cancer(fred)."]
train.neg = ["cancer(dan).", "cancer(earl)."]
train.facts = [
    "friends(alice, bob).",
    "friends(alice, fred).",
    "friends(chuck, bob).",
    "friends(chuck, fred).",
    "friends(dan, bob).",
    "friends(earl, bob).",
    "friends(bob, alice).",
    "friends(fred, alice).",
    "friends(bob, chuck).",
    "friends(fred, chuck).",
    "friends(bob, dan).",
    "friends(bob, earl).",
    "smokes(alice).",
    "smokes(chuck).",
    "smokes(bob).",
]

test.modes = [
    "friends(+person,-person).",
    "friends(-person,+person).",
    "smokes(+person).",
    "cancer(+person).",
]
test.pos = ["cancer(zod).", "cancer(xena).", "cancer(yoda)."]
test.neg = ["cancer(voldemort).", "cancer(watson)."]
test.facts = [
    "friends(zod, xena).",
    "friends(xena, watson).",
    "friends(watson, voldemort).",
    "friends(voldemort, yoda).",
    "friends(yoda, zod).",
    "friends(xena, zod).",
    "friends(watson, xena).",
    "friends(voldemort, watson).",
    "friends(yoda, voldemort).",
    "friends(zod, yoda).",
    "smokes(zod).",
    "smokes(xena).",
    "smokes(yoda).",
]
