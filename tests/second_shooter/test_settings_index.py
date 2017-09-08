"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import pytest

from second_shooter.second_shooter import settings_index


@pytest.fixture
def settings():
    """Test settings."""
    return [5.6, 8.0, 11.0]


def test_settings_index_equal(settings):
    """Test aperture equal to an index aperture."""
    assert settings_index(5.6, settings) == 0
    assert settings_index(8, settings) == 1
    assert settings_index(11, settings) == 2


def test_settings_index_less_than(settings):
    """Test closest aperture is above value."""
    assert settings_index(0, settings) == 0
    assert settings_index(7, settings) == 1
    assert settings_index(10, settings) == 2


def test_settings_index_greater_than(settings):
    """Test closest aperture is below value."""
    assert settings_index(6, settings) == 0
    assert settings_index(8.5, settings) == 1
    assert settings_index(12, settings) == 2
