# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Relational Dependency Networks
"""

import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_X_y
from sklearn.utils.validation import check_is_fitted

from .database import pathlib
from .background import Background


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
    >>> from boostsrl import example_data
    >>> dn = RDN(target="cancer")
    >>> dn.fit(example_data.train)
    RDN(background=Modes(), n_estimators=10, target='cancer')
    >>> dn.predict(example_data.test)
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, background=Background(), target="None", n_estimators=10):
        """Initialize an RDN

        Parameters
        ----------
        background : :class:`boostsrl.background.Background`
            Background knowledge with respect to the database (default=Background())
        target : str
            Target predicate to learn
        n_estimators : int, optional (default=10)
            Number of trees to fit

        Attributes
        ----------
        background_: Background
            Background object.
        estimators_ : array, shape (n_estimators)
            Return the boosted regression trees
        feature_importances_ : array, shape (n_features)
            Return the feature importances (based on how often each feature appears)
        """
        self.background = background
        self.target = target
        self.n_estimators = n_estimators

        # TODO: A better path manager would help in running multiple instances in
        #  parallel. This might be fixed by using the 'location' parameter here.

        self._train_log = "train_log.txt"
        self._test_log = "test_log.txt"

        # .jar file locations will be relative to this __file__
        self._here = pathlib.Path(__file__).parent
        self._boostsrl_jar = str(self._here.joinpath("v1-0.jar"))
        self._auc_jar = str(self._here.joinpath("auc.jar"))

        self.is_fitted = False

    def _check_params(self):
        """Check validity of parameters and raise ValueError if invalid."""
        if self.target == "None":
            raise ValueError("target must be set, cannot be {0}".format(self.target))
        if self.n_estimators <= 0:
            raise ValueError(
                "n_estimators must be greater than 0, cannot be {0}".format(
                    self.n_estimators
                )
            )

    def _check_initialized(self):
        """Check for the estimator(s), raise an error if not found."""
        check_is_fitted(self, "estimators_")

    def fit(self, database):
        """Learn structure and parameters.

        Fit the structure and parameters of a Relational Dependency Network using a
        database of positive examples, negative examples, facts, and any relevant
        background knowledge.

        Parameters
        ----------
        database : :class:`boostsrl.database.Database`
            Database containing examples and facts.
        location : str
            A relative path for storing training data.

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

        # TODO: On error, collect log files.

        location = "train"

        _CALL = (
            "java -jar "
            + self._boostsrl_jar
            + " -l -train "
            + str(self._here.joinpath(location))
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " > "
            + str(self._here.joinpath(self._train_log))
            + " 2>&1"
        )

        self.estimators_ = ["something"]

        # print(_CALL)
        return self

    @property
    def background_(self):
        """Set the background knowledge
        """
        return self._background

    @background_.setter
    def background_(self, Background):
        """Set the background knowledge.

        :return:
        """
        self._background = Background

    @property
    def feature_importances_(self):
        """Return the feature importances (the higher, the more important the feature).

        This is calculated based on how often a feature appears in the learned trees.

        Returns
        -------
        feature_importances_ : array, shape (n_features,)
        """
        self._check_initialized()
        return np.array([0, 1])

    def predict(self, database) -> None:
        """Use the learned model to predict on new data.

        Parameters
        ----------
        database : :class:`boostsrl.database.Database`
            Database containing examples and facts.
        location : str
            A relative path for storing test data.
        """

        self._check_initialized()

        location = "test"

        _CALL = (
            "java -jar "
            + self._boostsrl_jar
            + " -i -test "
            + str(self._here.joinpath(location))
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + self._auc_jar
            + " > "
            + str(self._here.joinpath(self._test_log))
            + " 2>&1"
        )

        # print(_CALL)

    def predict_proba(self, database, location="test") -> None:
        """
        Return probabilities instead.

        :param database:
        :param location:
        """

        check_is_fitted(self, "is_fitted_")
