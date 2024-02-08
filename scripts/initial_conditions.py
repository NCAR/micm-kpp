"""
Copyright (C) 2023, 2024
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0
(Software Package Data Exchange)

File:
    initial_conditions.py

Usage:
    python initial_conditions.py
    python initial_conditions.py --help

Description:

"""

import os
import sys
import argparse
import logging
import json

if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--micm_dir', type=str,
        # default=os.path.join('..', 'configs', 'micm'),
        default=os.path.join('..', 'racm_esrl_vcp', 'micm'),
        help='MICM output species config file')
    parser.add_argument('--mechanism', type=str,
        # default='test',
        default='RACM_SOA_VBS',
        help='mechanism name')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    species_file = os.path.join(args.micm_dir, args.mechanism, 'species.json')
    logging.info(species_file)

    reactions_file = os.path.join(args.micm_dir, args.mechanism, 'reactions.json')
    logging.info(reactions_file)
