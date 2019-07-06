# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
boostsrl metadata

- Versioning should follow SemVer (https://semver.org)
- DEBUG flag is a global setting for debug information that should be False at
  distribution time.

  >>> from ._meta import DEBUG
  >>> if DEBUG:
  ...     print("Debugging")

"""

__author__ = "Alexander L. Hayes (hayesall)"
__version__ = "0.4.2"

DEBUG = False
