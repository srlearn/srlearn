.. title:: User Guide

##########
User Guide
##########

This guide walks through how to initialize, parametrize, and invoke the core methods.
It may be helpful to consult the `API documentation <api.html>`_ for the following modules
as you progress:

- :class:`srlearn.Database`
- :class:`srlearn.Background`
- :class:`srlearn.rdn.BoostedRDNClassifier`

Parametrize the core classes
============================

1. Looking at our Data
----------------------

This example uses the built-in example data set: "smokes-friends-cancer". We want to model
whether a person will develop cancer based on their smoking habits and their social network.

The conventional way to do machine learning might be to list the people and list their
attributes. However, for social network problems it may be difficult or impossible to
represent arbitrary social networks in a vector representation.

In order to get around this, we adopt Prolog clauses to represent our data:

>>> from srlearn.datasets import load_toy_cancer
>>> train, _ = load_toy_cancer()
>>> for predicate in train.pos:
...     print(predicate)
...
cancer(alice).
cancer(bob).
cancer(chuck).
cancer(fred).

>>> from srlearn.datasets import load_toy_cancer
>>> train, _ = load_toy_cancer()
>>> for predicate in train.facts:
...    print(predicate)
...
friends(alice,bob).
friends(alice,fred).
friends(chuck,bob).
friends(chuck,fred).
friends(dan,bob).
friends(earl,bob).
friends(bob,alice).
friends(fred,alice).
friends(bob,chuck).
friends(fred,chuck).
friends(bob,dan).
friends(bob,earl).
smokes(alice).
smokes(chuck).
smokes(bob).

Since this differs from the vector representation, this uses a :class:`srlearn.Database` object
to represent positive examples, negative examples, and facts.

1. Declaring our Backround Knowledge
------------------------------------

The :class:`srlearn.Background` object helps declare background knowledge for a domain, as well as
some parameters for model learning (this last point may seem strange, but it is designed in order
to remain compatible with how
`BoostSRL <https://starling.utdallas.edu/software/boostsrl/>`_ accepts background as input).

>>> from srlearn import Background
>>> bk = Background()
>>> print(bk)
setParam: nodeSize=2.
setParam: maxTreeDepth=3.
setParam: numOfClauses=100.
setParam: numOfCycles=100.
usePrologVariables: true.
<BLANKLINE>

This gives us a view into some of the default parameters.
However, it is missing mode declarations [1]_.

We can declare modes as a list of strings:

>>> from srlearn import Background
>>> bk = Background(
...     modes=[
...         "friends(+person,-person).",
...         "friends(-person,+person).",
...         "cancer(+person).",
...         "smokes(+person).",
...     ],
... )

A full description of modes and how they constrain the search space is beyond the scope of the discussion
here, but further reading may be warranted [1]_.

3. Initializing a Classifier
----------------------------

Here we will learn Relational Dependency Networks (RDNs) [2]_ [3]_ as classifiers for predicting if a
person in this fictional data set will develop cancer.

>>> from srlearn.rdn import BoostedRDNClassifier
>>> from srlearn import Background
>>> bk = Background(
...     modes=[
...         "friends(+person,-person).",
...         "friends(-person,+person).",
...         "cancer(+person).",
...         "smokes(+person).",
...     ],
... )
>>> clf = BoostedRDNClassifier()
>>> print(clf)
BoostedRDN(background=None, max_tree_depth=3, n_estimators=10, neg_pos_ratio=2, node_size=2, solver='BoostSRL', target='None')

This pattern should begin to look familiar if you've worked with scikit-learn before.
This classifier is built on top of
:class:`sklearn.base.BaseEstimator` and :class:`sklearn.base.ClassifierMixin`,
but there are still a few things we need to declare before invoking
:func:`srlearn.rdn.BoostedRDNClassifier.fit`.

Specifically, we need to include a "target" and "background" as parameters.
The "background" is what we described above, and the "target" is what we
aim to learn about: the **cancer** predicate.

.. code-block:: python

    >>> clf = BoostedRDNClassifier(background=bk, target="cancer")

Putting the pieces together
===========================

Now that we have seen each of the examples, we can put them together to learn
a series of trees.

>>> from srlearn.rdn import BoostedRDNClassifier
>>> from srlearn import Background
>>> from srlearn.datasets import load_toy_cancer
>>> train, test = load_toy_cancer()
>>> bk = Background(
...     modes=[
...         "friends(+person,-person).",
...         "friends(-person,+person).",
...         "cancer(+person).",
...         "smokes(+person).",
...     ],
... )
>>> clf = BoostedRDNClassifier(background=bk, target="cancer")
>>> clf.fit(train)
BoostedRDNClassifier(background=setParam: nodeSize=2.
setParam: maxTreeDepth=3.
setParam: numOfClauses=100.
setParam: numOfCycles=100.
usePrologVariables: true.
mode: friends(+person,-person).
mode: friends(-person,+person).
mode: cancer(+person).
mode: smokes(+person).
, max_tree_depth=3, n_estimators=10, neg_pos_ratio=2, node_size=2, solver='BoostSRL', target='cancer')
>>> clf.predict(test)
array([ True,  True,  True, False, False])

Conclusion
==========

For further reading, see the `example gallery <auto_examples/index.html>`_.

References
==========

.. [1] https://starling.utdallas.edu/software/boostsrl/wiki/basic-modes/

.. [2] Sriraam Natarajan, Tushar Khot, Kristian Kersting, and Jude Shavlik,
   "*Boosted Statistical Relational Learners: From Benchmarks to Data-Driven
   Medicine*". SpringerBriefs in Computer Science, ISBN: 978-3-319-13643-1,
   2015

.. [3] Sriraam Natarajan, Tushar Khot, Kristian Kersting, Bernd Gutmann,
   and Jude Shavlik,
   `"Gradient-based boosting for statistical relational learning: The relational dependency network case" <http://ftp.cs.wisc.edu/machine-learning/shavlik-group/natarajan.mlj12.pdf>`_.
   Machine Learning Journal (MLJ) 2011.
