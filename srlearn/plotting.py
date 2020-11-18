# Copyright © 2020 Alexander L. Hayes

"""
Methods for plotting and visualization.
"""

from .base import BaseBoostedRelationalModel


def create_tree_digraph(booster, tree_index=0, out_file=None):
    """Create a digraph representation of a tree.

    Parameters
    ----------
    booster : BaseBoostedRelationalModel
        Model to create a tree from
    tree_index : int
        Index of the tree to visualize
    out_file : str, pathlike, or None
        Handle or name of the output file. If ``None``, returns a string
    """

    if not isinstance(booster, BaseBoostedRelationalModel):
        raise TypeError("booster must inherit from BaseBoostedRelationalModel.")
    dotfiles = booster._dotfiles

    if not (0 <= tree_index < len(dotfiles)):
        raise IndexError("tree_index is out of range.")

    if out_file:
        with open(out_file, "w") as _fh:
            _fh.write(dotfiles[tree_index])
    else:
        return dotfiles[tree_index]
