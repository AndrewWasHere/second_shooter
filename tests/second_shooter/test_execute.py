"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import pytest

from second_shooter.second_shooter import execute


def test_execute_gphoto2():
    """Test execute with gphoto2 command line."""
    result = execute('gphoto2 -v')

    assert result.returncode == 0


def test_execute_bad_argument():
    """Test execute with a bad argument to the command."""
    result = execute('gphoto2 --not-a-valid-argument')

    assert result.returncode == 1


def test_execute_bad_command():
    """Test execute with a bad command."""
    with pytest.raises(Exception):
        execute('')

    with pytest.raises(Exception):
        execute('qwejlkzdx')
