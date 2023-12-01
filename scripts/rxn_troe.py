"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    rxn_troe.py
"""

import logging

def parse_kpp_troe(kpp_str, N_reactants=2):
    """
    Parse KPP Troe reaction

    Parameters
        (str) kpp_str: Troe reaction string
        (int) N_reactants: number of reactants

    Returns
        (dict): MICM Troe reaction coefficients

    Troe formula from KPP
    ---------------------

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

    logging.debug(kpp_str)

