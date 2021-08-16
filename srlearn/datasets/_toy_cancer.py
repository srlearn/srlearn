# Copyright © 2017-2021 Alexander L. Hayes

"""
Toy Cancer Data Set

Examples
--------

>>> from srlearn.datasets import load_toy_cancer
>>> train, test = load_toy_cancer()
>>> train.pos
['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
"""

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
    >>> train, test = load_toy_cancer()
    >>> train
    Positive Examples:
    ['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
    Negative Examples:
    ['cancer(dan).', 'cancer(earl).']
    Facts:
    ['friends(alice,bob).', 'friends(alice,fred).', ..., 'smokes(bob).']

    """

    # toy_cancer = Bunch(train=Database(), test=Database(),)

    train = Database()
    test = Database()

    train.modes = [
        "friends(+Person,-Person).",
        "friends(-Person,+Person).",
        "smokes(+Person).",
        "cancer(+Person).",
    ]
    train.pos = [
        "cancer(alice).",
        "cancer(bob).",
        "cancer(chuck).",
        "cancer(fred).",
    ]
    train.neg = ["cancer(dan).", "cancer(earl)."]
    train.facts = [
        "friends(alice,bob).",
        "friends(alice,fred).",
        "friends(chuck,bob).",
        "friends(chuck,fred).",
        "friends(dan,bob).",
        "friends(earl,bob).",
        "friends(bob,alice).",
        "friends(fred,alice).",
        "friends(bob,chuck).",
        "friends(fred,chuck).",
        "friends(bob,dan).",
        "friends(bob,earl).",
        "smokes(alice).",
        "smokes(chuck).",
        "smokes(bob).",
    ]

    test.modes = [
        "friends(+Person,-Person).",
        "friends(-Person,+Person).",
        "smokes(+Person).",
        "cancer(+Person).",
    ]
    test.pos = ["cancer(zod).", "cancer(xena).", "cancer(yoda)."]
    test.neg = ["cancer(voldemort).", "cancer(watson)."]
    test.facts = [
        "friends(zod,xena).",
        "friends(xena,watson).",
        "friends(watson,voldemort).",
        "friends(voldemort,yoda).",
        "friends(yoda,zod).",
        "friends(xena,zod).",
        "friends(watson,xena).",
        "friends(voldemort,watson).",
        "friends(yoda,voldemort).",
        "friends(zod,yoda).",
        "smokes(zod).",
        "smokes(xena).",
        "smokes(yoda).",
    ]

    return train, test
