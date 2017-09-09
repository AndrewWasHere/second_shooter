"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_get_shutter_settings_(shooter):
    mock_result = mock.Mock(
        returncode=0,
        stdout=mock.Mock(
            decode=mock.Mock(
                return_value='Choice: 0 0.125s\nChoice: 1 0.5000s\nChoice: 2 2.500s\nChoice: 3 Bulb'
            )
        )
    )
    gold_shutters = [0.125, 0.5, 2.5]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock_result
    ) as mock_execute:
        shutters = shooter.get_shutter_settings()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--get-config /main/capturesettings/shutterspeed'
    )
    assert shutters == gold_shutters

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock_result
    ) as mock_execute:
        shutters = shooter.get_shutter_settings()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--get-config /main/capturesettings/shutterspeed'
    )
    assert shutters == gold_shutters
