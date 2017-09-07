"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_get_aperture_settings(shooter):
    mock_result = mock.Mock(
        returncode=0,
        stdout=mock.Mock(
            decode=mock.Mock(return_value='Choice: 0 f/5.6\nChoice: 1 f/8\nChoice: 2 f/11')
        )
    )
    gold_apertures = [5.6, 8.0, 11.0]

    # Shooter camera is specified in the tests.
    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock_result
    ) as mock_execute:
        apertures = shooter.get_aperture_settings()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--get-config /main/capturesettings/f-number'
    )
    assert apertures == gold_apertures

    # Force it to default.
    shooter._camera = None
    shooter._port = None

    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock_result
    ) as mock_execute:
        shooter.get_aperture_settings()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--get-config /main/capturesettings/f-number'
    )
    assert apertures == gold_apertures
