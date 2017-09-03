"""
Copyright 2017, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import argparse
import logging

import os

from second_shooter.second_shooter import SecondShooter


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument(
        '-r', '--repeat-forever',
        action='store_true',
        help='Repeat script forever.'
    )
    parser.add_argument(
        '-c', '--run-count',
        type=int,
        default=1,
        help='Run script this many times.'
    )
    parser.add_argument(
        '-C', '--camera',
        default=None,
        help='Camera identifier. Do not specify for auto-detect.'
    )
    parser.add_argument(
        '-p', '--port',
        default=None,
        help='Camera port. Do not specify for auto-detect.'
    )
    parser.add_argument(
        '-l', '--log-file',
        default=None,
        help='Path to log file.'
    )
    parser.add_argument(
        '-L', '--log-level',
        default=logging.INFO,
        help='Minimum log level.'
    )
    args = parser.parse_args()

    args.file = os.path.abspath(os.path.expanduser(args.file))
    if args.log_file:
        args.log_file = os.path.abspath(os.path.expanduser(args.log_file))

    return args


def configure_logging(path: str, level: int):
    logging.basicConfig(
        filename=path,
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    args = parse_command_line()
    configure_logging(args.log_file, args.log_level)
    shooter = SecondShooter(camera=args.camera, port=args.port)
    run_count = -1 if args.repeat_forever else args.run_count

    while run_count != 0:
        with open(args.file, 'r') as script:
            shooter.run(script)
        run_count -= 1

if __name__ == '__main__':
    main()
