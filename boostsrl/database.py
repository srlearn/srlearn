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

    def __init__(self):
        self.pos = []
        self.neg = []
        self.facts = []
        self.modes = []

    def write(self, filename="train", location=pathlib.Path("train")) -> None:
        """
        Write the database to disk.

        Parameters
        ----------
        filename : str
            Name of the file to write to: 'train' or 'test'
        location : :class:`pathlib.Path`
            Path where data should be written to.
        """

        # TODO: Different behavior will be necessary if the files are already
        #       stored on disk: they can be copied to self.location
        #       with sys

        with open(location.joinpath("{0}_pos.txt".format(filename)), "w") as _fh:
            for pos_example in self.pos:
                _fh.write(str(pos_example) + "\n")

        with open(location.joinpath("{0}_neg.txt".format(filename)), "w") as _fh:
            for neg_example in self.neg:
                _fh.write(str(neg_example) + "\n")

        with open(location.joinpath("{0}_facts.txt".format(filename)), "w") as _fh:
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
