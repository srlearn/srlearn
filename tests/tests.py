# Tests for CI-practice
import os
import sys
import unittest

sys.path.insert(0, '../../boostsrl/')
import boostsrl
#from boostsrl import boostsrl

class BasicFunctions:

    def build_background(self):
        bk = ['friends(+Person, -Person).', 'friends(-Person, +Person).', 'smokes(+Person).', 'cancer(+Person).']
        model = boostsrl.model()

    def function(self, x):
        return x + 1

    def function2(self, x):
        return [1,2,3]

class MyTest(unittest.TestCase):

    def test_background_created(self):
        pass

    def test_assert_true(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    
    def test_functions_above(self):
        f = BasicFunctions()
        self.assertEqual(f.function(3),4)
        self.assertEqual(f.function2(5),[1,2,3])

if __name__ == '__main__':
    unittest.main()
