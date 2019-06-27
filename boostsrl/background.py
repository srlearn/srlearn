# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
background.py
"""

import pathlib


class Background:
    """Background Knowledge for a database.

    Background knowledge expressed in the form of modes.
    """

    # TODO: Some parameters that would normally be in the background file might
    #  make more sense as classifier parameters. e.g.: maxTreeDepth,
    #  nodeSize, numOfClauses

    # TODO:
    #   - precomputes
    #   - bridgers
    #   - useStdLogicVariables
    #   - usePrologVariables
    #   - okIfUnknown
    #   - range

    # pylint: disable=too-many-instance-attributes,too-many-arguments

    def __init__(
        self,
        modes=None,
        node_size=2,
        number_of_clauses=100,
        number_of_cycles=100,
        max_tree_depth=3,
        recursion=False,
        line_search=False,
        use_std_logic_variables=False,
        use_prolog_variables=False,
        load_all_libraries=False,
        load_all_basic_modes=False,
    ):
        """Initialize a set of background knowledge

        Parameters
        ----------
        modes : list of str (default: None)
            Modes constrain the search space for hypotheses. If None, this will
            attempt to set the modes automatically at learning time.
        node_size : int, optional (default: 2)
            Maximum number of literals in each node.
        max_tree_depth : int, optional (default: 3)
            Maximum number of nodes from root to leaf (height) in the tree.
        number_of_clauses : int, optional (default: 100)
            Maximum number of clauses in the tree (i.e. maximum number of leaves)
        number_of_cycles : int, optional (default: 100)
            Maximum number of times the code will loop to learn clauses,
            increments even if no new clauses are learned.
        line_search : bool, optional (default: False)
            Use lineSearch
        recursion : bool, optional (default: False)
            Use recursion
        use_std_logic_variables : bool, optional (default: False)
            Set the stdLogicVariables parameter to True
        use_prolog_variables : bool, optional (default: False)
            Set the usePrologVariables parameter to True
        load_all_libraries : bool, optional (default: False)
            Load libraries: ``arithmeticInLogic``, ``comparisonInLogic``,
            ``differentInLogic``, ``listsInLogic``
        load_all_basic_modes : bool, optional (default: False)
            Load ``modes_arithmeticInLogic``, ``modes_comparisonInLogic``,
            ``modes_differentInLogic``, ``modes_listsInLogic``
            These may require many cycles while proving.

        Examples
        --------

        This demonstrates how to add parameters to the Background object.
        The main thing to take note of is the ``modes`` parameter, where
        background knowledge of the Toy-Cancer domain is specified.

        >>> from boostsrl import Background
        >>> bk = Background(
        ...     modes=[
        ...         "cancer(+Person).",
        ...         "smokes(+Person).",
        ...         "friends(+Person,-Person).",
        ...         "friends(-Person,+Person).",
        ...     ],
        ...     max_tree_depth=2,
        ...     use_std_logic_variables=True,
        ... )
        >>> print(bk)
        setParam: nodeSize=2.
        setParam: maxTreeDepth=2.
        setParam: numberOfClauses=100.
        setParam: numberOfCycles=100.
        useStdLogicVariables: true.
        mode: cancer(+Person).
        mode: smokes(+Person).
        mode: friends(+Person,-Person).
        mode: friends(-Person,+Person).
        <BLANKLINE>

        This Background object is used by the :class:`boostsrl.rdn.RDN` class to
        write the parameters to a ``background.txt`` file before running BoostSRL.

        .. code-block:: python

            >>> from boostsrl import Background
            >>> from boostsrl import example_data
            >>> bk = Background(
            ...     modes=example_data.train.modes,
            ...     max_tree_depth=2,
            ...     node_size=1,
            ... )
            >>> bk.write("training/")

        Notes
        -----

        Descriptions of these parameters are lifted almost word-for-word from the
        BoostSRL-Wiki "Advanced Parameters" page [1]_.

        Some of these parameters are defined in multiple places. This is mostly
        to follow the sklearn-style requirement for all tune-able parameters to
        be part of the object while still being relatively similar to the
        style where BoostSRL has parameters defined in a modes file.

        .. [1] https://starling.utdallas.edu/software/boostsrl/wiki/advanced-parameters/
        """
        self.modes = modes
        self.node_size = node_size
        self.max_tree_depth = max_tree_depth
        self.number_of_clauses = number_of_clauses
        self.number_of_cycles = number_of_cycles
        self.line_search = line_search
        self.recursion = recursion
        self.use_std_logic_variables = use_std_logic_variables
        self.use_prolog_variables = use_prolog_variables
        self.load_all_libraries = load_all_libraries
        self.load_all_basic_modes = load_all_basic_modes

        # Check params are correct at the tail of initialization.
        self._check_params()

    def _check_params(self) -> None:
        """Check validity of background knowledge, raise ValueError if invalid."""
        if not (isinstance(self.modes, list) or self.modes is None):
            raise ValueError(
                "modes parameter should be None or a list, found {0}".format(self.modes)
            )
        if not isinstance(self.line_search, bool):
            raise ValueError(
                "line_search parameter should be bool, found {0}".format(
                    self.line_search
                )
            )
        if not isinstance(self.recursion, bool):
            raise ValueError(
                "recursion parameter should be a bool, found {0}".format(self.recursion)
            )
        if not isinstance(self.max_tree_depth, int) or isinstance(
            self.max_tree_depth, bool
        ):
            raise ValueError(
                "max_tree_depth should be an int, found {0}".format(self.max_tree_depth)
            )
        if self.max_tree_depth <= 0:
            raise ValueError(
                "max_tree_depth must be greater than 0, found {0}".format(
                    self.max_tree_depth
                )
            )
        if not isinstance(self.number_of_clauses, int) or isinstance(
            self.number_of_clauses, bool
        ):
            raise ValueError(
                "number_of_clauses must be an int, found {0}".format(
                    self.number_of_clauses
                )
            )
        if self.number_of_clauses <= 0:
            raise ValueError(
                "number_of_clauses must be greater than 0, found {0}".format(
                    self.number_of_clauses
                )
            )
        if not isinstance(self.number_of_cycles, int) or isinstance(
            self.number_of_cycles, bool
        ):
            raise ValueError(
                "number_of_cycles must be an int, found {0}".format(
                    self.number_of_cycles
                )
            )
        if self.number_of_cycles <= 0:
            raise ValueError(
                "number_of_cycles must be greater than 0, found {0}".format(
                    self.number_of_cycles
                )
            )
        if not isinstance(self.load_all_libraries, bool):
            raise ValueError(
                "load_all_libraries should be a bool, found {0}".format(
                    self.load_all_libraries
                )
            )
        if not isinstance(self.load_all_basic_modes, bool):
            raise ValueError(
                "load_all_basic_modes should be a bool, found {0}".format(
                    self.load_all_basic_modes
                )
            )
        if not isinstance(self.use_std_logic_variables, bool):
            raise ValueError(
                "use_std_logic_variables should be a bool, found {0}".format(
                    self.use_std_logic_variables
                )
            )
        if not isinstance(self.use_prolog_variables, bool):
            raise ValueError(
                "use_prolog_variables should be a bool, found {0}".format(
                    self.use_prolog_variables
                )
            )

    def write(self, filename="train", location=pathlib.Path("train")) -> None:
        """Write the background to disk for learning.

        Parameters
        ----------
        filename : str
            Name of the file to write to: 'train_bk.txt' or 'test_bk.txt'
        location : :class:`pathlib.Path`
            This should be handled by a manager to ensure locations do not overlap.
        """

        with open(location.joinpath("{0}_bk.txt".format(filename)), "w") as _fh:
            _fh.write(str(self))

    def _to_background_string(self) -> str:
        """Convert self to a string.

        This converts the Background object to use the background/mode syntax used
        by BoostSRL. Normally this will be accessed via the public __str__ method
        or __repr__ method.

        Parameters
        ----------
        self : object
            Instance of a Background object.

        Returns
        -------
        self : str
            A string representation of the Background object.

        Notes
        -----

        This method is based on the description and examples from the
        BoostSRL-Wiki "Basic Modes Guide" [1]_.

        .. [1] https://starling.utdallas.edu/software/boostsrl/wiki/basic-modes/
        """
        _relevant = [
            [_attr, _val]
            for _attr, _val in self.__dict__.items()
            if (_val is not False) and (_val is not None)
        ]

        _background_syntax = {
            "line_search": "setParam: lineSearch={0}.\n",
            "recursion": "setParam: recursion={0}.\n",
            "node_size": "setParam: nodeSize={0}.\n",
            "max_tree_depth": "setParam: maxTreeDepth={0}.\n",
            "number_of_clauses": "setParam: numberOfClauses={0}.\n",
            "number_of_cycles": "setParam: numberOfCycles={0}.\n",
            "load_all_libraries": "setParam: loadAllLibraries = {0}.\n",
            "load_all_basic_modes": "setParam: loadAllBasicModes = {0}.\n",
            "use_std_logic_variables": "useStdLogicVariables: {0}.\n",
            "use_prolog_variables": "usePrologVariables: {0}.\n",
        }

        _background = ""
        for _attr, _val in _relevant:
            if _attr in ["modes"]:
                pass
            else:
                _background += _background_syntax[_attr].format(str(_val).lower())

        if self.modes:
            for _mode in self.modes:
                _background += "mode: " + _mode + "\n"

        return _background

    def __str__(self) -> str:
        return self._to_background_string()

    def __repr__(self) -> str:
        return self._to_background_string()
