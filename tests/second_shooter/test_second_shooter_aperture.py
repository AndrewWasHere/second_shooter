"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from second_shooter.second_shooter import SecondShooter


def test_aperture(shooter):
    gold_apertures = [5.6, 8.0, 11.0]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_aperture_settings',
        return_value=gold_apertures
    ):
        shooter.aperture('f/11')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config-index /main/capturesettings/f-number=2'
    )

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute'
    ) as mock_execute, mock.patch.object(
        SecondShooter,
        'get_aperture_settings',
        return_value=gold_apertures
    ):
        shooter.aperture('f/11')

    mock_execute.assert_called_with(
        'gphoto2 '
        '--set-config-index /main/capturesettings/f-number=2'
    )
