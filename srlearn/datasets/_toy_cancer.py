# Copyright © 2017-2020 Alexander L. Hayes

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


ToyCancer = Bunch(
    train=Database(),
    test=Database(),
)

ToyCancer.train.modes = [
    "friends(+Person,-Person).",
    "friends(-Person,+Person).",
    "smokes(+Person).",
    "cancer(+Person).",
]
ToyCancer.train.pos = ["cancer(Alice).", "cancer(Bob).", "cancer(Chuck).", "cancer(Fred)."]
ToyCancer.train.neg = ["cancer(Dan).", "cancer(Earl)."]
ToyCancer.train.facts = [
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

ToyCancer.test.modes = [
    "friends(+Person,-Person).",
    "friends(-Person,+Person).",
    "smokes(+Person).",
    "cancer(+Person).",
]
ToyCancer.test.pos = ["cancer(Zod).", "cancer(Xena).", "cancer(Yoda)."]
ToyCancer.test.neg = ["cancer(Voldemort).", "cancer(Watson)."]
ToyCancer.test.facts = [
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
