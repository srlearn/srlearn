# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Base class for Boosted Relational Models
"""

from collections import Counter
import json
import logging

from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_is_fitted
import subprocess

from .background import Background
from .system_manager import FileSystem
from .utils._parse_trees import parse_tree
from ._meta import __version__


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

    The actual :class:`srlearn.rdn.BoostedRDNClassifier` is derived from this class, so this
    example is similar to the implementation (but the actual implementation
    passes model parameters instead of leaving them with the defaults).
    This example derives a new class ``BoostedRDNClassifier``, which inherits the default
    values of the superclass while also setting a 'special_parameter' which
    may be unique to this model.

    All that remains is to implement the specific cases of ``fit()``,
    ``predict()``, and ``predict_proba()``.

    >>> from srlearn.base import BaseBoostedRelationalModel
    >>> class BoostedRDNClassifier(BaseBoostedRelationalModel):
    ...     def __init__(self, special_parameter=5):
    ...         super().__init__(self)
    ...         self.special_parameter = special_parameter
    ...
    >>> dn = BoostedRDNClassifier(special_parameter=8)
    >>> print(dn)
    BoostedRDNClassifier(special_parameter=8)
    >>> print(dn.n_estimators)
    10
    """

    # pylint: disable=too-many-instance-attributes
    background = None
    target = "None"
    n_estimators = 10
    node_size = 2
    max_tree_depth = 3
    neg_pos_ratio = 2

    def __init__(
        self,
        background=None,
        target="None",
        n_estimators=10,
        node_size=2,
        max_tree_depth=3,
        neg_pos_ratio=2,
    ):
        """Initialize a BaseEstimator"""
        self.background = background
        self.target = target
        self.n_estimators = n_estimators
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.neg_pos_ratio = neg_pos_ratio

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
        if (
            not isinstance(self.neg_pos_ratio, int)
            and not isinstance(self.neg_pos_ratio, float)
            or isinstance(self.neg_pos_ratio, bool)
        ):
            raise ValueError("neg_pos_ratio must be an integer or float")
        if self.neg_pos_ratio < 1:
            raise ValueError(
                "neg_pos_ratio must be greater than 1, cannot be {0}".format(
                    self.neg_pos_ratio
                )
            )

        # If all params are valid, allocate a FileSystem:
        self.file_system = FileSystem()

    def to_json(self, file_name) -> None:
        """Serialize a learned model to json.

        Parameters
        ----------
        file_name : str (or pathlike)
            Path to a saved json file.

        Notes / Warnings
        ----------------

        This feature is *experimental*.
        There could be major changes between releases, causing old model
        files to break.
        """
        check_is_fitted(self, "estimators_")

        with open(
            self.file_system.files.BRDNS_DIR.value.joinpath(
                "{0}.model".format(self.target)
            ),
            "r",
        ) as _fh:
            _model = _fh.read().splitlines()

        model_params = {
            "background": dict(self.background.__dict__.items()),
            "target": self.target,
            "n_estimators": self.n_estimators,
            "node_size": self.node_size,
            "max_tree_depth": self.max_tree_depth,
            "neg_pos_ratio": self.neg_pos_ratio,
        }

        with open(file_name, "w") as _fh:
            _fh.write(
                json.dumps(
                    [
                        __version__,
                        _model,
                        self.estimators_,
                        model_params,
                        self._dotfiles,
                    ]
                )
            )

    def from_json(self, file_name):
        """Load a learned model from json.

        Parameters
        ----------
        file_name : str (or pathlike)
            Path to a saved json file.

        Notes / Warnings
        ----------------

        This feature is *experimental*.
        There could be major changes between releases, causing old model
        files to break. There are also *no checks* to ensure you are
        loading the correct object type.
        """

        with open(file_name, "r") as _fh:
            params = json.loads(_fh.read())

        if params[0] != __version__:
            logging.warning(
                "Version of loaded model ({0}) does not match srlearn version ({1}).".format(
                    params[0], __version__
                )
            )

        _model = params[1]
        _estimators = params[2]
        _model_parameters = params[3]

        try:
            self._dotfiles = params[4]
        except IndexError:
            self._dotfiles = None
            logging.warning(
                "Did not find dotfiles during load, srlearn.plotting may not work."
            )

        _bkg = Background()
        _bkg.__dict__ = _model_parameters["background"]

        # 1. Loop over all class attributes of `BaseBoostedRelationalModel`
        #    except `background`, which has been handled as a special case.
        # 2. Update an `_attributes` dictionary mapping attributes from JSON
        # 3. *If a key was not present in the JSON*: set it to the default value.
        # 4. Initialize self by unpacking the dictionary into arguments.
        _attributes = {"background": _bkg}
        for key in BaseBoostedRelationalModel().__dict__.keys() - {"background"}:
            _attributes[key] = _model_parameters.get(
                key,
                BaseBoostedRelationalModel().__dict__[key],
            )
        self.__init__(**_attributes)

        self.estimators_ = _estimators

        # Currently allocates the File System.
        self._check_params()

        self.file_system.files.TREES_DIR.value.mkdir(parents=True)

        with open(
            self.file_system.files.BRDNS_DIR.value.joinpath(
                "{0}.model".format(self.target)
            ),
            "w",
        ) as _fh:
            _fh.write("\n".join(_model))

        for i, _tree in enumerate(_estimators):
            with open(
                self.file_system.files.TREES_DIR.value.joinpath(
                    "{0}Tree{1}.tree".format(self.target, i)
                ),
                "w",
            ) as _fh:
                _fh.write(_tree)

    @property
    def feature_importances_(self):
        """
        Return the features contained in a tree.

        Parameters
        ----------

        tree_number: int
            Index of the tree to read.
        """
        check_is_fitted(self, "estimators_")

        features = []

        for tree_number in range(self.n_estimators):
            _rules_string = self.estimators_[tree_number]
            features += parse_tree(
                _rules_string, (not self.background.use_std_logic_variables)
            )
        return Counter(features)

    def _get_dotfiles(self):
        dotfiles = []
        for i in range(self.n_estimators):
            with open(
                self.file_system.files.DOT_DIR.value.joinpath(
                    "WILLTreeFor_" + self.target + str(i) + ".dot"
                )
            ) as _fh:
                dotfiles.append(_fh.read())
        self._dotfiles = dotfiles

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
