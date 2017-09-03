"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import pytest

from second_shooter.second_shooter import load_camera_settings


def test_load_camera_settings_nikon():
    """Test loading camera settings for a known model."""
    config = load_camera_settings('Nikon')

    assert isinstance(config, dict)
    assert config.get('aperture') == '/main/capturesettings/f-number'
    assert config.get('iso') == '/main/imgsettings/iso'
    assert config.get('shutter') == '/main/capturesettings/shutterspeed2'


def test_load_camera_settings_unknown_model():
    """Test loading camera settings for an unknown model."""
    with pytest.raises(ValueError):
        load_camera_settings('Unknown')


def test_load_camera_settings_autodetect():
    """Test loading camera settings with auto-detection."""
    with mock.patch(
        'second_shooter.second_shooter.autodetect_camera',
        return_value='Nikon'
    ) as mock_autodetect:
        config = load_camera_settings(None)

    assert isinstance(config, dict)
    assert mock_autodetect.called
