"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import io
import json
import logging
import os
import shlex
import subprocess
import time
import typing
import yaml


_logger = logging.getLogger(__name__)


class SecondShooter:
    def __init__(
        self,
        camera: typing.Union[str, None] = None,
        port: typing.Union[str, None] = None
    ):
        if (camera and not port) or (not camera and port):
            raise ValueError(
                'Camera and port must both be specified when overriding '
                'auto-detection.'
            )

        self._camera = camera
        self._port = port
        self._camera_settings = load_camera_settings(camera)
        self._command = {
            'aperture': self.aperture,
            'capture': self.capture,
            'iso': self.iso,
            'shutter': self.shutter,
            'wait': self.wait
        }

    def run(self, script: typing.Union[io.TextIOBase, str]):
        for step in yaml.load_all(script):
            if step:
                self._command.get(step.get('cmd'), self.default)(**step)

    def aperture(self, value, **_):
        _logger.info('Setting aperture to %s.', value)

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config {entry}={value}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['aperture'],
                value=value
            )
            if self._camera else
            'gphoto2 --set-config {entry}={value}'.format(
                entry=self._camera_settings['aperture'],
                value=value
            )
        )
        execute(cmd)

    def capture(self, **_):
        _logger.info('Capturing image.')

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--capture-image'.format(
                camera=self._camera,
                port=self._port
            )
            if self._camera else
            'gphoto2 --capture-image'
        )
        execute(cmd)

    def iso(self, value, **_):
        _logger.info('Setting ISO to %s.', value)

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config {entry}={value}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['iso'],
                value=value
            )
            if self._camera else
            'gphoto2 --set-config {entry}={value}'.format(
                entry=self._camera_settings['iso'],
                value=value
            )
        )
        execute(cmd)

    def shutter(self, value, **_):
        _logger.info('Setting shutter speed to %s.', value)

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config {entry}={value}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['shutter'],
                value=value
            )
            if self._camera else
            'gphoto2 --set-config {entry}={value}'.format(
                entry=self._camera_settings['shutter'],
                value=value
            )
        )
        execute(cmd)

    def wait(self, value: float, **_):
        _logger.info('Waiting %s seconds.', value)

        time.sleep(float(value))

    def default(self, cmd: str, **kwargs):
        _logger.error('Unknown command, %s', cmd)
        _logger.debug('%s', kwargs)


def autodetect_camera() -> str:
    """Auto-detect camera using gphoto2.

    Returns:
        string returned from gphoto2.
    """
    _logger.debug('Auto detecting camera.')

    result = execute('gphoto2 --auto-detect')

    if result.returncode:
        raise ValueError(result.stderr)

    return result.stdout.decode()


def load_camera_settings(camera: typing.Union[str, None]) -> dict:
    """Load camera settings for camera.

    Args:
        camera: camera make, or None for auto-detect.

    Returns:
        camera settings.
    """
    _logger.debug('Loading camera settings.')
    if camera is None:
        camera = autodetect_camera()

    for model in ('Canon', 'Nikon'):
        if model in camera:
            break
    else:
        raise ValueError('Unknown camera "{}"'.format(camera))

    _logger.info('Camera model: %s.', model)

    with open(
        os.path.join(
            os.path.dirname(__file__),
            'cameras',
            '{}.json'.format(model.lower())
        )
    ) as f:
        config = json.load(f)

    return config


def execute(cmd: str) -> subprocess.CompletedProcess:
    """Execute command.

    Args:
        cmd: shell command to execute.

    Returns:
        CompletedProcess.
    """
    _logger.debug('Executing cmd: %s', cmd)

    result = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode:
        _logger.error(
            '{cmd} exited with value {value}'.format(
                cmd=cmd,
                value=result.returncode
            )
        )

    return result
