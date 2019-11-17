# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.system_manager.reset
"""

import pathlib
from srlearn import system_manager


def test_soft_reset():
    """Test performing a soft reset."""
    result = system_manager.reset(soft=True)
    assert result == []


def test_soft_reset_with_dirs():
    """Soft reset when the directory is non-empty."""
    _dir = pathlib.Path(system_manager.__file__).parent
    _there = _dir.joinpath(system_manager.FileSystem.boostsrl_data_directory)
    _there.joinpath("data1").mkdir(parents=True)
    _there.joinpath("data2").mkdir(parents=True)

    result = system_manager.reset(soft=True)
    assert sorted(result) == sorted(["data1", "data2"])
    result = system_manager.reset()
    assert result == []
    result = system_manager.reset(soft=True)
    assert result == []


def test_hard_reset():
    """Hard reset should return []"""
    result = system_manager.reset(soft=False)
    assert result == []
    result = system_manager.reset()
    assert result == []
