"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import pytest

from second_shooter.second_shooter import aperture_index


@pytest.fixture
def apertures():
    return [5.6, 8.0, 11.0]


def test_aperture_index_equal(apertures):
    """Test aperture equal to an index aperture."""
    assert aperture_index(5.6, apertures) == 0
    assert aperture_index(8, apertures) == 1
    assert aperture_index(11, apertures) == 2


def test_aperture_index_less_than(apertures):
    """Test closest aperture is above value."""
    assert aperture_index(0, apertures) == 0
    assert aperture_index(7, apertures) == 1
    assert aperture_index(10, apertures) == 2


def test_aperture_index_greater_than(apertures):
    """Test closest aperture is below value."""
    assert aperture_index(6, apertures) == 0
    assert aperture_index(8.5, apertures) == 1
    assert aperture_index(12, apertures) == 2
