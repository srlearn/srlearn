# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""Handler for file system operations on behalf of BoostSRL."""

from enum import Enum
from enum import unique
import pathlib
import shutil


class FileSystem:
    """BoostSRL File System

    BoostSRL has an implicit assumption that it has access to a file system. At runtime
    it needs to both read and write with files. This object provides a view into the
    files needed, requests files from the operating system, and (most importantly)
    prepares and cleans up the file system at allocation/de-allocation time.

    Examples
    --------

    This first example may not appear to do much, but behind the scenes it is
    creating directories for each instance of ``FileSystem``, and removing
    them upon ``exit()``.

    >>> from boostsrl.system_manager import FileSystem
    >>> systems = []
    >>> for _ in range(5):
    ...     systems.append(FileSystem())

    Notes
    -----

    Ideally, each instance of a :class:`boostsrl.rdn.RDN` should have its own directory
    where it can operate independently. But this can be problematic and will often
    lead to duplicated data and other problems if multiple models are learned in
    parallel on the same database.

    Another option (which may be more suited to parallel tree learning) would be to
    store data in a single location, but write the log files and models to separate
    locations.

    Attributes
    ----------
    files : :class:`enum.Enum`
        Enum providing key,value pairs for a BoostSRL database
    """

    # TODO: Resistance to concurrency, race conditions, and asynchronous problems.

    # Prefix is the master directory that all databases will reside in.
    # In case of failure, this directory should be safe to delete.
    boostsrl_data_directory = "bsrl_data"

    def __init__(self):
        """Initialize a BoostSRL File System.

        This will create directories that are cleaned up when the instance
        is de-allocated.
        """

        _here = pathlib.Path(__file__).parent

        # Allocate a location where data can safely be stored.
        _data = _here.joinpath(FileSystem.boostsrl_data_directory)
        _allotment_number = self._allocate_space(_data)
        _directory = _data.joinpath("data" + str(_allotment_number))

        @unique
        class Files(Enum):
            DIRECTORY = _directory
            BOOST_JAR = _here.joinpath("v1-0.jar")
            AUC_JAR = _here
            TRAIN_LOG = _directory.joinpath("train_output.txt")
            TEST_LOG = _directory.joinpath("test_output.txt")
            TRAIN_DIR = _directory.joinpath("train")
            TEST_DIR = _directory.joinpath("test")
            MODELS_DIR = _directory.joinpath("train/models/")
            TREES_DIR = _directory.joinpath("train/models/bRDNs/Trees")

        # Create directories
        Files.TRAIN_DIR.value.mkdir()
        Files.TEST_DIR.value.mkdir()

        self.files = Files

    def __del__(self):
        """Clean up the file system on object de-allocation."""
        shutil.rmtree(self.files.DIRECTORY.value)

    @staticmethod
    def _allocate_space(current_directory) -> int:
        """Attempt to allocate directory `data{n}`, increment until success.

        Returns
        -------
        _postfix : int
            The number corresponding to the allocated directory.
        """
        _postfix = 0
        while True:
            _attempt = current_directory.joinpath("data" + str(_postfix))
            if not _attempt.exists():
                _attempt.mkdir(parents=True)
                break
            else:
                _postfix += 1
        return _postfix
