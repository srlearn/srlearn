# Copyright 2017, 2018, 2019 Alexander L. Hayes

from .database import Database
from .database import pathlib


class RDN:
    """
    Wrappers around BoostSRL for learning and inference with Relational Dependency Networks
    written with a scikit-learn-style interface.

    :param str target: The target predicate being predicted in the database.
    :param str location: A relative location.

    Examples
    
    .. code-block:: python
    
       >>> from boostsrl.rdn import RDN
       >>> from boostsrl import example_data
       >>> dn = RDN("cancer")
       >>> dn.background = example_data.train.background
       >>> dn.fit(example_data.train)
       >>> dn.predict(example_data.test)
    """

    def __init__(self, target="None", location="bsrl_data"):

        self._target = target
        # TODO: A better path manager would help in running multiple instances in parallel.
        #       This might be fixed by using the 'location' parameter here.

        # TODO: How should modes/background knowledge be handled?
        self.background = None

        self._train_log = "train_log.txt"
        self._test_log = "test_log.txt"

        # .jar file locations will be relative to this __file__
        self._here = pathlib.Path(__file__).parent
        self._boostsrl_jar = str(self._here.joinpath("v1-0.jar"))
        self._auc_jar = str(self._here.joinpath("auc.jar"))

        self._ran = 0

    def __repr__(self) -> str:
        return "Relational Dependency Network Object\ntarget: " + self._target

    def fit(self, database, location="train") -> None:
        """
        Fit a relational dependency network to the underlying database,
        simultaneously learning both the structure and parameters of a
        model.

        :param database database: Database containing positives, negatives, and facts.
        :param str location: A relative path for storing training data.
        """

        if self._target == "None":
            raise Exception("Target cannot be None.")
        if self._trees == 0:
            raise Exception("Trees must be greater than 0.")

        # TODO: On error, collect log files.

        _CALL = (
            "java -jar "
            + self._boostsrl_jar
            + " -l -train "
            + str(self._here.joinpath(location))
            + " -target "
            + self._target
            + " -trees "
            + str(self._n_trees)
            + " > "
            + str(self._here.joinpath(self._train_log))
            + " 2>&1"
        )

        print(_CALL)
        self._ran = 1

    def predict(self, database, location="test") -> None:
        """
        Use the learned model to predict on new data.

        :param database database: Database containing positives, negatives, and facts.
        :param str location: A relative path for storing test data.
        """

        if not self._ran:
            raise Exception("Error, cannot run 'RDN.predict()' before 'RDN.fit()'")

        _CALL = (
            "java -jar "
            + self._boostsrl_jar
            + " -i -test "
            + str(self._here.joinpath(location))
            + " -target "
            + self._target
            + " -trees "
            + str(self._n_trees)
            + " -aucJarPath "
            + self._auc_jar
            + " > "
            + str(self._here.joinpath(self._test_log))
            + " 2>&1"
        )

        print(_CALL)
