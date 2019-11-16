"""Test for the show_versions helper. Based on the sklearn tests."""
# Author: Alexander L. Hayes <hayesall@iu.edu>
# License: MIT

from srlearn.utils._show_versions import _get_deps_info
from srlearn.utils._show_versions import show_versions


DEPENDENCIES = ["srlearn", "pip", "setuptools", "sklearn", "numpy", "scipy"]


def test_get_missing_deps_inf():
    """Check that something is produced when a package doesn't exist."""
    _deps_info = _get_deps_info(["bad_package_name", "srlearn"])
    assert "srlearn" in _deps_info
    assert "bad_package_name" in _deps_info


def test_get_deps_info():
    """Assert that strings are in the output of _get_deps_info()"""
    _deps_info = _get_deps_info(DEPENDENCIES)
    assert "srlearn" in _deps_info
    assert "pip" in _deps_info
    assert "setuptools" in _deps_info
    assert "sklearn" in _deps_info
    assert "numpy" in _deps_info
    assert "scipy" in _deps_info


def test_show_versions_no_github(capsys):
    """Assert that strings are in the output when github=False"""
    show_versions(github=False)
    out, _ = capsys.readouterr()
    assert "python" in out
    assert "executable" in out
    assert "machine" in out
    assert "srlearn" in out
    assert "pip" in out
    assert "setuptools" in out
    assert "sklearn" in out
    assert "numpy" in out
    assert "scipy" in out


def test_show_versions_github(capsys):
    """Assert that GitHub markdown is wrapped when github=True"""
    show_versions(github=True)
    out, _ = capsys.readouterr()
    assert "<details><summary>System and Dependency Information</summary>" in out
    assert "**System Information**" in out
    assert "* python" in out
    assert "* executable" in out
    assert "* machine" in out
    assert "**Python Dependencies**" in out
    assert "* srlearn" in out
    assert "* pip" in out
    assert "* setuptools" in out
    assert "* sklearn" in out
    assert "* numpy" in out
    assert "* scipy" in out
    assert "</details>" in out
