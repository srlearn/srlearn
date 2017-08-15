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

class MyTest(unittest.TestCase):

    def test_background_setup_1(self):
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

if __name__ == '__main__':
    unittest.main()
