# Copyright © 2017-2020 Alexander L. Hayes

"""
Toy Father Data Set

Examples
--------

>>> from srlearn.datasets import ToyFather
>>> print(ToyFather.train.pos)
['father(harrypotter,jamespotter).', ... , 'father(fredweasley,arthurweasley).']
"""

from sklearn.utils import Bunch
from ..database import Database


ToyFather = Bunch(
    train=Database(),
    test=Database(),
)

ToyFather.train.modes = [
    "male(+name).",
    "father(+name,+name).",
    "childof(+name,+name).",
    "siblingof(+name,+name)."
]

ToyFather.train.pos = [
    "father(harrypotter,jamespotter).",
    "father(dracomalfoy,luciusmalfoy).",
    "father(ginnyweasley,arthurweasley).",
    "father(ronweasley,arthurweasley).",
    "father(fredweasley,arthurweasley).",
]
ToyFather.train.neg = [
    "father(harrypotter,mrgranger).",
    "father(harrypotter,mrsgranger).",
    "father(georgeweasley,xenophiliuslovegood).",
    "father(luciusmalfoy,xenophiliuslovegood).",
    "father(harrypotter,hagrid).",
    "father(ginnyweasley,dracomalfoy).",
    "father(hagrid,dracomalfoy).",
    "father(hagrid,dumbledore).",
    "father(lunalovegood,dumbledore).",
    "father(hedwig,narcissamalfoy).",
    "father(hedwig,lunalovegood).",
    "father(ronweasley,hedwig).",
    "father(mollyweasley,cygnusblack).",
    "father(arthurweasley,mollyweasley).",
    "father(georgeweasley,fredweasley).",
    "father(fredweasley,georgeweasley).",
    "father(ronweasley,georgeweasley).",
    "father(ronweasley,hermione).",
    "father(dracomalfoy,narcissamalfoy).",
    "father(hermione,mrsgranger).",
    "father(ginnyweasley,mollyweasley).",
]
ToyFather.train.facts = [
    "male(mrgranger).",
    "male(jamespotter).",
    "male(harrypotter).",
    "male(luciusmalfoy).",
    "male(dracomalfoy).",
    "male(arthurweasley).",
    "male(ronweasley).",
    "male(fredweasley).",
    "male(georgeweasley).",
    "male(hagrid).",
    "male(dumbledore).",
    "male(xenophiliuslovegood).",
    "male(cygnusblack).",
    "siblingof(ronweasley,fredweasley).",
    "siblingof(ronweasley,georgeweasley).",
    "siblingof(ronweasley,ginnyweasley).",
    "siblingof(fredweasley,ronweasley).",
    "siblingof(fredweasley,georgeweasley).",
    "siblingof(fredweasley,ginnyweasley).",
    "siblingof(georgeweasley,ronweasley).",
    "siblingof(georgeweasley,fredweasley).",
    "siblingof(georgeweasley,ginnyweasley).",
    "siblingof(ginnyweasley,ronweasley).",
    "siblingof(ginnyweasley,fredweasley).",
    "siblingof(ginnyweasley,georgeweasley).",
    "childof(mrgranger,hermione).",
    "childof(mrsgranger,hermione).",
    "childof(jamespotter,harrypotter).",
    "childof(lilypotter,harrypotter).",
    "childof(luciusmalfoy,dracomalfoy).",
    "childof(narcissamalfoy,dracomalfoy).",
    "childof(arthurweasley,ronweasley).",
    "childof(mollyweasley,ronweasley).",
    "childof(arthurweasley,fredweasley).",
    "childof(mollyweasley,fredweasley).",
    "childof(arthurweasley,georgeweasley).",
    "childof(mollyweasley,georgeweasley).",
    "childof(arthurweasley,ginnyweasley).",
    "childof(mollyweasley,ginnyweasley).",
    "childof(xenophiliuslovegood,lunalovegood).",
    "childof(cygnusblack,narcissamalfoy).",
]

ToyFather.test.modes = [
    "male(+name).",
    "father(+name,+name).",
    "childof(+name,+name).",
    "siblingof(+name,+name)."
]

ToyFather.test.pos = [
    "father(elizabeth,mrbennet).",
    "father(jane,mrbennet).",
    "father(charlotte,mrlucas).",
]

ToyFather.test.neg = [
    "father(charlotte,mrsbennet).",
    "father(jane,mrlucas).",
    "father(mrsbennet,mrbennet).",
    "father(jane,elizabeth).",
]

ToyFather.test.facts = [
    "male(mrbennet).",
    "male(mrlucas).",
    "male(darcy).",
    "childof(mrbennet,elizabeth).",
    "childof(mrsbennet,elizabeth).",
    "childof(mrbennet,jane).",
    "childof(mrsbennet,jane).",
    "childof(mrlucas,charlotte).",
    "childof(mrslucas,charlotte).",
    "siblingof(jane,elizabeth).",
    "siblingof(elizabeth,jane).",
]
