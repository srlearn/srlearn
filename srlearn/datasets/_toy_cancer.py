# Copyright © 2017-2021 Alexander L. Hayes

"""
Toy Cancer Data Set

Examples
--------

>>> from srlearn.datasets import ToyCancer
>>> print(ToyCancer.train.pos)
['cancer(Alice).', 'cancer(Bob).', 'cancer(Chuck).', 'cancer(Fred).']
"""

from sklearn.utils import Bunch
from ..database import Database


def load_toy_cancer():
    """Load and return the Toy Cancer dataset.

    Returns
    -------
    toy_cancer : Bunch
        Bunch contains `train` and  `test` Database objects.
    
    Examples
    --------

    >>> from srlearn.datasets import load_toy_cancer
    >>> toy_cancer = load_toy_cancer()
    >>> print(toy_cancer.train)
    Positive Examples:
    ['cancer(Alice).', 'cancer(Bob).', 'cancer(Chuck).', 'cancer(Fred).']
    Negative Examples:
    ['cancer(Dan).', 'cancer(Earl).']
    Facts:
    ['friends(Alice, Bob).', 'friends(Alice, Fred).', ..., 'smokes(Bob).']

    """

    toy_cancer = Bunch(train=Database(), test=Database(),)

    toy_cancer.train.modes = [
        "friends(+Person,-Person).",
        "friends(-Person,+Person).",
        "smokes(+Person).",
        "cancer(+Person).",
    ]
    toy_cancer.train.pos = [
        "cancer(alice).",
        "cancer(bob).",
        "cancer(chuck).",
        "cancer(fred).",
    ]
    toy_cancer.train.neg = ["cancer(dan).", "cancer(earl)."]
    toy_cancer.train.facts = [
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

    toy_cancer.test.modes = [
        "friends(+Person,-Person).",
        "friends(-Person,+Person).",
        "smokes(+Person).",
        "cancer(+Person).",
    ]
    toy_cancer.test.pos = ["cancer(zod).", "cancer(xena).", "cancer(yoda)."]
    toy_cancer.test.neg = ["cancer(voldemort).", "cancer(watson)."]
    toy_cancer.test.facts = [
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

    return toy_cancer
