"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_capture(shooter):
    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute:
        shooter.capture()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--capture-image'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute:
        shooter.capture()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--capture-image'
    )
