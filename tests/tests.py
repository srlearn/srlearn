# Tests for CI-practice
import os
import sys
import unittest

class BasicFunctions:

    def function(self, x):
        return x + 1

    def function2(self, x):
        return [1,2,3]

class MyTest(unittest.TestCase):

    def test_assert_true(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    
    def test_functions_above(self):
        f = BasicFunctions()
        self.assertEqual(f.function(3),4)
        self.assertEqual(f.function2(5),[1,2,3])

if __name__ == '__main__':
    unittest.main()
