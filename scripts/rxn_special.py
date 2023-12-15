"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    rxn_special.py
"""

import logging

from parse_kpp_utils import parse_coeffs

def parse_kpp_k45(kpp_str):
    """
    Parse KPP RACM k45 reaction

    Parameters
        (str) kpp_str: k45 reaction string

    Returns
        (tuple of dict): MICM Arrhenius and Troe reaction coefficients


    k45 formula from WRF-KPP
    ------------------------
    k45(T, [M])
    k0 = 2.4e-14 * exp(460 / T)
    k2 = 2.7e-17 * exp(2199 / T)
    k3 = 6.5e-34 * exp(1335 / T) * [M]
    k45 = k0 + k3 / (1 + k3 / k2)
    """

    coeffs = parse_coeffs(kpp_str)

    arrhenius_dict = dict()
    arrhenius_dict['type'] = 'ARRHENIUS'

    troe_dict = dict()
    troe_dict['type'] = 'TROE'

    if ('k45' in kpp_str):
        arrhenius_dict['A'] = 2.4e-14
        arrhenius_dict['B'] = 0.0
        arrhenius_dict['C'] = 460.0
        troe_dict['k0_A']   = 6.5e-34
        troe_dict['k0_B']   = 0.0
        troe_dict['k0_C']   = 1335.0
        troe_dict['kinf_A'] = 2.7e-17
        troe_dict['kinf_B'] = 0.0
        troe_dict['kinf_C'] = 2199.0
        troe_dict['Fc']     = 1.0
        troe_dict['N']      = 0.0
    else:
        logging.error('unrecognized KPP k45 syntax')

    logging.debug(arrhenius_dict)
    logging.debug(troe_dict)

    return arrhenius_dict, troe_dict


def parse_kpp_k57(kpp_str):
    """
    Parse KPP RACM k57 reaction

    Parameters
        (str) kpp_str: k57 reaction string

    Returns
        (tuple of dict): MICM Troe and Ternary reaction coefficients


    k57 formula from WRF-KPP
    ------------------------
    k57(T, [M])
    sum of Troe and Ternary reactions
    """
    coeffs = parse_coeffs(kpp_str)

    troe_dict = dict()
    troe_dict['type'] = 'TROE'

    ternary_dict = dict()
    ternary_dict['type'] = 'TERNARY_CHEMICAL_ACTIVATION'

    if ('k57' in kpp_str):
        troe_dict['k0_A']      = 5.9e-33
        troe_dict['k0_B']      = - 1.4
        troe_dict['k0_C']      = 0.0
        troe_dict['kinf_A']    = 1.1e-12
        troe_dict['kinf_B']    = 1.3
        troe_dict['kinf_C']    = 0.0
        troe_dict['Fc']        = 0.6
        troe_dict['N']         = 1.0
        ternary_dict['k0_A']   = 1.5e-13
        ternary_dict['k0_B']   = 0.6
        ternary_dict['k0_C']   = 0.0
        ternary_dict['kinf_A'] = 2.9e9
        ternary_dict['kinf_B'] = 6.1
        ternary_dict['kinf_C'] = 0.0
        ternary_dict['Fc']     = 0.6
        ternary_dict['N']      = 1.0
    else:
        logging.error('unrecognized KPP k57 syntax')

    logging.debug(troe_dict)
    logging.debug(ternary_dict)

    return troe_dict, ternary_dict

