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
        (str) kpp_str: 'f(x, y, z, ...)'

    Returns
        (list of float): [float(x), float(y), float(z), ...]
    """

    logger = logging.getLogger(__name__)
    logger.debug('kpp_str:' + str(kpp_str))

    if (kpp_str.lstrip()[0] == '('):
        coeff_strs = kpp_str.lstrip().rstrip()[1:-1].split('(')[1].split(')')[0].split(',')
    else:
        coeff_strs = kpp_str.split('(')[1].split(')')[0].split(',')

    logger.debug('coeff_strs:' + str(coeff_strs))

    coeffs = list()

    for coeff_str in coeff_strs:
        coeff_str_reform \
            = coeff_str.replace(' ', '').replace('_dp', '').replace('D', 'E')
        if (is_float(coeff_str_reform)):
            coeffs.append(float(coeff_str_reform))

    logger.debug(coeffs)

    return coeffs


def parse_term(kpp_str):
    """
    Parse a reaction term from a KPP string
        with a numerical coefficient x and molecular formula M

    Parameters
        (str) kpp_str: 'x M'

    Returns
        (tuple float, str): float(x), M
    """

    logger = logging.getLogger(__name__)
    logger.debug('kpp_str:' + str(kpp_str))

    n = 0
    while ( not kpp_str[n].isalpha() ):
        n += 1

    return float(kpp_str[0:n]), kpp_str[n:]

