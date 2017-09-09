"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from second_shooter.second_shooter import shutter_value


def test_shutter_value_fraction():
    """Test fractional shutter value (1/N)"""
    shutter = shutter_value('1/4')

    assert shutter == 0.25


def test_shutter_value_decimal():
    """Test decimal shutter value (N.NNNN)"""
    shutter = shutter_value('0.25')

    assert shutter == 0.25


def test_number_shutter_value():
    """Test integer shutter value (N)"""
    shutter = shutter_value(1)

    assert shutter == 1.0

    shutter = shutter_value(0.25)

    assert shutter == 0.25
