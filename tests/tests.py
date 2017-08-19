import os
import sys
import unittest

# Test that train_pos, (etc) are lists of strings.
# Test that each string is in predicate-logic notation.
# Check to make sure there are no references that are not present in the modes object.
# Check that train_bk and test_bk exist, and both point to background.txt

sys.path.append('./boostsrl')
import boostsrl

class sample_data_functions:

    def sample(self, example):
        '''Calls the example_data function from boostsrl.py'''
        return boostsrl.example_data(example)
    
class background_functions:

    def build_background_1(self):
        bk = ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).']
        background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)
        return background

class train_functions:

    def test_training_1(self):
        bk = ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).']
        background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)
        train_pos = boostsrl.example_data('train_pos')
        train_neg = boostsrl.example_data('train_neg')
        train_facts = boostsrl.example_data('train_facts')
        model = boostsrl.train(background, train_pos, train_neg, train_facts)
        return model

class test_with_model_functions:

    def test_testing_1(self):
        bk = boostsrl.example_data('background')
        background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)
        train_pos = boostsrl.example_data('train_pos')
        train_neg = boostsrl.example_data('train_neg')
        train_facts = boostsrl.example_data('train_facts')
        
        test_pos = boostsrl.example_data('test_pos')
        test_neg = boostsrl.example_data('test_neg')
        test_facts = boostsrl.example_data('test_facts')
        
        model = boostsrl.train(background, train_pos, train_neg, train_facts)
        results = boostsrl.test(model, test_pos, test_neg, test_facts)
        return results

