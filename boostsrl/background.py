# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
background.py
"""


class Background:
    """Background Knowledge for a database.

    Background knowledge expressed in the form of modes.
    """

    # TODO: Some parameters that would normally be in the background file might
    #  make more sense as classifier parameters. e.g.: maxTreeDepth,
    #  nodeSize, numOfClauses

    def __init__(self, modes=None, recursion=False, line_search=False):
        """Initialize a set of background knowledge

        Parameters
        ----------
        modes : None or list of str
            Modes constrain the search space for hypotheses. If None, this will
            attempt to set the
            modes automatically at learning time (default: None)
        line_search : bool, optional
            Use lineSearch (default: False)
        recursion : bool, optional
            Use recursion (default: False)
        """
        self.modes = modes
        self.line_search = line_search
        self.recursion = recursion

        # Check params are correct.
        self._check_params()

    def _check_params(self):
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

    def write(self, location="train") -> None:
        """Write the background to disk for learning.

        Parameters
        ----------
        location : str
            This should be handled by a manager to ensure locations do not overlap.
        """
        return

    def __str__(self):
        return "Modes()"

    def __repr__(self):
        return self.__str__()
