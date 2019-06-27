# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Relational Dependency Networks
"""

import os
import re
import subprocess
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_is_fitted

from .background import Background
from .system_manager import FileSystem
from ._meta import DEBUG


# TODO: @property: feature_importances_


class RDN(BaseEstimator, ClassifierMixin):
    """Relational Dependency Networks Estimator

    Wrappers around BoostSRL for learning and inference with Relational Dependency
    Networks written with a scikit-learn-style interface derived from
    :class:`sklearn.base.BaseEstimator`

    Similar to :class:`sklearn.ensemble.GradientBoostingClassifier`, this builds
    a model by fitting a series of regression trees.

    Examples
    --------

    >>> from boostsrl.rdn import RDN
    >>> from boostsrl import Background
    >>> from boostsrl import example_data
    >>> bk = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    >>> dn = RDN(background=bk, target="cancer")
    >>> dn.fit(example_data.train)
    RDN(background=setParam: nodeSize=2.
    setParam: maxTreeDepth=3.
    setParam: numberOfClauses=100.
    setParam: numberOfCycles=100.
    useStdLogicVariables: true.
    mode: friends(+Person,-Person).
    mode: friends(-Person,+Person).
    mode: smokes(+Person).
    mode: cancer(+Person).
    ,
        max_tree_depth=3, n_estimators=10, node_size=2, target='cancer')
    >>> dn.predict(example_data.test)
    array([ True,  True,  True, False, False])

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
        """Initialize an RDN

        Parameters
        ----------
        background : :class:`boostsrl.background.Background` (default: None)
            Background knowledge with respect to the database
        target : str (default: "None")
            Target predicate to learn
        n_estimators : int, optional (default: 10)
            Number of trees to fit
        node_size : int, optional (default: 2)
            Maximum number of literals in each node.
        max_tree_depth : int, optional (default: 3)
            Maximum number of nodes from root to leaf (height) in the tree.

        Attributes
        ----------
        estimators_ : array, shape (n_estimators)
            Return the boosted regression trees
        feature_importances_ : array, shape (n_features)
            Return the feature importances (based on how often each feature appears)
        """
        self.background = background
        self.target = target
        self.n_estimators = n_estimators
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.debug = DEBUG

        # Initialize the _FILE_SYSTEM to None. Replace if parameters are valid.
        self._FILE_SYSTEM = None

    def _check_params(self):
        """Check validity of parameters and raise ValueError if invalid.

        If all parameters are valid, instantiate ``self._FILE_SYSTEM`` by
        instantiating it with a :class:`boostsrl.system_manager.FileSystem`
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
                "background should be a boostsrl.Background object, cannot be {0}".format(
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
        self.FILE_SYSTEM = FileSystem()

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

        # TODO: Explore other ways to interface with BoostSRL or the JVM.
        #   https://wiki.python.org/moin/IntegratingPythonWithOtherLanguages#Java

        _pid = subprocess.Popen(shell_command, shell=True)
        _id, _status = os.waitpid(_pid.pid, 0)
        if _status != 0:
            raise RuntimeError(
                "Error when running shell command: {0}".format(shell_command)
            )

    def fit(self, database):
        """Learn structure and parameters.

        Fit the structure and parameters of a Relational Dependency Network using a
        database of positive examples, negative examples, facts, and any relevant
        background knowledge.

        Parameters
        ----------
        database : :class:`boostsrl.database.Database`
            Database containing examples and facts.

        Returns
        -------
        self : object
            Returns self.

        Notes
        -----

        The underlying algorithm is based on the "Relational Functional Gradient
        Boosting" as described in [1]_.

        This fit function is based on subprocess calling the BoostSRL jar files.
        This will require a Java runtime to also be available. See [2]_.

        .. [1] Sriraam Natarajan, Tushar Khot, Kristian Kersting, and Jude Shavlik,
           "*Boosted Statistical Relational Learners: From Benchmarks to Data-Driven
           Medicine*". SpringerBriefs in Computer Science, ISBN: 978-3-319-13643-1,
           2015
        .. [2] https://starling.utdallas.edu/software/boostsrl/
        """

        self._check_params()

        # Write the background to file.
        self.background.write(
            filename="train", location=self.FILE_SYSTEM.files.TRAIN_DIR.value
        )

        # Write the data to files.
        database.write(
            filename="train", location=self.FILE_SYSTEM.files.TRAIN_DIR.value
        )

        _CALL = (
            "java -jar "
            + str(self.FILE_SYSTEM.files.BOOST_JAR.value)
            + " -l -train "
            + str(self.FILE_SYSTEM.files.TRAIN_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " > "
            + str(self.FILE_SYSTEM.files.TRAIN_LOG.value)
        )

        if self.debug:
            print(_CALL)

        # Call the constructed command.
        self._call_shell_command(_CALL)

        # Read the trees from files.
        _estimators = []
        for _tree_number in range(self.n_estimators):
            with open(
                self.FILE_SYSTEM.files.TREES_DIR.value.joinpath(
                    "{0}Tree{1}.tree".format(self.target, _tree_number)
                )
            ) as _fh:
                _estimators.append(_fh.read())

        self.estimators_ = _estimators

        # TODO: On error, collect log files.
        return self

    def _run_inference(self, database) -> None:
        """Run inference mode on the BoostSRL Jar files.

        This is a helper method for ``self.predict`` and ``self.predict_proba``
        """

        self._check_initialized()

        # Write the background to file.
        self.background.write(
            filename="test", location=self.FILE_SYSTEM.files.TEST_DIR.value
        )

        # Write the data to files.
        database.write(filename="test", location=self.FILE_SYSTEM.files.TEST_DIR.value)

        _CALL = (
            "java -jar "
            + str(self.FILE_SYSTEM.files.BOOST_JAR.value)
            + " -i -test "
            + str(self.FILE_SYSTEM.files.TEST_DIR.value)
            + " -model "
            + str(self.FILE_SYSTEM.files.MODELS_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + str(self.FILE_SYSTEM.files.AUC_JAR.value)
            + " > "
            + str(self.FILE_SYSTEM.files.TEST_LOG.value)
        )

        if self.debug:
            print(_CALL)

        self._call_shell_command(_CALL)

        # Read the threshold
        with open(self.FILE_SYSTEM.files.TEST_LOG.value, "r") as _fh:
            _threshold = re.findall("% Threshold = \\d*.\\d*", _fh.read())
        self.threshold_ = float(_threshold[0].split(" = ")[1])

    def predict(self, database):
        """Use the learned model to predict on new data.

        Parameters
        ----------
        database : :class:`boostsrl.Database`
            Database containing examples and facts.

        Returns
        -------
        results : ndarray
            Positive or negative class.
        """

        self._run_inference(database)

        # Collect the classifications.
        _results_db = self.FILE_SYSTEM.files.TEST_DIR.value.joinpath(
            "results_" + self.target + ".db"
        )
        _classes, _results = np.loadtxt(
            _results_db,
            delimiter=" ",
            usecols=(0, 1),
            converters={0: lambda s: 0 if s[0] == 33 else 1},
            unpack=True,
        )

        self.classes_ = _classes

        _neg = _results[_classes == 0]
        _pos = _results[_classes == 1]
        _results2 = np.greater(
            np.concatenate((_pos, 1 - _neg), axis=0), self.threshold_
        )

        return _results2

    def predict_proba(self, database):
        """Return class probabilities.

        Parameters
        ----------
        database : :class:`boostsrl.Database`
            Database containing examples and facts.

        Returns
        -------
        results : ndarray
            Probability of belonging to the positive class
        """

        self._run_inference(database)

        _results_db = self.FILE_SYSTEM.files.TEST_DIR.value.joinpath(
            "results_" + self.target + ".db"
        )
        _classes, _results = np.loadtxt(
            _results_db,
            delimiter=" ",
            usecols=(0, 1),
            converters={0: lambda s: 0 if s[0] == 33 else 1},
            unpack=True,
        )

        _neg = _results[_classes == 0]
        _pos = _results[_classes == 1]
        _results2 = np.concatenate((_pos, 1 - _neg), axis=0)

        self.classes_ = _classes

        return _results2
