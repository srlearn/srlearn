# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Relational Dependency Networks
"""

import re
import numpy as np

from .base import BaseBoostedRelationalModel


class BoostedRDN(BaseBoostedRelationalModel):
    """Relational Dependency Networks Estimator

    Wrappers around BoostSRL for learning and inference with Relational Dependency
    Networks written with a scikit-learn-style interface derived from
    :class:`sklearn.base.BaseEstimator`

    Similar to :class:`sklearn.ensemble.GradientBoostingClassifier`, this builds
    a model by fitting a series of regression trees.

    Examples
    --------

    >>> from srlearn.rdn import BoostedRDN
    >>> from srlearn import Background
    >>> from srlearn import example_data
    >>> bk = Background(modes=example_data.train.modes, use_std_logic_variables=True)
    >>> dn = BoostedRDN(background=bk, target="cancer")
    >>> dn.fit(example_data.train)
    BoostedRDN(background=setParam: nodeSize=2.
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
        """Initialize a BoostedRDN

        Parameters
        ----------
        background : :class:`srlearn.background.Background` (default: None)
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

        super().__init__(
            background=background,
            target=target,
            n_estimators=n_estimators,
            node_size=node_size,
            max_tree_depth=max_tree_depth,
        )

    def fit(self, database):
        """Learn structure and parameters.

        Fit the structure and parameters of a Relational Dependency Network using a
        database of positive examples, negative examples, facts, and any relevant
        background knowledge.

        Parameters
        ----------
        database : :class:`srlearn.database.Database`
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
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        # Write the data to files.
        database.write(
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -l -train "
            + str(self.file_system.files.TRAIN_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " > "
            + str(self.file_system.files.TRAIN_LOG.value)
        )

        if self.debug:
            print(_CALL)

        # Call the constructed command.
        self._call_shell_command(_CALL)

        # Read the trees from files.
        _estimators = []
        for _tree_number in range(self.n_estimators):
            with open(
                self.file_system.files.TREES_DIR.value.joinpath(
                    "{0}Tree{1}.tree".format(self.target, _tree_number)
                )
            ) as _fh:
                _estimators.append(_fh.read())

        self.estimators_ = _estimators

        return self

    def _run_inference(self, database) -> None:
        """Run inference mode on the BoostSRL Jar files.

        This is a helper method for ``self.predict`` and ``self.predict_proba``
        """

        self._check_initialized()

        # Write the background to file.
        self.background.write(
            filename="test", location=self.file_system.files.TEST_DIR.value
        )

        # Write the data to files.
        database.write(filename="test", location=self.file_system.files.TEST_DIR.value)

        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -i -test "
            + str(self.file_system.files.TEST_DIR.value)
            + " -model "
            + str(self.file_system.files.MODELS_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + str(self.file_system.files.AUC_JAR.value)
            + " > "
            + str(self.file_system.files.TEST_LOG.value)
        )

        if self.debug:
            print(_CALL)

        self._call_shell_command(_CALL)

        # Read the threshold
        with open(self.file_system.files.TEST_LOG.value, "r") as _fh:
            _threshold = re.findall("% Threshold = \\d*.\\d*", _fh.read())
        self.threshold_ = float(_threshold[0].split(" = ")[1])

    def predict(self, database):
        """Use the learned model to predict on new data.

        Parameters
        ----------
        database : :class:`srlearn.Database`
            Database containing examples and facts.

        Returns
        -------
        results : ndarray
            Positive or negative class.
        """

        self._run_inference(database)

        # Collect the classifications.
        _results_db = self.file_system.files.TEST_DIR.value.joinpath(
            "results_" + self.target + ".db"
        )
        _classes, _results = np.loadtxt(
            _results_db,
            delimiter=") ",
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
        database : :class:`srlearn.Database`
            Database containing examples and facts.

        Returns
        -------
        results : ndarray
            Probability of belonging to the positive class
        """

        self._run_inference(database)

        _results_db = self.file_system.files.TEST_DIR.value.joinpath(
            "results_" + self.target + ".db"
        )
        _classes, _results = np.loadtxt(
            _results_db,
            delimiter=") ",
            usecols=(0, 1),
            converters={0: lambda s: 0 if s[0] == 33 else 1},
            unpack=True,
        )

        _neg = _results[_classes == 0]
        _pos = _results[_classes == 1]
        _results2 = np.concatenate((_pos, 1 - _neg), axis=0)

        self.classes_ = _classes

        return _results2


class BoostedRDNRegressor(BaseBoostedRelationalModel):
    """Relational Dependency Networks Regressor

    Wrappers around BoostSRL for learning and inference of RDNs for regression task.

    Similar to :class:`sklearn.ensemble.GradientBoostingRegressor`, this builds
    a model by fitting a series of regression trees.

    Examples
    --------

    >>> from srlearn.rdn import BoostedRDNRegressor
    >>> from srlearn import Background
    >>> from srlearn import Database
    >>> train = Database.from_files(
            pos="./datasets/Boston/train/pos.pl",
            neg="./datasets/Boston/train/neg.pl",
            facts="./datasets/Boston/train/facts.pl",
            lazy_load=False
        )
    >>> test = Database.from_files(
            pos="./datasets/Boston/test/pos.pl",
            neg="./datasets/Boston/test/neg.pl",
            facts="./datasets/Boston/test/facts.pl",
            lazy_load=False
        )
    >>> train.modes = ["crim(+id,#varsrim).",
            "zn(+id,#varzn).",
            "indus(+id,#varindus).",
            "chas(+id,#varchas).",
            "nox(+id,#varnox).",
            "rm(+id,#varrm).",
            "age(+id,#varage).",
            "dis(+id,#vardis).",
            "rad(+id,#varrad).",
            "tax(+id,#vartax).",
            "ptratio(+id,#varptrat).",
            "b(+id,#varb).",
            "lstat(+id,#varlstat).",
            "medv(+id)."]
    >>> bk = Background(modes=train.modes)
    >>> reg = BoostedRDNRegressor(background=bk, target="medv", n_estimators=20)
    >>> reg.fit(train)
    BoostedRegressionTrees(background=setParam: nodeSize=2.
    setParam: maxTreeDepth=3.
    setParam: numberOfClauses=100.
    setParam: numberOfCycles=100.
    mode: crim(+id,#varsrim).
    mode: zn(+id,#varzn).
    mode: indus(+id,#varindus).
    mode: chas(+id,#varchas).
    mode: nox(+id,#varnox).
    mode: rm(+id,#varrm).
    mode: age(+id,#varage).
    mode: dis(+id,#vardis).
    mode: rad(+id,#varrad).
    mode: tax(+id,#vartax).
    mode: ptratio(+id,#varptrat).
    mode: b(+id,#varb).
    mode: lstat(+id,#varlstat).
    mode: medv(+id).
    ,
                           n_estimators=20, target='medv')
    >>> reg.predict(test)
    array([10.04313307 13.55804603 20.549378   18.14681934 23.9393469  10.01292162
         29.83298024 20.34668817 27.81642572 32.04067867  9.41342835 20.975001
         19.21966845])

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
        """Initialize a BoostedRDN

        Parameters
        ----------
        background : :class:`srlearn.background.Background` (default: None)
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

        super().__init__(
            background=background,
            target=target,
            n_estimators=n_estimators,
            node_size=node_size,
            max_tree_depth=max_tree_depth,
        )

    def fit(self, database):
        """Learn structure and parameters.

        Fit the structure and parameters of a Relational Dependency Network using a
        database of positive examples, negative examples, facts, and any relevant
        background knowledge.

        Parameters
        ----------
        database : :class:`srlearn.database.Database`
            Database containing examples and facts.

        Returns
        -------
        self : object
            Returns self.

        Notes
        -----

        The underlying algorithm is based on the "Relational Functional Gradient
        Boosting" as described in [1]_ and [2]_.

        This fit function is based on subprocess calling the BoostSRL jar files.
        This will require a Java runtime to also be available. See [3]_.

        .. [1] Sriraam Natarajan, Tushar Khot, Kristian Kersting, and Jude Shavlik,
           "*Boosted Statistical Relational Learners: From Benchmarks to Data-Driven
           Medicine*". SpringerBriefs in Computer Science, ISBN: 978-3-319-13643-1,
           2015
        -- [2] https://starling.utdallas.edu/software/boostsrl/wiki/regression/
        .. [3] https://starling.utdallas.edu/software/boostsrl/
        """

        self._check_params()

        # Write the background to file.
        self.background.write(
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        # Write the data to files.
        database.write(
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -reg -l -train "
            + str(self.file_system.files.TRAIN_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " > "
            + str(self.file_system.files.TRAIN_LOG.value)
        )

        if self.debug:
            print(_CALL)

        # Call the constructed command.
        self._call_shell_command(_CALL)

        # Read the trees from files.
        _estimators = []
        for _tree_number in range(self.n_estimators):
            with open(
                self.file_system.files.TREES_DIR.value.joinpath(
                    "{0}Tree{1}.tree".format(self.target, _tree_number)
                )
            ) as _fh:
                _estimators.append(_fh.read())

        self.estimators_ = _estimators

        return self

    def _run_inference(self, database) -> None:
        """Run inference mode on the BoostSRL Jar files.

        This is a helper method for ``self.predict`` and ``self.predict_proba``
        """

        self._check_initialized()

        # Write the background to file.
        self.background.write(
            filename="test", location=self.file_system.files.TEST_DIR.value
        )

        # Write the data to files.
        database.write(filename="test", location=self.file_system.files.TEST_DIR.value)

        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -reg -i -test "
            + str(self.file_system.files.TEST_DIR.value)
            + " -model "
            + str(self.file_system.files.MODELS_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + str(self.file_system.files.AUC_JAR.value)
            + " > "
            + str(self.file_system.files.TEST_LOG.value)
        )

        if self.debug:
            print(_CALL)

        self._call_shell_command(_CALL)

    def predict(self, database):
        """Use the learned model to predict values on new data.

        Parameters
        ----------
        database : :class:`srlearn.Database`
            Database containing examples and facts.

        Returns
        -------
        pred : ndarray
            regression value predicted for each example.
        """

        self._run_inference(database)

        # Collect the classifications.
        _results_db = self.file_system.files.TEST_DIR.value.joinpath(
            "results_" + self.target + ".db"
        )
        _pred, _true = np.loadtxt(
            _results_db,
            delimiter="\t",
            usecols=(1, 2),
            unpack=True,
        )

        self.true_ = _true
        self.pred_ = _pred

        return _pred
