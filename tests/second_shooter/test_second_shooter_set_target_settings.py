"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock


def test_set_target_settings_no_config(shooter):
    """Test no target config on camera."""
    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock.Mock(
            returncode=1
        )
    ) as mock_execute:
        shooter.set_target_settings()

    mock_execute.assert_called_once_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--get-config /main/settings/capturetarget'
    )

    shooter._camera = None

    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock.Mock(
            returncode=1
        )
    ) as mock_execute:
        shooter.set_target_settings()

    mock_execute.assert_called_once_with(
        'gphoto2 --get-config /main/settings/capturetarget'
    )


def test_set_target_settings_config(shooter):
    """Test target config on camera."""
    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock.Mock(
            returncode=0,
            stdout=mock.Mock(decode=mock.Mock(return_value=None))
        )
    ) as mock_execute, mock.patch(
        'second_shooter.second_shooter.parse_settings',
        return_value=iter(['Internal RAM', 'Memory card'])
    ):
        shooter.set_target_settings()

    mock_execute.assert_called_with(
        'gphoto2 '
        '--camera "Nikon" '
        '--port "port" '
        '--set-config-index /main/settings/capturetarget=1'
    )
    assert mock_execute.call_count == 2

    shooter._camera = None

    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=mock.Mock(
            returncode=0
        )
    ) as mock_execute, mock.patch(
        'second_shooter.second_shooter.parse_settings',
        return_value=iter(['Internal RAM', 'Somewhere else'])
    ):
        shooter.set_target_settings()

    assert mock_execute.call_count == 1
