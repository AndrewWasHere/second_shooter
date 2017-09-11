"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import pytest

from second_shooter.second_shooter import SecondShooter


@pytest.fixture
def shooter():
    """SecondShooter instantiated without a camera to talk to."""
    with mock.patch.object(
        SecondShooter,
        'set_target_settings'
    ):
        s = SecondShooter('Nikon', 'port')

    return s
