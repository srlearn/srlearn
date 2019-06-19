========
boostsrl
========

|License|_ |Travis|_ |Codecov|_

.. |License| image:: https://img.shields.io/github/license/starling-lab/boostsrl-python-package.svg
.. _License: LICENSE

.. |Travis| image:: https://travis-ci.org/starling-lab/boostsrl-python-package.svg?branch=master
.. _Travis: https://travis-ci.org/starling-lab/boostsrl-python-package

.. |Codecov| image:: https://codecov.io/gh/starling-lab/boostsrl-python-package/branch/master/graphs/badge.svg?branch=master
.. _Codecov: https://codecov.io/github/starling-lab/boostsrl-python-package?branch=master

**boostsrl** is a set of Python wrappers around
`BoostSRL <https://starling.utdallas.edu/software/BoostSRL>`_

Getting Started
---------------

**Prerequisites**:

- Java 1.8
- Python (3.5, 3.6, 3.7)
- subprocess
- graphviz

**Installation**

.. code-block:: bash

   pip install boostsrl

Basic Usage
-----------

.. code-block:: python

   from boostsrl import boostsrl

   bk = boostsrl.example_data("background")
   background = boostsrl.modes(
	bk,
	["cancer"],
	useStdLogicVariables=True,
	treeDepth=4,
	nodeSize=2,
	numOfClauses=8
   )

   # Example Training Data
   train_pos = boostsrl.example_data("train_pos")
   train_neg = boostsrl.example_data("train_neg")
   train_facts = boostsrl.example_data("train_facts")

   model = boostsrl.train(background, train_pos, train_neg, train_facts)

   # Example Test Data
   test_pos = boostsrl.example_data("test_pos")
   test_neg = boostsrl.example_data("test_neg")
   test_facts = boostsrl.example_data("test_facts")
   
   test = boostsrl.test(model, test_pos, test_neg, test_facts)

   print("Training Time (s)", model.traintime())
   print("Results Summary  ", test.summarize_results())
   print("Inference Results", test.inference_results("cancer"))

Contributing
------------

Please refer to `CONTRIBUTING.md <.github/CONTRIBUTING.md>`_ for information on
submitting issues and pull requests.

Versioning
----------

We use `SemVer <https://semver.org>`_ for versioning.
See `Releases <https://github.com/starling-lab/boostsrl-python-package/releases>`_
for stable versions that are available, or the
`Project Page on PyPi <https://pypi.org/project/boostsrl/>`_.
