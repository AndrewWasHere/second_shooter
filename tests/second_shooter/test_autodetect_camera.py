"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import subprocess

from second_shooter.second_shooter import autodetect_camera


def test_autodetect_camera():
    with mock.patch(
        'second_shooter.second_shooter.execute',
        return_value=subprocess.CompletedProcess([], 0, stdout=b'')
    ) as mock_execute:
        autodetect_camera()

    assert mock_execute.called_with('gphoto2 --auto-detect')
