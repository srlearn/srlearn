############
srlearn API
############

.. currentmodule:: srlearn

Core Classes
============

These classes form the set of core pieces for describing the data, providing
background knowledge, and learning.

.. autosummary::
   :toctree: generated/
   :template: class.rst

   Database
   Background
   rdn.BoostedRDN
   rdn.BoostedRDNRegressor

Data Sets
=========

There are some toy datasets built into the srlearn package. For more datasets,
see the `relational-datasets package <https://srlearn.github.io/relational-datasets/>`_.

.. autosummary::
   :toctree: generated/
   :template: function.rst 

   datasets.load_toy_cancer
   datasets.load_toy_father

Plotting and Visualization
==========================

These may be helpful for visualizing trees.

.. autosummary::
   :toctree: generated/
   :template: function.rst

   plotting.export_digraph
   plotting.plot_digraph

Utilities
=========

Some of these are for behind-the-scenes operations, but tend to
be useful for further development
(`contributions are welcome! <https://github.com/hayesall/srlearn/blob/main/.github/CONTRIBUTING.md>`_).

.. autosummary::
   :toctree: generated/
   :template: class.rst

   base.BaseBoostedRelationalModel
   system_manager.FileSystem

.. autosummary::
   :toctree: generated/
   :template: function.rst

   system_manager.reset

Deprecated boostsrl objects
===========================

This is the old API style that has been deprecated. It is no longer tested or
actively developed and is pending removal in 0.6.0.

.. autosummary::
   :toctree: generated/

   srlearn.boostsrl
