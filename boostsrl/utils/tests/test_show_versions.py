"""Test for the show_versions helper. Based on the sklearn tests."""
# Author: Alexander L. Hayes <hayesall@iu.edu>
# License: MIT

from boostsrl.utils._show_versions import _get_deps_info
from boostsrl.utils._show_versions import show_versions


_dependencies = [
    "boostsrl",
    "pip",
    "setuptools",
    "sklearn",
    "numpy",
    "scipy",
]


def test_get_missing_deps_inf():
    _deps_info = _get_deps_info(["bad_package_name", "boostsrl"])
    assert "boostsrl" in _deps_info
    assert "bad_package_name" in _deps_info


def test_get_deps_info():
    _deps_info = _get_deps_info(_dependencies)
    assert "boostsrl" in _deps_info
    assert "pip" in _deps_info
    assert "setuptools" in _deps_info
    assert "sklearn" in _deps_info
    assert "numpy" in _deps_info
    assert "scipy" in _deps_info


def test_show_versions_default(capsys):
    show_versions(github=False)
    out, err = capsys.readouterr()
    assert "python" in out
    assert "executable" in out
    assert "machine" in out
    assert "macros" in out
    assert "lib_dirs" in out
    assert "cblas_libs" in out
    assert "boostsrl" in out
    assert "pip" in out
    assert "setuptools" in out
    assert "sklearn" in out
    assert "numpy" in out
    assert "scipy" in out


def test_show_versions_github(capsys):
    show_versions(github=True)
    out, err = capsys.readouterr()
    assert "<details><summary>System, BLAS, and Dependencies</summary>" in out
    assert "**System Information**" in out
    assert "* python" in out
    assert "* executable" in out
    assert "* machine" in out
    assert "**BLAS**" in out
    assert "* macros" in out
    assert "* lib_dirs" in out
    assert "* cblas_libs" in out
    assert "**Python Dependencies**" in out
    assert "* boostsrl" in out
    assert "* pip" in out
    assert "* setuptools" in out
    assert "* sklearn" in out
    assert "* numpy" in out
    assert "* scipy" in out
    assert "</details>" in out
