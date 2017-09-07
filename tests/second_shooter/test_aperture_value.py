"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from second_shooter.second_shooter import aperture_value


def test_aperture_value_canon():
    assert aperture_value('5.6') == 5.6
    assert aperture_value('8') == 8.0


def test_aperture_value_nikon():
    assert aperture_value('f/5.6') == 5.6
    assert aperture_value('f/8') == 8.0
