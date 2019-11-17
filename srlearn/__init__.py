# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
srlearn: A Python Library for Gradient-Boosted Statistical Relational Models.

Submodules
----------

utils
    Utility modules for developing with the srlearn package.
"""

from .background import Background
from .database import Database

from ._meta import __author__
from ._meta import __version__
from .utils._show_versions import show_versions

__all__ = ["Background", "Database", "__author__", "__version__", "show_versions"]
