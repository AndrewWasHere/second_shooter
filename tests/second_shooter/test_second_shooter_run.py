"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from second_shooter.second_shooter import SecondShooter


def test_run_empty():
    """Test run with no commands."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('')

    assert not mock_aperture.called
    assert not mock_capture.called
    assert not mock_iso.called
    assert not mock_shutter.called
    assert not mock_wait.called
    assert not mock_default.called


def test_run_empty():
    """Test run with no commands."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('---')

    assert not mock_aperture.called
    assert not mock_capture.called
    assert not mock_iso.called
    assert not mock_shutter.called
    assert not mock_wait.called
    assert not mock_default.called

def test_run_aperture():
    """Test run calls aperture."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: aperture\nvalue: 8')

    mock_aperture.assert_called_with(cmd='aperture', value=8)
    assert not mock_capture.called
    assert not mock_iso.called
    assert not mock_shutter.called
    assert not mock_wait.called
    assert not mock_default.called


def test_run_capture():
    """Test run calls capture."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: capture')

    assert not mock_aperture.called
    mock_capture.assert_called_with(cmd='capture')
    assert not mock_iso.called
    assert not mock_shutter.called
    assert not mock_wait.called
    assert not mock_default.called


def test_run_iso():
    """Test run calls iso."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: iso\nvalue: 100')

    assert not mock_aperture.called
    assert not mock_capture.called
    mock_iso.assert_called_with(cmd='iso', value=100)
    assert not mock_shutter.called
    assert not mock_wait.called
    assert not mock_default.called


def test_run_shutter():
    """Test run calls shutter."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: shutter\nvalue: 1/250')

    assert not mock_aperture.called
    assert not mock_capture.called
    assert not mock_iso.called
    mock_shutter.assert_called_with(cmd='shutter', value='1/250')
    assert not mock_wait.called
    assert not mock_default.called


def test_run_wait():
    """Test run calls wait."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: wait')

    assert not mock_aperture.called
    assert not mock_capture.called
    assert not mock_iso.called
    assert not mock_shutter.called
    mock_wait.assert_called_with(cmd='wait')
    assert not mock_default.called


def test_run_default():
    """Test run calls default when it gets an unkown command."""
    with mock.patch.object(
        SecondShooter,
        'aperture'
    ) as mock_aperture, mock.patch.object(
        SecondShooter,
        'capture'
    ) as mock_capture, mock.patch.object(
        SecondShooter,
        'iso'
    ) as mock_iso, mock.patch.object(
        SecondShooter,
        'shutter'
    ) as mock_shutter, mock.patch.object(
        SecondShooter,
        'wait'
    ) as mock_wait, mock.patch.object(
        SecondShooter,
        'default'
    ) as mock_default:
        shooter = SecondShooter('Nikon', 'port')
        shooter.run('cmd: not a command')

    assert not mock_aperture.called
    assert not mock_capture.called
    assert not mock_iso.called
    assert not mock_shutter.called
    assert not mock_wait.called
    mock_default.assert_called_with(cmd='not a command')


def test_run_multiple_steps():
    """Test run parses multiple commands."""
    def aperture_side_effect(**_):
        call_order.append('aperture')

    def capture_side_effect(**_):
        call_order.append('capture')

    def iso_side_effect(**_):
        call_order.append('iso')

    def shutter_side_effect(**_):
        call_order.append('shutter')

    def wait_side_effect(**_):
        call_order.append('wait')

    def default_side_effect(**_):
        call_order.append('default')

    call_order = []

    with mock.patch.object(
        SecondShooter,
        'aperture',
        side_effect=aperture_side_effect
    ), mock.patch.object(
        SecondShooter,
        'capture',
        side_effect=capture_side_effect
    ), mock.patch.object(
        SecondShooter,
        'iso',
        side_effect=iso_side_effect
    ), mock.patch.object(
        SecondShooter,
        'shutter',
        side_effect=shutter_side_effect
    ), mock.patch.object(
        SecondShooter,
        'wait',
        side_effect=wait_side_effect
    ), mock.patch.object(
        SecondShooter,
        'default',
        side_effect=default_side_effect
    ):
        shooter = SecondShooter('Nikon', 'port')
        shooter.run("""\
---
cmd: iso
value: 100
---
cmd: shutter
value: 1/125
---
cmd: aperture
value: 8
---
cmd: capture
---
cmd: wait
value: 2
---
cmd: capture
---
cmd: shutter
value: 1/250
---
cmd: capture
            """)

    assert call_order == [
        'iso',
        'shutter',
        'aperture',
        'capture',
        'wait',
        'capture',
        'shutter',
        'capture'
    ]
