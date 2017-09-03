"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import pytest

from second_shooter.second_shooter import SecondShooter


@pytest.fixture
def shooter():
    shooter = SecondShooter('Nikon', 'port')
    return shooter