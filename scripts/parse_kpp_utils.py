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

    coeff_strs = kpp_str.split('(')[1].split(')')[0].split(',')

    coeffs = list()

    for coeff_str in coeff_strs:
        coeffs.append(
            float(coeff_str.replace(' ', '').replace('_dp', '').replace('D', 'E')))

    logging.debug(coeffs)

    return coeffs

