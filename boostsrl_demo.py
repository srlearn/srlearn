'''Introduction to using the boostsrl python wrappers.'''

from boostsrl import boostsrl
#import boostsrl

'''
bk = [
    'friends(+Person, -Person).',
    'friends(-Person, +Person).',
    'smokes(+Person).',
    'cancer(+Person).'
]

bridgers = [
    'friends/2'
]

precomputes = {
    'num_of_smoking_friends(+Person, #Number).': 'num_of_smoking_friends(x, n) :- friends(x, y), countUniqueBindings((friends(x,z)^smokes(z)), n).'
}

background = boostsrl.modes(bk, treeDepth=4, nodeSize=2, numOfClauses=8, useStdLogicVariables=True)

exit()
'''
train_pos = [
    'cancer(Alice).',
    'cancer(Bob).',
    'cancer(Chuck).',
    'cancer(Fred).'
]

train_neg = [
    'cancer(Dan).',
    'cancer(Earl).'
]

train_facts = [
    'friends(Alice, Bob).',
    'friends(Alice, Fred).',
    'friends(Chuck, Bob).',
    'friends(Chuck, Fred).',
    'friends(Dan, Bob).',
    'friends(Earl, Bob).',
    'friends(Bob, Alice).',
    'friends(Fred, Alice).',
    'friends(Bob, Chuck).',
    'friends(Fred, Chuck).',
    'friends(Bob, Dan).',
    'friends(Bob, Earl).',
    'smokes(Alice).',
    'smokes(Chuck).',
    'smokes(Bob).',
]

model = boostsrl.train('cancer', train_pos, train_neg, train_facts, trees=10)

test_pos = [
    'cancer(Zod).',
    'cancer(Xena).',
    'cancer(Yoda).',
]

test_neg = [
    'cancer(Voldemort)',
    'cancer(Watson)',
]

test_facts = [
    'friends(Zod, Xena).',
    'friends(Xena, Watson).',
    'friends(Watson, Voldemort).',
    'friends(Voldemort, Yoda).',
    'friends(Yoda, Zod).',
    'friends(Xena, Zod).',
    'friends(Watson, Xena).',
    'friends(Voldemort, Watson).',
    'friends(Yoda, Voldemort).',
    'friends(Zod, Yoda).',
    'smokes(Zod).',
    'smokes(Xena).',
    'smokes(Yoda).',
]

results = boostsrl.test('cancer', train_pos, train_neg, train_facts, trees=10)
