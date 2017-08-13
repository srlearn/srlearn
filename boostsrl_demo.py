'''Introduction to using the boostsrl python wrappers.'''

from boostsrl import boostsrl

bk = [
    'friends(+Person, -Person).',
    'friends(-Person, +Person).',
    'smokes(+Person).',
    'cancer(+Person).'
]

bridgers = ['friends/2']

precomputes = {
    'num_of_smoking_friends(+Person, #Number).': 'num_of_smoking_friends(x, n) :- friends(x, y), countUniqueBindings((friends(x,z)^smokes(z)), n).'
}

train_pos = ['cancer(Alice).', 'cancer(Bob).', 'cancer(Chuck).', 'cancer(Fred).']
train_neg = ['cancer(Dan).','cancer(Earl).']
train_facts = ['friends(Alice, Bob).', 'friends(Alice, Fred).', 'friends(Chuck, Bob).', 'friends(Chuck, Fred).', 'friends(Dan, Bob).', 'friends(Earl, Bob).','friends(Bob, Alice).', 'friends(Fred, Alice).', 'friends(Bob, Chuck).', 'friends(Fred, Chuck).', 'friends(Bob, Dan).', 'friends(Bob, Earl).', 'smokes(Alice).', 'smokes(Chuck).', 'smokes(Bob).' ]
test_pos = ['cancer(Zod).', 'cancer(Xena).', 'cancer(Yoda).']
test_neg = ['cancer(Voldemort).', 'cancer(Watson).']
test_facts = ['friends(Zod, Xena).', 'friends(Xena, Watson).', 'friends(Watson, Voldemort).', 'friends(Voldemort, Yoda).', 'friends(Yoda, Zod).', 'friends(Xena, Zod).', 'friends(Watson, Xena).', 'friends(Voldemort, Watson).', 'friends(Yoda, Voldemort).', 'friends(Zod, Yoda).', 'smokes(Zod).', 'smokes(Xena).', 'smokes(Yoda).']

background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)
#model = boostsrl.train('cancer', train_pos, train_neg, train_facts)
model = boostsrl.train(background, train_pos, train_neg, train_facts)
test = boostsrl.test(model, test_pos, test_neg, test_facts)

print(test.summarize_results())
print(test.inference_results())
