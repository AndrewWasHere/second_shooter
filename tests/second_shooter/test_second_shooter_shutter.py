"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from second_shooter.second_shooter import SecondShooter


def test_shutter_short(shooter):
    gold_shutters = [0.1250, 0.5000, 2.000]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_shutter_settings',
        return_value=gold_shutters
    ):
        shooter.shutter('1/60')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config-index /main/capturesettings/shutterspeed=0'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_shutter_settings',
        return_value=gold_shutters
    ):
        shooter.shutter('1/2')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--set-config-index /main/capturesettings/shutterspeed=1'
    )


def test_shutter_decimal(shooter):
    gold_shutters = [0.1250, 0.5000, 2.000]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_shutter_settings',
        return_value=gold_shutters
    ):
        shooter.shutter('2.5')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config-index /main/capturesettings/shutterspeed=2'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_shutter_settings',
        return_value=gold_shutters
    ):
        shooter.shutter('2.5')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--set-config-index /main/capturesettings/shutterspeed=2'
    )
