# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Markov Logic Networks
"""

import numpy as np
from .base import BaseBoostedRelationalModel


class MLNClassifier(BaseBoostedRelationalModel):
    """Markov Logic Networks Estimator

    Wrappers around BoostSRL for learning and inference with Markov Logic
    Networks written with a scikit-learn-style interface.

    Examples
    --------

    >>> from boostsrl.mln import MLN
    >>> from boostsrl import Background
    >>> from boostsrl import example_data
    >>> bk = Background(modex=example_data.train.modes, use_std_logic_variables=True)
    >>> mln = MLN(background=bk, target="cancer")
    >>> mln.fit(example_data.train)
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
        """Initialize a Markov Logic Network Classifier

        Parameters
        ----------

        :param background:
        :param target:
        :param n_estimators:
        :param node_size:
        :param max_tree_depth:
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

        :param database:
        :return:
        """

        self._check_params()

        # Write the background to a file.
        self.background.write(
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        # Write the data to files
        database.write(
            filename="train", location=self.file_system.files.TRAIN_DIR.value
        )

        # TODO: Currently uses the tree-structured mlns.
        #  Clausal representation should also be available.
        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -l -mln -train "
            + str(self.file_system.files.TRAIN_DIR.value)
            + " - target "
            + self.target
            + str(self.n_estimators)
            + " > "
            + str(self.file_system.files.TRAIN_LOG.value)
        )

        if self.debug:
            print(_CALL)

        self._call_shell_command(_CALL)

    def _run_inference(self, database):
        """Run BoostSRL jar files in inference mode.

        Helper method for ``self.predict`` and ``self.predict_proba``
        """

        self._check_initialized()

        # Write the background to a file.
        self.background.write(
            filename="test", location=self.file_system.files.TEST_DIR.value
        )

        # Write the data to files
        database.write(
            filename="test", location=self.file_system.files.TESTDIR.value
        )

        _CALL = (
            "java -jar "
            + str(self.file_system.files.BOOST_JAR.value)
            + " -i -mln -test "
            + str(self.file_system.files.TEST_DIR.value)
            + " -model "
            + str(self.file_system.files.MODELS_DIR.value)
            + " -target "
            + self.target
            + " -trees "
            + str(self.trees)
            + " -aucJarPath "
            + str(self.file_system.files.AUC_JAR.value)
            + " > "
            + str(self.file_system.files.TEST_LOG.value)
        )

        if self.debug:
            print(_CALL)

        self._call_shell_command(_CALL)

    def predict(self, database):
        """Use the learned model to predict on new data.
        """

        self._run_inference(database)


        # Collect the classifications.
        _results_db = self.file_system.files.TEST_DIR.value.joinpath(
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
        """Return class probabilities (currently probability of positive class)
        """

        self._run_inference(database)

        _results_db = self.file_system.files.TEST_DIR.value.joinpath(
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
