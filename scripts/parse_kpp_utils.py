"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    parse_kpp_utils.py
"""

import logging


def is_float(string):
    """
    Test if a string can be converted to a float

    Parameters
        (str) string: test string

    Returns
        (bool): True if convertible float, False otherwise
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def parse_coeffs(kpp_str):
    """
    Parse coefficients from a KPP string

    Parameters
        (str) kpp_str: f(x, y, z, ...)

    Returns
        (list of float): [float(x), float(y), float(z), ...]
    """

    logging.debug(kpp_str)

    coeff_strs = kpp_str.split('(')[1].split(')')[0].split(',')

    coeffs = list()

    for coeff_str in coeff_strs:
        coeff_str_reform \
            = coeff_str.replace(' ', '').replace('_dp', '').replace('D', 'E')
        if (is_float(coeff_str_reform)):
            coeffs.append(float(coeff_str_reform))

    logging.debug(coeffs)

    return coeffs

