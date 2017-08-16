# Tests for CI-practice
import os
import sys
import unittest

# Path problems tend to be caused depending on which directory tests begin in.
try:
    sys.path.insert(0, '../boostsrl/')
    import boostsrl
except:
    sys.path.insert(0, './boostsrl/')
    import boostsrl

class background_functions:

    def build_background_1(self):
        bk = ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).']
        background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)
        return background

    def build_background_2(self):
        bk = ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).']
        background = boostsrl.modes(bk, 'cancer')
        return background

class MyTest(unittest.TestCase):

    def test_background_setup_1(self):
        '''Ensure that the background returned by boostsrl.modes sets variables correctly.'''
        f = background_functions()
        background = f.build_background_1()
        #print(background.relevant)
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
        
    def test_background_setup_2(self):
        '''Ensure that the file created by boostsrl.modes is created properly'''
        pass
        '''
        f = background_functions()
        background = f.build_background_2()
        self.assertEqual(background.target, 'cancer')
        '''

if __name__ == '__main__':
    unittest.main()
