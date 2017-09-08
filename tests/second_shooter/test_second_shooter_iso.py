"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from second_shooter.second_shooter import SecondShooter


def test_iso(shooter):
    gold_iso = [100, 200, 340]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_iso_settings',
        return_value=gold_iso
    ):
        shooter.iso(100)

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config-index /main/imgsettings/iso=0'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_iso_settings',
        return_value=gold_iso
    ):
        shooter.iso(340)

    mock_execute.assert_called_with(
        'gphoto2 '
        '--set-config-index /main/imgsettings/iso=2'
    )
