"""
Copyright (C) 2024
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0
(Software Package Data Exchange)

File:
    mozart_to_micm.py

Usage:
    python mozart_to_micm.py
    python mozart_to_micm.py --help
"""

import os
import sys
import argparse
import logging
import json
from glob import glob

__version__ = 'v1.00'


def read_mozart_config(config_dir, config_name):
    """
    Read all Mozart config files in a directory

    Parameters
        (str) mozart_dir: Mozart directory

    Returns
        (list of str): all lines from all config files
    """

    suffixes = ['.spc', '.eqn', '.def']

    lines = list()

    for suffix in suffixes:
        files = glob(os.path.join(config_dir, config_name + '*' + suffix))
        logging.debug(files)
        for filename in files:
            with open(filename, 'r') as f:
                lines.extend(f.readlines())

    # remove empty lines and tabs
    lines = [line.replace('\t', '') for line in lines if line.strip()] 

    for line in lines:
        logging.debug(line.strip())

    return lines


def split_by_section(lines):
    """
    Split config lines by section

    Parameters
        (list of str) lines: all lines config files

    Returns
        (dict of list of str): lines in each section
    """

    sections = {'#Variable': [],
                '#Fixed': [],
                '#Equations': []}

    joined_lines = ''.join(lines)
    section_blocks = joined_lines.split('#')

    for section in sections:
        for section_block in section_blocks:
            if section.replace('#', '') in section_block:
                sections[section].extend(section_block.split('\n')[1:-1])

    return sections


if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--input_dir', type=str,
        default=os.path.join('..', 'am4', 'mozart'),
        help='input config directory')
    parser.add_argument('--input_name', type=str,
        default='am4',
        help='config name')
    parser.add_argument('--micm_dir', type=str,
        default=os.path.join('..', 'am4', 'micm'),
        help='MICM output species config file')
    parser.add_argument('--mechanism', type=str,
        default='AM4',
        help='mechanism name')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    """
    Read Mozart config files
    """
    lines = read_mozart_config(args.input_dir, args.input_name)

    """
    Split configs by section
    """
    sections = split_by_section(lines)
    for section in sections:
        logging.info('____ section %s ____' % section)
        for line in sections[section]:
            logging.info(line)
        print('\n')

