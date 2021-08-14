########
srlearn
########

.. image:: https://raw.githubusercontent.com/srlearn/srlearn/main/docs/source/_static/preview.png
    :alt:  Repository preview image: "srlearn. Python wrappers around BoostSRL with a scikit-learn-style interface. pip install srlearn."

|License|_ |LGTM|_ |GitHubBuilds|_ |Codecov|_ |ReadTheDocs|_

.. |License| image:: https://img.shields.io/github/license/srlearn/srlearn.svg
    :alt: License
.. _License: LICENSE

.. |LGTM| image:: https://img.shields.io/lgtm/grade/python/github/srlearn/srlearn?label=code%20quality&logo=lgtm
    :alt: LGTM code quality analysis
.. _LGTM: https://lgtm.com/projects/g/srlearn/srlearn/context:python

.. |GitHubBuilds| image:: https://github.com/srlearn/srlearn/actions/workflows/python_tests.yml/badge.svg
    :alt: GitHub CI Builds 
.. _GitHubBuilds: https://github.com/srlearn/srlearn/actions/workflows/python_tests.yml

.. |Codecov| image:: https://codecov.io/gh/srlearn/srlearn/branch/main/graphs/badge.svg?branch=main
    :alt: Code coverage status
.. _Codecov: https://codecov.io/github/srlearn/srlearn?branch=main

.. |ReadTheDocs| image:: https://readthedocs.org/projects/srlearn/badge/?version=latest
    :alt: Documentation status
.. _ReadTheDocs: https://srlearn.readthedocs.io/en/latest/

**srlearn** is a set of Python wrappers around
`BoostSRL <https://starling.utdallas.edu/software/BoostSRL>`_ with a scikit-learn interface.

- **Documentation**: https://srlearn.readthedocs.io/en/latest/
- **Questions?** Contact `Alexander L. Hayes  <https://hayesall.com>`_ (`hayesall <https://github.com/hayesall>`_)

Getting Started
---------------

**Prerequisites**:

- Java 1.8
- Python (3.6, 3.7)

**Installation**

.. code-block:: bash

   pip install srlearn

Basic Usage
-----------

The general setup should be similar to scikit-learn. But there are a few extra requirements in terms of setting
background knowledge and formatting the data.

A minimal working example (using the Toy-Cancer data set imported with 'load_toy_cancer') is:

.. code-block:: python

    from srlearn.rdn import BoostedRDN
    from srlearn import Background
    from srlearn.datasets import load_toy_cancer
    toy_cancer = load_toy_cancer()
    bk = Background(
        modes=toy_cancer.train.modes,
        use_std_logic_variables=True,
    )
    clf = BoostedRDN(
        background=bk,
        target='cancer',
    )
    clf.fit(toy_cancer.train)
    clf.predict_proba(toy_cancer.test)
    # array([0.88079619, 0.88079619, 0.88079619, 0.3075821 , 0.3075821 ])
    print(clf.classes_)
    # array([1., 1., 1., 0., 0.])

``toy_cancer.train`` and ``toy_cancer.test`` are each ``srlearn.Database`` objects, so this hides some of
the complexity behind the scenes.

This example abstracts away some complexity in exchange for compactness.
For more examples, see the `Example Gallery <https://srlearn.readthedocs.io/en/latest/auto_examples/index.html>`_.

Contributing
------------

We have adopted the `Contributor Covenant Code of Conduct <https://github.com/srlearn/srlearn/blob/main/.github/CODE_OF_CONDUCT.md>`_ version 1.4. Please read,
follow, and report any incidents which violate this.

Questions, Issues, and Pull Requests are welcome. Please refer to `CONTRIBUTING.md <https://github.com/srlearn/srlearn/blob/main/.github/CONTRIBUTING.md>`_ for
information on submitting issues and pull requests.

Versioning and Releases
-----------------------

We use `SemVer <https://semver.org>`_ for versioning.
See `Releases <https://github.com/srlearn/srlearn/releases>`_
for stable versions that are available, or the
`Project Page on PyPi <https://pypi.org/project/srlearn/>`_.
