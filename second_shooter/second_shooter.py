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
        """Camera Controller.

        Args:
            camera: gphoto2 camera identifier, or None for autodetect.
            port:  gphoto2 port identifier, or None for autodetect.
        """
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
        self._aperture_settings = None
        self._iso_settings = None
        self._shutter_settings = None

    def run(self, script: typing.Union[io.TextIOBase, str]):
        """Run script.

        Args:
            script: YAML script to run.
        """
        for step in yaml.load_all(script):
            if step:
                self._command.get(step.get('cmd'), self.default)(**step)

    def aperture(self, value: str, **_):
        """Set camera aperture.

        Args:
            value: new aperture as f-number.
                e.g f/8
        """
        if self._aperture_settings is None:
            self._aperture_settings = self.get_aperture_settings()

        value = aperture_value(value)
        idx = settings_index(value, self._aperture_settings)

        _logger.info(
            'Setting aperture to %s (requested %s).',
            self._aperture_settings[idx],
            value
        )

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config-index {entry}={index}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['aperture'],
                index=idx
            )
            if self._camera else
            'gphoto2 --set-config-index {entry}={index}'.format(
                entry=self._camera_settings['aperture'],
                index=idx
            )
        )
        execute(cmd)

    def capture(self, **_):
        """Command camera to take picture."""
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

    def iso(self, value: int, **_):
        """Set camera ISO.

        Args:
            value: New ISO value
        """
        if self._iso_settings is None:
            self._iso_settings = self.get_iso_settings()

        idx = settings_index(value, self._iso_settings)

        _logger.info(
            'Setting ISO to %s (requested %s).',
            self._iso_settings[idx],
            value
        )

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config-index {entry}={index}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['iso'],
                index=idx
            )
            if self._camera else
            'gphoto2 --set-config-index {entry}={index}'.format(
                entry=self._camera_settings['iso'],
                index=idx
            )
        )
        execute(cmd)

    def shutter(self, value: str, **_):
        """Set camera shutter speed.

        Args:
            value: shutter speed as decimal value or fraction of a second.
                e.g 1/125 or 2.5.
        """
        if self._shutter_settings is None:
            self._shutter_settings = self.get_shutter_settings()

        value = shutter_value(value)
        idx = settings_index(value, self._shutter_settings)

        _logger.info(
            'Setting shutter speed to %s (requested %s).',
            self._shutter_settings[idx],
            value
        )

        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--set-config-index {entry}={index}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['shutter'],
                index=idx
            )
            if self._camera else
            'gphoto2 --set-config-index {entry}={index}'.format(
                entry=self._camera_settings['shutter'],
                index=idx
            )
        )
        execute(cmd)

    def wait(self, value: float, **_):
        """Pause before next command."""
        _logger.info('Waiting %s seconds.', value)

        time.sleep(float(value))

    def default(self, cmd: str, **kwargs):
        """Unknown commands execute this."""
        _logger.error('Unknown command, %s', cmd)
        _logger.debug('%s', kwargs)

    def get_aperture_settings(self) -> list:
        """Retrieve aperture settings from camera."""
        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--get-config {entry}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['aperture']
            )
            if self._camera else
            'gphoto2 --get-config {entry}'.format(
                entry=self._camera_settings['aperture']
            )
        )
        result = execute(cmd)
        if result.returncode == 0:
            aperture_settings = [
                aperture_value(value)
                for value in parse_settings(result.stdout.decode())
            ]
        else:
            raise ValueError('Unable to get aperture settings from camera.')

        return aperture_settings

    def get_iso_settings(self) -> list:
        """Retrieve iso settings from camera.

        Returns:
            List of ISO values. Indexes correspond to gphoto2 indexes.
        """
        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--get-config {entry}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['iso']
            )
            if self._camera else
            'gphoto2 --get-config {entry}'.format(
                entry=self._camera_settings['iso']
            )
        )
        result = execute(cmd)
        if result.returncode == 0:
            iso_settings = [
                int(value)
                for value in parse_settings(result.stdout.decode())
            ]
        else:
            raise ValueError('Unable to get ISO settings from camera.')

        return iso_settings

    def get_shutter_settings(self):
        """Retrieve shutter settings from camera."""
        cmd = (
            'gphoto2 '
            '--camera "{camera}" '
            '--port "{port}" '
            '--get-config {entry}'.format(
                camera=self._camera,
                port=self._port,
                entry=self._camera_settings['shutter']
            )
            if self._camera else
            'gphoto2 --get-config {entry}'.format(
                entry=self._camera_settings['shutter']
            )
        )
        result = execute(cmd)
        if result.returncode == 0:
            shutter_settings = [
                shutter_value(value)
                for value in parse_settings(result.stdout.decode())
            ]
            while isinstance(shutter_settings[-1], str):
                shutter_settings.pop()
        else:
            raise ValueError('Unable to get shutter settings from camera.')

        return shutter_settings


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


def parse_settings(settings: str):
    """Settings generator from get-config.

    Get-config returns something that looks like this:

        Label: ISO Speed
        Type: RADIO
        Current: 100
        Choice: 0 100
        Choice: 1 125
        Choice: 2 160
        Choice: 3 200
        Choice: 4 250
        Choice: 5 320
        Choice: 6 400
        Choice: 7 500
        Choice: 8 640
        Choice: 9 800
        Choice: 10 1000
        Choice: 11 1250
        Choice: 12 1600
        Choice: 13 2000
        Choice: 14 2500
        Choice: 15 3200
        Choice: 16 4000
        Choice: 17 5000
        Choice: 18 6400
        Choice: 19 8000
        Choice: 20 10000
        Choice: 21 12800
        Choice: 22 25600

    Args:
        settings: Returned string from gphoto2 --get-config <setting>

    Yields:
        value
    """
    for line in settings.split('\n'):
        if line.startswith('Choice'):
            tokens = line.split()
            value = tokens[-1]
            yield value


def aperture_value(val: str) -> float:
    """Convert val to a standard aperture value.

    val format depends on the camera manufacturer.

    Canon: <value>
    Nikon: f/<value>

    Args:
        val: aperture value string.

    Returns:
        aperture f-stop
    """
    try:
        # Canon.
        value = float(val)
    except ValueError:
        # Nikon.
        value = float(val.split('/')[-1])

    return value


def shutter_value(val: str) -> typing.Union[float, str]:
    """Convert val to a standard shutter speed value.

    val format depends on the camera manufacturer.

    YAML: 1/N
    Canon: TBD
    Nikon: <decimal>s e.g. 0.1250s or fraction, or string.

    Args:
        val:

    Returns:
        shutter speed or 'error'
    """
    tokens = val.split('/')
    if len(tokens) < 2:
        # Decimal format.
        try:
            shutter_speed = float(tokens[0].strip('s'))
        except ValueError:
            # Not a number.
            shutter_speed = 'error'

    else:
        # Fractional format.
        shutter_speed = float(tokens[0]) / float(tokens[1])

    return shutter_speed


def settings_index(val: float, settings: list) -> int:
    """Return index into settings that has nearest value to val.

    Args:
        val:
        settings:

    Returns:

    """
    idx = 0
    for idx, setting in enumerate(settings):
        if val <= setting:
            if idx > 0:
                # Not first entry.
                delta_prev = abs(val - settings[idx - 1])
                delta_cur = abs(val - setting)

                if delta_prev < delta_cur:
                    # Value closer to previous entry.
                    idx -= 1

            # Setting found.
            break

    return idx
