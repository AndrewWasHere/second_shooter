"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_wait(shooter):
    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.time.sleep'
    ) as mock_wait:
        shooter.wait(1.25)

    mock_wait.assert_called_with(1.25)

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.time.sleep'
    ) as mock_wait:
        shooter.wait(0)

    mock_wait.assert_called_with(0)
