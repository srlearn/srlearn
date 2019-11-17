"""
===========================
Family Relationships Domain
===========================

This example motivates learning about family relationships from examples of *Harry Potter* characters, then applies
those rules to characters from *Pride and Prejudice*.
"""

from srlearn.rdn import BoostedRDN
from srlearn import Background
from srlearn import Database

train_db = Database()
train_db.pos = [
    "father(harrypotter,jamespotter).",
    "father(dracomalfoy,luciusmalfoy).",
    "father(ginnyweasley,arthurweasley).",
    "father(ronweasley,arthurweasley).",
    "father(fredweasley,arthurweasley).",
]
train_db.neg = [
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
train_db.facts = [
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

bk = Background(
    modes=[
        "male(+name).",
        "father(+name,+name).",
        "childof(+name,+name).",
        "siblingof(+name,+name)."
    ],
    number_of_clauses=8,
    use_prolog_variables=True,
)

clf = BoostedRDN(
    background=bk,
    target="father",
    n_estimators=5,
)

clf.fit(train_db)

test_db = Database()

test_db.pos = [
    "father(elizabeth,mrbennet).",
    "father(jane,mrbennet).",
    "father(charlotte,mrlucas).",
]

test_db.neg = [
    "father(charlotte,mrsbennet).",
    "father(jane,mrlucas).",
    "father(mrsbennet,mrbennet).",
    "father(jane,elizabeth).",
]

test_db.facts = [
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

print(clf.predict_proba(test_db))
