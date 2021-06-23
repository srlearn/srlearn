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
        "cancer(Alice).",
        "cancer(Bob).",
        "cancer(Chuck).",
        "cancer(Fred).",
    ]
    toy_cancer.train.neg = ["cancer(Dan).", "cancer(Earl)."]
    toy_cancer.train.facts = [
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

    toy_cancer.test.modes = [
        "friends(+Person,-Person).",
        "friends(-Person,+Person).",
        "smokes(+Person).",
        "cancer(+Person).",
    ]
    toy_cancer.test.pos = ["cancer(Zod).", "cancer(Xena).", "cancer(Yoda)."]
    toy_cancer.test.neg = ["cancer(Voldemort).", "cancer(Watson)."]
    toy_cancer.test.facts = [
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

    return toy_cancer
