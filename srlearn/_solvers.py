# Copyright © 2017-2022 Alexander L. Hayes

import re
import subprocess
import numpy as np

from .background import Background
from .database import Database
from .system_manager import FileSystem

# Solver knows about FileSystems and can call shell commands.
# Classifiers should not know about the FileSystem, but can get results indirectly through Solvers.

class Solver:
    # Must implement `learn` and `infer`

    def __init__(
        self,
        *,
        background: Background = None,
        neg_pos_ratio: float = 2.0,
        n_estimators: int = 10,
        target: str = "None",
    ):
        self.background = background
        self.n_estimators = n_estimators
        self.neg_pos_ratio = neg_pos_ratio
        self.target = target

        # These are filled when a solver learn/infer runs.
        self.file_system = None
        self.dotfiles = None
        self.estimators_ = None
        self.threshold_ = None
        self.predictions_ = None
        self.predictions_probs_ = None
        self.classes_ = None

    def learn(self):
        raise NotImplementedError

    def infer(self):
        raise NotImplementedError

    def before_learn(self, database: Database) -> None:

        # TODO(hayesall): Move validation into here before allocating a FileSystem.

        self.file_system = FileSystem()
        self.background.write(filename="train", location=self.file_system.files.TRAIN_DIR)
        database.write(filename="train", location=self.file_system.files.TRAIN_DIR)

    def after_learn(self) -> None:
        self.get_estimators()
        self.get_dotfiles()

    def before_infer(self, database: Database) -> None:
        self.background.write(filename="test", location=self.file_system.files.TEST_DIR)
        database.write(filename="test", location=self.file_system.files.TEST_DIR)

    def after_infer(self) -> None:
        self.get_threshold()
        self.get_results()

    def get_results(self) -> None:
        _results_db = self.file_system.files.TEST_DIR.joinpath(
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
        _pred_prob = np.concatenate((_pos, 1 - _neg), axis=0)
        _pred = np.greater(_pred_prob, self.threshold_)

        self.classes_ = _classes
        self.predictions_probs_ = _pred_prob
        self.predictions_ = _pred

    def get_dotfiles(self):
        dotfiles = []
        for i in range(self.n_estimators):
            with open(
                self.file_system.files.DOT_DIR.joinpath(
                    "WILLTreeFor_" + self.target + str(i) + ".dot"
                )
            ) as _fh:
                dotfiles.append(_fh.read())
        self.dotfiles = dotfiles

    def get_estimators(self):
        _estimators = []
        for _tree_number in range(self.n_estimators):
            with open(
                self.file_system.files.TREES_DIR.joinpath(
                    "{0}Tree{1}.tree".format(self.target, _tree_number)
                )
            ) as _fh:
                _estimators.append(_fh.read())
        self.estimators_ = _estimators

    def get_threshold(self):
        with open(self.file_system.files.TEST_LOG, "r") as _fh:
            _threshold = re.findall("% Threshold = \\d*.\\d*", _fh.read())
        self.threshold_ = float(_threshold[0].split(" = ")[1])

    @staticmethod
    def call(shell_command):
        _pid = subprocess.Popen(shell_command, shell=True)
        _status = _pid.wait()
        if _status != 0:
            raise RuntimeError(
                "Error when running shell command: {0}".format(shell_command)
            )


class BoostSRL_RDN_Solver(Solver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def learn(self):
        _call = (
            "java -jar "
            + str(self.file_system.files.BOOSTSRL_BACKEND)
            + " -l -combine -train "
            + str(self.file_system.files.TRAIN_DIR)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -negPosRatio "
            + str(self.neg_pos_ratio)
            + " > "
            + str(self.file_system.files.TRAIN_LOG)
        )
        self.call(_call)

    def infer(self):
        _call = (
            "java -jar "
            + str(self.file_system.files.BOOSTSRL_BACKEND)
            + " -i -test "
            + str(self.file_system.files.TEST_DIR)
            + " -model "
            + str(self.file_system.files.MODELS_DIR)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + str(self.file_system.files.AUC_JAR)
            + " > "
            + str(self.file_system.files.TEST_LOG)
        )
        self.call(_call)

class SRLBoost_RDN_Solver(Solver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def learn(self):
        _call = (
            "java -jar "
            + str(self.file_system.files.SRLBOOST_BACKEND)
            + " -l -train "
            + str(self.file_system.files.TRAIN_DIR)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -negPosRatio "
            + str(self.neg_pos_ratio)
            + " > "
            + str(self.file_system.files.TRAIN_LOG)
        )
        self.call(_call)

    def infer(self):
        _call = (
            "java -jar "
            + str(self.file_system.files.SRLBOOST_BACKEND)
            + " -i -test "
            + str(self.file_system.files.TEST_DIR)
            + " -model "
            + str(self.file_system.files.MODELS_DIR)
            + " -target "
            + self.target
            + " -trees "
            + str(self.n_estimators)
            + " -aucJarPath "
            + str(self.file_system.files.AUC_JAR)
            + " > "
            + str(self.file_system.files.TEST_LOG)
        )
        self.call(_call)
