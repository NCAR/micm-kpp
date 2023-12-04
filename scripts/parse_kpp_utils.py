"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    parse_kpp_utils.py
"""

import logging

def parse_coeffs(kpp_str):

    logging.debug(kpp_str)

    coeffs = [float(coeff.replace(' ', '')) for coeff in
        kpp_str.split('(')[1].split(')')[0].split(',')]

    logging.debug(coeffs)

