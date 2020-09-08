# Copyright 2020 Alexander L. Hayes

"""
Parsing trees written by BoostSRL / SRLBoost
"""


def _parse_std_logic_expression(tree):

    _features = []

    for line in tree.splitlines():
        if "=>" in line:

            _lhs = line.split("=>")[0]

            if "^" in _lhs:
                for _portion in _lhs.split("^"):
                    if not _portion.split("(")[0]:
                        _features += [_portion.split("(")[1].replace(" ", "")]
                    else:
                        _features += [_portion.split("(")[0].replace(" ", "")]
            else:
                _features += [line.split("(")[1]]

    return _features


def _parse_prolog_expression(tree):

    _features = []

    for line in tree.splitlines():
        if ":-" in line:

            _rhs = line.split(":-")[1]

            if "^" in _rhs:
                for _portion in _rhs.split("^"):
                    if not _portion.split("(")[0]:
                        _features += [_portion.split("(")[1].replace(" ", "")]
                    else:
                        _features += [_portion.split("(")[0].replace(" ", "")]
            else:
                for _portion in _rhs.split(" "):
                    if "(" in _portion:
                        _features += [_portion.split("(")[0]]

    return _features


def parse_tree(tree, use_prolog_variables=True):
    """Extract variables used for splits in classification.

    Parameters
    ----------

    tree : str
        Model representation produced by BoostSRL / SRLBoost
    """
    if use_prolog_variables:
        features = _parse_prolog_expression(tree)
    else:
        features = _parse_std_logic_expression(tree)
    return features
