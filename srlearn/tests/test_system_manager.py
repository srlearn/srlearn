# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Tests for srlearn.system_manager.FileSystem
"""


from srlearn.system_manager import FileSystem


def test_initialize_file_system():
    """Test initializing a FileSystem()"""
    system0 = FileSystem()
    _location = system0.files.DIRECTORY.value

    assert _location.exists()
    del system0
    assert not _location.exists()


def test_initialize_two_systems():
    """Test initializing multiple FileSystem()"""
    system0 = FileSystem()
    system1 = FileSystem()

    _location0 = system0.files.DIRECTORY.value
    _location1 = system1.files.DIRECTORY.value

    assert _location0.exists()
    assert _location1.exists()

    del system0
    del system1

    assert not _location0.exists()
    assert not _location1.exists()


def test_system_train_test_dirs():
    """Test that train/test directories are created."""
    system0 = FileSystem()

    _location = system0.files.DIRECTORY.value
    _train_location = system0.files.TRAIN_DIR.value
    _test_location = system0.files.TEST_DIR.value

    assert _train_location.exists()
    assert _test_location.exists()

    del system0

    assert not _location.exists()
