"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    rxn_arrhenius.py
"""

import logging

from parse_kpp_utils import parse_coeffs

def parse_kpp_arrhenius(kpp_str, N_reactants=2):
    """
    Parse KPP Arrhenius reaction

    Parameters
        (str) kpp_str: Arrhenius reaction string
        (int) N_reactants: number of reactants

    Returns
        (dict): MICM Arrhenius reaction coefficients

    Arrhenius formula from KPP
    --------------------------
    ARR_abc = A * exp(- B / T) * (T / 300)^C

    Arrhenius formula from MICM
    ---------------------------
    return parameters_.A_ * std::exp(parameters_.C_ / temperature)
      * pow(temperature / parameters_.D_, parameters_.B_) *
      (1.0 + parameters_.E_ * pressure);
    """

    coeffs = parse_coeffs(kpp_str)
    logging.debug('coeffs:' + str(coeffs))

    arrhenius_dict = dict()
    arrhenius_dict['type'] = 'ARRHENIUS'
    # note the interchange of B and C, and change of sign
    # in the KPP and MICM conventions
    if ('ARR(' in kpp_str or '_abc(' in kpp_str):
        arrhenius_dict['A'] = coeffs[0]
        arrhenius_dict['B'] = coeffs[2]
        arrhenius_dict['C'] = - coeffs[1]
        arrhenius_dict['D'] = 300.0
    elif ('ARR2(' in kpp_str or '_ab(' in kpp_str):
        arrhenius_dict['A'] = coeffs[0]
        arrhenius_dict['C'] = - coeffs[1]
        arrhenius_dict['D'] = 300.0
    elif ('_ac(' in kpp_str):
        arrhenius_dict['A'] = coeffs[0]
        arrhenius_dict['B'] = coeffs[1]
        arrhenius_dict['D'] = 300.0
    else:
        logging.error('unrecognized KPP Arrhenius syntax')
    logging.debug(arrhenius_dict)
    return arrhenius_dict

