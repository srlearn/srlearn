'''

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

    def write_to_file(self, content, path):
        with open(path, 'w') as f:
            f.write()

    def Train(self):
        # Begin by writing the contents of each (pos/neg/facts) to respectives files that will be used in a few.
        self.write_to_file(self.train_pos, 'boostsrl-src/train/train_pos.txt')
        self.write_to_file(self.train_neg, 'boostsrl-src/train/train_neg.txt')
        self.write_to_file(self.train_facts, 'boostsrl-src/train/train_facts.txt')
        
        CALL = 'java -jar v1-0.jar -l -train boostsrl-src/train/ '

class boostsrl_test(object):

    # BoostSRL Testing method.

    def __init__(self, test_pos, test_neg, test_facts, trees=10):
        self.trees = trees

    
