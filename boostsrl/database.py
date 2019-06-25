# Copyright 2017, 2018, 2019 Alexander L. Hayes

"""
database.py

A BoostSRL database consists of positive examples, negative examples, and facts;
all of which need to be stored as .txt files on a file system.

Use Cases
---------

- Creating an instance of the database through code (write to location)
- Files already stored on the filesystem (copy to location)
- Examples stored in a RDBMS?

Examples
--------

Create a new instance of a database, add examples, and write them to the filesystem.

>>> from boostsrl.database import Database
>>> db = Database()
>>> db.add_pos("student(alexander).")
>>> db.add_neg("student(sriraam).")
>>> db.add_fact("advises(alexander, sriraam).")

Create an instance of the database from an existing set of files.

>>> from boostsrl.database import Database
>>> db = Database()
"""

import pathlib


class Database:
    """Database of examples and facts.

    A database (in this respect) contains positive examples, negative examples,
    facts, and augmented with background knowledge.
    """

    # pylint: disable=too-many-instance-attributes

    # TODO: Currently disabling linter warnings, trimming attributes may be wise
    #       e.g. file_prefix and target should typically be the same variable

    def __init__(self, target="None", location="bsrl_data"):
        self.pos = []
        self.neg = []
        self.facts = []
        self.modes = []

        self.location = location
        self.file_prefix = target

        self._target = target
        self._n_trees = 10
        self._trees = []

    @property
    def target(self) -> str:
        """
        Target predicate for learning and inference.

        Examples:

        >>> from boostsrl.database import Database
        >>> db = Database()
        >>> db.target
        'None'
        >>> db.target = "student"
        >>> db.target
        'student'
        """
        return self._target

    @target.setter
    def target(self, target: str) -> None:
        if not isinstance(target, str):
            raise Exception("Target must be a string.")
        self._target = target

    @property
    def trees(self) -> int:
        """
        Number of trees that will be learned to represent the concept.
        """
        return self._n_trees

    @trees.setter
    def trees(self, n_trees: int) -> None:
        if not isinstance(n_trees, int):
            raise Exception("Tree must be an integer.")
        self._n_trees = n_trees

    def write(self, location="train/") -> None:
        """
        Write the database to disk.
        """

        # TODO: Different behavior will be necessary if the files are already
        #       stored on disk: they can be copied to self.location
        #       with sys

        self.location = pathlib.Path(location)

        if not self.location.exists():
            self.location.mkdir(parents=True, exist_ok=True)

        self.file_prefix = self.location.parts[-1]

        with open(
            self.location.joinpath("{0}_pos.txt".format(self.file_prefix)), "w"
        ) as _fh:
            for pos_example in self.pos:
                _fh.write(str(pos_example) + "\n")

        with open(
            self.location.joinpath("{0}_neg.txt".format(self.file_prefix)), "w"
        ) as _fh:
            for neg_example in self.neg:
                _fh.write(str(neg_example) + "\n")

        with open(
            self.location.joinpath("{0}_facts.txt".format(self.file_prefix)), "w"
        ) as _fh:
            for fact in self.facts:
                _fh.write(str(fact) + "\n")

    def __repr__(self) -> str:
        return (
            "Positive Examples:\n"
            + str(self.pos)
            + "\nNegative Examples:\n"
            + str(self.neg)
            + "\nFacts:\n"
            + str(self.facts)
        )

    def add_pos(self, example: str) -> None:
        """
        Append a positive example to the list of positive examples.
        """
        self.pos.append(example)

    def add_neg(self, example: str) -> None:
        """
        Append a negative example to the list of negative examples.
        """
        self.neg.append(example)

    def add_fact(self, example: str) -> None:
        """
        Append a fact to the list of facts.
        """
        self.facts.append(example)
