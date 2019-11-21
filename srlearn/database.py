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

>>> from srlearn.database import Database
>>> db = Database()
>>> db.add_pos("student(alexander).")
>>> db.add_neg("student(sriraam).")
>>> db.add_fact("advises(alexander, sriraam).")

Create an instance of the database from an existing set of files.

>>> from srlearn.database import Database
>>> db = Database()
"""

from shutil import copyfile
import pathlib


class Database:
    """Database of examples and facts."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """Initialize a Database object

        A database (in this respect) contains positive examples, negative examples,
        facts, and is augmented with background knowledge.

        The implementation is done with four attributes: ``pos``, ``neg``,
        ``facts``, and ``modes``. Each attribute is a list that may be set by
        mutating, or loaded from files with :func:`Database.from_files`.

        Examples
        --------

        This initializes a Database object, then sets the ``pos`` attribute.

        >>> from srlearn import Database
        >>> db = Database()
        >>> db.pos = ["student(alexander)."]
        """
        self.pos = []
        self.neg = []
        self.facts = []
        self.modes = []

    def write(self, filename="train", location=pathlib.Path("train")) -> None:
        """Write the database to disk

        Parameters
        ----------
        filename : str
            Name of the file to write to: 'train' or 'test'
        location : :class:`pathlib.Path`
            Path where data should be written to.

        Notes
        -----

        This function has polymorphic behavior. When attributes (``self.pos``,
        ``self.neg``, ``self.facts``) are lists of strings, the lists are
        written to files. When the attributes are (path-like) strings or
        pathlib Paths (:class:`pathlib.Path`), the files are copied.
        """

        def _write(_filename, _location, _object, _type):
            if isinstance(_object, list):
                with open(
                    _location.joinpath("{0}_{1}.txt".format(_filename, _type)), "w"
                ) as _fh:
                    for example in _object:
                        _fh.write(example + "\n")
            else:
                copyfile(
                    str(_object),
                    str(_location.joinpath("{0}_{1}.txt".format(_filename, _type))),
                )

        _write(filename, location, self.pos, "pos")
        _write(filename, location, self.neg, "neg")
        _write(filename, location, self.facts, "facts")

    def __repr__(self) -> str:
        return (
            "Positive Examples:\n"
            + str(self.pos)
            + "\nNegative Examples:\n"
            + str(self.neg)
            + "\nFacts:\n"
            + str(self.facts)
        )

    @staticmethod
    def from_files(pos="pos.pl", neg="neg.pl", facts="facts.pl", lazy_load=True):
        """Load files into a Database

        Return an instance of a Database with pos, neg, and facts set to the
        contents of files. By default this performs a "lazy load," where the
        files are not loaded into Python lists, but copied at learning time.

        Parameters
        ----------
        pos : str or pathlib.Path
            Location of positive examples
        neg : str or pathlib.Path
            Location of negative examples
        facts : str or pathlib.Path
            Location of facts
        lazy_load : bool (default: True)
            Skip loading the files into a list

        Returns
        -------
        db : srlearn.Database
            Instance of a Database object
        """

        _db = Database()

        if lazy_load:
            _db.pos = pos
            _db.neg = neg
            _db.facts = facts
        else:
            with open(pos, "r") as _fh:
                _db.pos = _fh.read().splitlines()
            with open(neg, "r") as _fh:
                _db.neg = _fh.read().splitlines()
            with open(facts, "r") as _fh:
                _db.facts = _fh.read().splitlines()

        return _db

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
