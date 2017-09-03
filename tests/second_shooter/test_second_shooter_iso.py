"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_iso(shooter):
    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute:
        shooter.iso(1600)

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config /main/imgsettings/iso=1600'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute:
        shooter.iso(100)

    mock_execute.assert_called_with(
        'gphoto2 '
        '--set-config /main/imgsettings/iso=100'
    )