class MyTest(unittest.TestCase):

    def test_background_setup_1(self):
        '''Ensure that the background returned by boostsrl.modes sets variables correctly.'''
        f = background_functions()
        background = f.build_background_1()
        # These background values should be bound since they are set with the build_background function.
        self.assertEqual(background.target, 'cancer')
        self.assertEqual(background.useStdLogicVariables, True)
        self.assertEqual(background.treeDepth, 4)
        self.assertEqual(background.nodeSize, 2)
        self.assertEqual(background.numOfClauses, 8)
        # These background values should remain as the default values since they are not referenced.
        self.assertEqual(background.loadAllLibraries, False)
        self.assertEqual(background.usePrologVariables, False)
        self.assertEqual(background.maxTreeDepth, None)
        self.assertEqual(background.numOfCycles, None)
        self.assertEqual(background.minLCTrees, None)
        self.assertEqual(background.incrLCTrees, None)
        self.assertEqual(background.recursion, False)
        self.assertEqual(background.lineSearch, False)
        self.assertEqual(background.resampleNegs, False)

    def test_data_sampling(self):
        '''Ensures that example_data function is returning the proper results.'''
        f = sample_data_functions()
        self.assertEqual(f.sample('background'), ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).'])
        self.assertEqual(f.sample('train_pos'), ['cancer(Alice).', 'cancer(Bob).', 'cancer(Chuck).', 'cancer(Fred).'])
        self.assertEqual(f.sample('train_neg'), ['cancer(Dan).','cancer(Earl).'])
        self.assertEqual(f.sample('train_facts'), ['friends(Alice, Bob).', 'friends(Alice, Fred).', 'friends(Chuck, Bob).', 'friends(Chuck, Fred).', 'friends(Dan, Bob).', 'friends(Earl, Bob).','friends(Bob, Alice).', 'friends(Fred, Alice).', 'friends(Bob, Chuck).', 'friends(Fred, Chuck).', 'friends(Bob, Dan).', 'friends(Bob, Earl).', 'smokes(Alice).', 'smokes(Chuck).', 'smokes(Bob).'])
        self.assertEqual(f.sample('test_pos'), ['cancer(Zod).', 'cancer(Xena).', 'cancer(Yoda).'])
        self.assertEqual(f.sample('test_neg'), ['cancer(Voldemort).', 'cancer(Watson).'])
        self.assertEqual(f.sample('test_facts'), ['friends(Zod, Xena).', 'friends(Xena, Watson).', 'friends(Watson, Voldemort).', 'friends(Voldemort, Yoda).', 'friends(Yoda, Zod).', 'friends(Xena, Zod).', 'friends(Watson, Xena).', 'friends(Voldemort, Watson).', 'friends(Yoda, Voldemort).', 'friends(Zod, Yoda).', 'smokes(Zod).', 'smokes(Xena).', 'smokes(Yoda).'])

    def test_background_setup_1_relevant(self):
        '''Ensure that the correct relevant information is created from the background variables.'''
        f = background_functions()
        background = f.build_background_1()
        self.assertTrue(['numOfClauses', 8] in background.relevant)
        self.assertTrue(['target', 'cancer'] in background.relevant)
        self.assertTrue(['useStdLogicVariables', True] in background.relevant)
        self.assertTrue(['treeDepth', 4] in background.relevant)
        self.assertTrue(['nodeSize', 2] in background.relevant)
        
    def test_background_setup_1_background_knowledge(self):
        '''Ensure that the background_knowledge list is created properly'''
        f = background_functions()
        background = f.build_background_1()
        self.assertTrue('setParam: numOfClauses=8.' in background.background_knowledge)
        self.assertTrue('useStdLogicVariables: true.' in background.background_knowledge)
        self.assertTrue('setParam: treeDepth=4.' in background.background_knowledge)
        self.assertTrue('setParam: nodeSize=2.' in background.background_knowledge)
        self.assertTrue('mode: friends(+Person, -Person).' in background.background_knowledge)
        self.assertTrue('mode: friends(-Person, +Person).' in background.background_knowledge)
        self.assertTrue('mode: smokes(+Person).' in background.background_knowledge)
        self.assertTrue('mode: cancer(+Person).' in background.background_knowledge)

    def test_background_setup_1_file_exists(self):
        '''Ensure that the background file is actually created.'''
        f = background_functions()
        background = f.build_background_1()
        self.assertTrue(os.path.isfile('boostsrl/background.txt'))

    def test_background_setup_1_matches_background_knowledge(self):
        '''Open the background.txt up and make sure it matches what was written into it.'''
        f = background_functions()
        background = f.build_background_1()
        with open('boostsrl/background.txt', 'r') as f:
            self.assertTrue(f.read().splitlines() == background.background_knowledge)

    def test_boostsrl_training(self):
        '''Check assignment and outcomes of BoostSRL training.'''
        f = train_functions()
        model = f.test_training_1()
        self.assertEqual(model.target, 'cancer')
        self.assertEqual(model.advice, False)
        self.assertEqual(model.softm, False)
        self.assertEqual(model.alpha, 0.5)
        self.assertEqual(model.beta, -2)
        self.assertEqual(model.trees, 10)

        # Do the trees exist? Does 'cancer' appear in tree0?
        self.assertTrue(isinstance(model.tree(0), str))
        self.assertTrue(isinstance(model.tree(1), str))
        self.assertTrue(isinstance(model.tree(2), str))
        self.assertTrue(isinstance(model.tree(3), str))
        self.assertTrue(isinstance(model.tree(4), str))
        self.assertTrue(isinstance(model.tree(5), str))
        self.assertTrue(isinstance(model.tree(6), str))
        self.assertTrue(isinstance(model.tree(7), str))
        self.assertTrue(isinstance(model.tree(8), str))
        self.assertTrue(isinstance(model.tree(9), str))
        self.assertTrue('cancer' in model.tree(0))

        # Does training time return either a float or an int?
        self.assertTrue(isinstance(model.traintime(), float))
        self.assertEqual(model.training_time_to_float(['1', 'milliseconds']), 0.001)
        self.assertEqual(model.training_time_to_float(['1', 'days', '981', 'milliseconds']), 86400.981)
        self.assertEqual(model.training_time_to_float(['2', 'hours', '1', 'minutes', '25', 'seconds', '120', 'milliseconds']), 7285.12)

    def test_boostsrl_testing(self):
        '''Run the entire training/testing pipeline to ensure testing works properly.'''
        f = test_with_model_functions()
        results = f.test_testing_1()

        # Check the contents of the results summary.
        summary = results.summarize_results()
        self.assertTrue('AUC ROC' in summary)
        self.assertTrue('AUC PR' in summary)
        self.assertTrue('CLL' in summary)
        self.assertTrue('Precision' in summary)
        self.assertTrue('Recall' in summary)
        self.assertTrue('F1' in summary)

        # Check the contents of the inference results.
        inference_dict = results.inference_results()
        self.assertTrue('cancer(Zod)' in inference_dict)
        self.assertTrue('!cancer(Watson)' in inference_dict)
        self.assertTrue('cancer(Xena)' in inference_dict)
        self.assertTrue('!cancer(Voldemort)' in inference_dict)
        self.assertTrue('cancer(Yoda)' in inference_dict)

if __name__ == '__main__':
    unittest.main()
