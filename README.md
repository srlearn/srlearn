<p align="center">
   <img src="media/box2.png" />
</p>

---

| License | Build Status |
| --- | --- |
| [![][license img]][license] | [![Build Status](https://travis-ci.org/batflyer/boostsrl-python-package.svg?branch=master)](https://travis-ci.org/batflyer/boostsrl-python-package) |

---


**BoostSRL** (Boosting for Statistical Relational Learning) is a gradient-boosting based approach to learning different types of SRL models. As with the standard gradient-boosting approach, our approach turns the model learning problem to learning a sequence of regression models. The key difference to the standard approaches is that we learn relational regression models i.e., regression models that operate on relational data. We assume the data in a predicate logic format and the output are essentially first-order regression trees where the inner nodes contain conjunctions of logical predicates. For more details on the models and the algorithm, we refer to our book on this topic.

Sriraam Natarajan, Tushar Khot, Kristian Kersting and Jude Shavlik, Boosted Statistical Relational Learners: From Benchmarks to Data-Driven Medicine . SpringerBriefs in Computer Science, ISBN: 978-3-319-13643-1, 2015 

## Installation

Python 2.7:

```bash
git clone https://github.com/batflyer/boostsrl-python-package.git
```

---

### Usage

```python
>>> from boostsrl import boostsrl

'''Step 1: Background Knowledge'''

# Sample data is built in from the 'Toy Cancer' Dataset, retrieve it with sample_data
>>> bk = boostsrl.sample_data('background')

# Create the background knowledge or 'Modes,' where 'cancer' is the target we want to predict.
>>> background = boostsrl.modes(bk, 'cancer', useStdLogicVariables=True, treeDepth=4, nodeSize=2, numOfClauses=8)

'''Step 2: Training a Model'''

# Retrieve the positives, negatives, and facts.
>>> train_pos = boostsrl.sample_data('train_pos')
>>> train_neg = boostsrl.sample_data('train_neg')
>>> train_facts = boostsrl.sample_data('train_facts')

# Train a model using this data:
>>> model = boostsrl.train('cancer', train_pos, train_neg, train_facts)

'''Step 3: Test Model on New Data'''

# Retrieve the positives, negatives, and facts.
>>> test_pos = boostsrl.sample_data('test_pos')
>>> test_neg = boostsrl.sample_data('test_neg')
>>> test_facts = boostsrl.sample_data('test_facts')

# Test the data
>>> results = boostsrl.test(model, test_pos, test_neg, test_facts)

'''Step 4: Observe Performance'''

# To see the overall performance of the model on test data:
>>> test.summarize_results()
{'CLL': '-0.223184', 'F1': '1.000000', 'Recall': '1.000000', 'Precision': '1.000000,0.500', 'AUC ROC': '1.000000', 'AUC PR': '1.000000'}

# To see probabilities for individual test examples:
>>> test.inference_results()
{'!cancer(Watson)': 0.6924179024024251, 'cancer(Xena)': 0.8807961917687174, '!cancer(Voldemort)': 0.6924179024024251, 'cancer(Yoda)': 0.8807961917687174, 'cancer(Zod)': 0.8807961917687174}

```

### Saving a model (not implemented yet)

```python
>>> from boostsrl import boostsrl
>>> boostsrl.save_model('toy_cancer')
```

[license]:license.txt
[license img]:https://img.shields.io/aur/license/yaourt.svg