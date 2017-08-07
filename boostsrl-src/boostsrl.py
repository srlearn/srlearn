'''
   Python package that makes it easier to write code that uses the BoostSRL java package, without having
   to create the data then run the jar manually.

   Name:         boostsrl.py
   Author:       Alexander L. Hayes
   Updated:      August 5, 2017
   License:      GPLv3
'''

from __future__ import print_function
import os
import re
import sys

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

def call_process(call):
    p = subprocess.Popen(call, shell=True)
    os.waitpid(p.pid, 0)

class modes(object):

    def __init__(self):
        self.loadAllLibraries = False
        self.usePrologVariables = False
        # Note to self: check further into the difference between treeDepth and maxTreeDepth
        self.maxTreeDepth = 3
        self.treeDepth = 3
        self.nodeSize = 1
        self.numOfClauses = 8
        self.numOfCycles = 8
        self.minLCTrees = 5
        self.incrLCTrees = 5
        self.recursion = False
        self.lineSearch = False
        self.resampleNegs = False
        self.queryPred = 'advisedby/2'

    def check_exists(self, predicate):
        pass

    def infer_modes(self, background):
        pass
        
class boostsrl_train(object):

    # BoostSRL Training method.

    def __init__(self, target, train_pos, train_neg, train_facts, advice=False, softm=False, alpha=0.5, beta=-2, trees=10):
        self.target = target
        self.train_pos = train_pos
        self.train_neg = train_neg
        self.train_facts = train_facts
        self.advice = advice
        self.softm = softm
        self.alpha = alpha
        self.beta = beta
        self.trees = trees
        self.TRAINED = 0

    def write_to_file(self, content, path):
        '''Takes a list (content) and a path/file (path) and writes each line of the list to the file location.'''
        with open(path, 'w') as f:
            for line in content:
                f.write(line)
        f.close()

    def test_cases(self):
        # test that train_pos, train_neg (etc.) are lists of strings
        # tests that each string is in predicate-logic notation.
        # check to make sure there are no references that are not present in the modes object.
        pass
        
    def Train(self):
        # Begin by writing the contents of each (pos/neg/facts) to respectives files that will be used in a few.
        self.write_to_file(self.train_pos, 'boostsrl-src/train/train_pos.txt')
        self.write_to_file(self.train_neg, 'boostsrl-src/train/train_neg.txt')
        self.write_to_file(self.train_facts, 'boostsrl-src/train/train_facts.txt')
        
        CALL = 'java -jar v1-0.jar -l -train boostsrl-src/train/ -target ' + self.target + ' -trees ' + self.trees + ' 2>&1'
        call_process(CALL)
        self.TRAINED = 1

    def Tree(self, treenumber):
        # Tree number is between 0 and the self.trees.
        if (treenumber > (self.trees - 1)) or (self.TRAINED == 0):
            raise Exception('Tried to find a tree that does not exist.')
        else:
            # read the tree from the file produced by boostsrl
            pass

class boostsrl_test(object):

    # BoostSRL Testing method.

    def __init__(self, test_pos, test_neg, test_facts, trees=10):
        self.trees = trees

        
