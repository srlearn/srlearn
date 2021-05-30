# Copyright © 2020 Alexander L. Hayes

"""
Methods for plotting and visualization.
"""

from .base import BaseBoostedRelationalModel


class _GVPlotter:
    def __init__(self, dot_string):
        self.dot_string = dot_string
    def _repr_html_(self):
        import graphviz
        return graphviz.Source(self.dot_string)._repr_svg_()


def plot_digraph(dot_string, format="png"):
    """Plot a digraph as an image.

    Parameters
    ----------
    dot_string : str
        String representing a dot
    format : str
        Format passed to Source (default: ``png``)

    Returns
    -------
    source : graphviz.files.Source
        Graphviz ``Source`` object
    """
    try:
        import graphviz
    except ImportError as excep:
        raise ImportError("graphviz needs to be available to plot_digraph") from excep
    from graphviz import Source
    if format == "html":
        return _GVPlotter(dot_string)
    return Source(dot_string, format=format)


def export_digraph(booster, tree_index=0, out_file=None):
    """Create a digraph representation of a tree.

    Parameters
    ----------
    booster : BaseBoostedRelationalModel
        Model to create a tree from
    tree_index : int
        Index of the tree to visualize
    out_file : str, pathlike, or None
        Handle or name of the output file. If ``None``, returns a string

    Examples
    --------

    This can be used in two ways: returning a string, or directly writing the
    result to a file.

    .. code-block:: python

        from srlearn.rdn import BoostedRDN
        from srlearn import Background
        from srlearn import example_data
        from srlearn.plotting import export_digraph

        bkg = Background(
            modes=example_data.train.modes,
        )

        clf = BoostedRDN(
            background=bkg,
            target="cancer",
        )

        clf.fit(example_data.train)

        print(export_digraph(clf, tree_index=0))
    """

    if not isinstance(booster, BaseBoostedRelationalModel):
        raise TypeError("booster must inherit from BaseBoostedRelationalModel.")
    dotfiles = booster._dotfiles

    if not 0 <= tree_index < len(dotfiles):
        raise IndexError("tree_index is out of range.")

    if out_file:
        with open(out_file, "w") as _fh:
            _fh.write(dotfiles[tree_index])
    else:
        return dotfiles[tree_index]
