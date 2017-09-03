"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from second_shooter.second_shooter import SecondShooter


def test_construction_defaults():
    test_settings = {
        'test': 0,
        'settings': 1
    }
    with mock.patch(
        'second_shooter.second_shooter.load_camera_settings',
        return_value=test_settings
    ) as mock_load_camera_settings:
        shooter = SecondShooter()

        assert mock_load_camera_settings.called
        assert shooter._camera is None
        assert shooter._port is None
        assert shooter._camera_settings == test_settings
        assert shooter._command['aperture'] == shooter.aperture
        assert shooter._command['capture'] == shooter.capture
        assert shooter._command['iso'] == shooter.iso
        assert shooter._command['shutter'] == shooter.shutter
        assert shooter._command['wait'] == shooter.wait


def test_construction_arguments():
    test_settings = {
        'test': 2,
        'settings': 3
    }
    with mock.patch(
        'second_shooter.second_shooter.load_camera_settings',
        return_value=test_settings
    ) as mock_load_camera_settings:
        shooter = SecondShooter('camera', 'port')

        assert mock_load_camera_settings.called
        assert shooter._camera == 'camera'
        assert shooter._port == 'port'
        assert shooter._camera_settings == test_settings
        assert shooter._command['aperture'] == shooter.aperture
        assert shooter._command['capture'] == shooter.capture
        assert shooter._command['iso'] == shooter.iso
        assert shooter._command['shutter'] == shooter.shutter
        assert shooter._command['wait'] == shooter.wait
