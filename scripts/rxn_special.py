"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    rxn_troe.py
"""

import logging

from parse_kpp_utils import parse_coeffs

def parse_kpp_special(kpp_str, N_reactants=2):
    """
    Parse KPP specially defined reaction

    Parameters
        (str) kpp_str: Troe reaction string
        (int) N_reactants: number of reactants

    Returns
        (dict): MICM Troe reaction coefficients


    k45 formula from WRF-KPP
    ---------------------
    k45(T, [M])
    k0 = 2.4E-14 * exp(460 / T)
    k2 = 2.7E-17 * exp(2199 / T)
    k3 = 6.5E-34 * exp(1335 / T) * [M]
    k45 = k0 + k3 / (1 + k3 / k2)

    Troe formula from MICM
    ----------------------
    double k0 = parameters_.k0_A_ * std::exp(parameters_.k0_C_ / temperature)
      * std::pow(temperature / 300.0, parameters_.k0_B_);

    double kinf = parameters_.kinf_A_ * std::exp(parameters_.kinf_C_ / temperature)
      * std::pow(temperature / 300.0, parameters_.kinf_B_);

    return k0 * air_number_density / (1.0 + k0 * air_number_density / kinf)
      * std::pow(parameters_.Fc_, parameters_.N_
      / (parameters_.N_ + std::pow(std::log10(k0 * air_number_density / kinf), 2)));
    """

    coeffs = parse_coeffs(kpp_str)

    troe_dict = dict()
    troe_dict['type'] = 'TROE'

    if ('k45' in kpp_str):
        troe_dict['k0_A']   =
        troe_dict['k0_B']   =
        troe_dict['k0_C']   =
        troe_dict['kinf_A'] =
        troe_dict['kinf_B'] =
        troe_dict['kinf_C'] = 0.0
        troe_dict['Fc']     = 0.6
        troe_dict['N']      = 1.0
    else:
        logging.error('unrecognized KPP Troe syntax')

    logging.debug(troe_dict)
    return troe_dict

