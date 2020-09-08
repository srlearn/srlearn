# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Base class for Boosted Relational Models
"""

from collections import Counter

from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_is_fitted
import subprocess

from .background import Background
from .system_manager import FileSystem
from .utils._parse_trees import parse_tree
from ._meta import DEBUG


class BaseBoostedRelationalModel(BaseEstimator, ClassifierMixin):
    """Base class for deriving boosted relational models

    This class extends :class:`sklearn.base.BaseEstimator` and
    :class:`sklearn.base.ClassifierMixin` while providing several utilities
    for instantiating a model and performing learning/inference with the
    BoostSRL jar files.

    .. note:: This is not a complete treatment of *how to derive estimators*.
        Contributions would be appreciated.

    Examples
    --------

    The actual :class:`srlearn.rdn.BoostedRDN` is derived from this class, so this
    example is similar to the implementation (but the actual implementation
    passes model parameters instead of leaving them with the defaults).
    This example derives a new class ``BoostedRDN``, which inherits the default
    values of the superclass while also setting a 'special_parameter' which
    may be unique to this model.

    All that remains is to implement the specific cases of ``fit()``,
    ``predict()``, and ``predict_proba()``.

    >>> from srlearn.base import BaseBoostedRelationalModel
    >>> class BoostedRDN(BaseBoostedRelationalModel):
    ...     def __init__(self, special_parameter=5):
    ...         super().__init__(self)
    ...         self.special_parameter = special_parameter
    ...
    >>> dn = BoostedRDN(special_parameter=8)
    >>> print(dn)
    BoostedRDN(special_parameter=8)
    >>> print(dn.n_estimators)
    10
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        background=None,
        target="None",
        n_estimators=10,
        node_size=2,
        max_tree_depth=3,
    ):
        """Initialize a BaseEstimator"""
        self.background = background
        self.target = target
        self.n_estimators = n_estimators
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.debug = DEBUG

    def _check_params(self):
        """Check validity of parameters. Raise ValueError if errors are detected.

        If all parameters are valid, instantiate ``self.file_system`` by
        instantiating it with a :class:`srlearn.system_manager.FileSystem`
        """
        if self.target == "None":
            raise ValueError("target must be set, cannot be {0}".format(self.target))
        if not isinstance(self.target, str):
            raise ValueError(
                "target must be a string, cannot be {0}".format(self.target)
            )
        if self.background is None:
            raise ValueError(
                "background must be set, cannot be {0}".format(self.background)
            )
        if not isinstance(self.background, Background):
            raise ValueError(
                "background should be a srlearn.Background object, cannot be {0}".format(
                    self.background
                )
            )
        if not isinstance(self.n_estimators, int) or isinstance(
            self.n_estimators, bool
        ):
            raise ValueError(
                "n_estimators must be an integer, cannot be {0}".format(
                    self.n_estimators
                )
            )
        if self.n_estimators <= 0:
            raise ValueError(
                "n_estimators must be greater than 0, cannot be {0}".format(
                    self.n_estimators
                )
            )

        # If all params are valid, allocate a FileSystem:
        self.file_system = FileSystem()

    def feature_importance(self):
        """
        Return the features contained in a tree.

        Parameters
        ----------

        tree_number: int
            Index of the tree to read.
        """

        features = []

        for tree_number in range(self.n_estimators):
            _rules_string = self.estimators_[tree_number]
            features += parse_tree(_rules_string)
        return Counter(features)

    def _check_initialized(self):
        """Check for the estimator(s), raise an error if not found."""
        check_is_fitted(self, "estimators_")

    @staticmethod
    def _call_shell_command(shell_command):
        """Start a new process to execute a shell command.

        This is intended for use in calling jar files. It opens a new process and
        waits for it to return 0.

        Parameters
        ----------
        shell_command : str
            A string representing a shell command.

        Returns
        -------
        None
        """

        _pid = subprocess.Popen(shell_command, shell=True)
        _status = _pid.wait()
        if _status != 0:
            raise RuntimeError(
                "Error when running shell command: {0}".format(shell_command)
            )

    def fit(self, database):
        raise NotImplementedError

    def predict(self, database):
        raise NotImplementedError

    def predict_proba(self, database):
        raise NotImplementedError
