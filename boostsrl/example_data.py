# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
Populate a BoostSRL database with the "Toy-Cancer" dataset.

Importing this module makes a ``train`` and ``test`` database available.

Examples
--------

.. code-block:: python

    >>> from boostsrl import example_data
    >>> print(example_data.train)
    Positive Examples:
    ['cancer(Alice).', 'cancer(Bob).', 'cancer(Chuck).', 'cancer(Fred).']
    Negative Examples:
    ['cancer(Dan).', 'cancer(Earl).']
    Facts:
    ['friends(Alice, Bob).', 'friends(Alice, Fred).', ..., 'smokes(Bob).']

Ellipsis added to the facts for easier reading.

.. code-block:: python

    >>> from boostsrl import example_data
    >>> print(example_data.test)
    Positive Examples:
    ['cancer(Zod).', 'cancer(Xena).', 'cancer(Yoda).']
    Negative Examples:
    ['cancer(Voldemort).', 'cancer(Watson).']
    Facts:
    ['friends(Zod, Xena).', 'friends(Xena, Watson).', ..., 'smokes(Yoda).']

"""

from .database import database

train = database()
test = database()

train.background = [
    "friends(+Person,-Person).",
    "friends(-Person,+Person).",
    "smokes(+Person).",
    "cancer(+Person).",
]
train.pos = ["cancer(Alice).", "cancer(Bob).", "cancer(Chuck).", "cancer(Fred)."]
train.neg = ["cancer(Dan).", "cancer(Earl)."]
train.facts = [
    "friends(Alice, Bob).",
    "friends(Alice, Fred).",
    "friends(Chuck, Bob).",
    "friends(Chuck, Fred).",
    "friends(Dan, Bob).",
    "friends(Earl, Bob).",
    "friends(Bob, Alice).",
    "friends(Fred, Alice).",
    "friends(Bob, Chuck).",
    "friends(Fred, Chuck).",
    "friends(Bob, Dan).",
    "friends(Bob, Earl).",
    "smokes(Alice).",
    "smokes(Chuck).",
    "smokes(Bob).",
]

test.background = [
    "friends(+Person,-Person).",
    "friends(-Person,+Person).",
    "smokes(+Person).",
    "cancer(+Person).",
]
test.pos = ["cancer(Zod).", "cancer(Xena).", "cancer(Yoda)."]
test.neg = ["cancer(Voldemort).", "cancer(Watson)."]
test.facts = [
    "friends(Zod, Xena).",
    "friends(Xena, Watson).",
    "friends(Watson, Voldemort).",
    "friends(Voldemort, Yoda).",
    "friends(Yoda, Zod).",
    "friends(Xena, Zod).",
    "friends(Watson, Xena).",
    "friends(Voldemort, Watson).",
    "friends(Yoda, Voldemort).",
    "friends(Zod, Yoda).",
    "smokes(Zod).",
    "smokes(Xena).",
    "smokes(Yoda).",
]
