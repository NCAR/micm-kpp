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


    Troe formulas from WRF-KPP
    ---------------------
    TROE(k0, n0, kinf, ninf, T, [M])
    k0    low pressure limit at 300 K
    n0    low pressure exponent
    kinf  high pressure limit at 300 K
    ninf  high pressure exponent
    T     temperature [K]
    [M]   air concentration [molecules cm-3]

    k0(T) = k0 * (300 / T)^n0
    kinf(T) = kinf * (300 / T)^ninf
    kratio(T) = k0(T) / kinf(T)

    TROE = k0(T) * [M] / (1 + kratio(T))
      * 0.6^(1 / (1 + (log10(kratio))^2))

    TROEE(A, B, k0, n0, kinf, ninf, T, [M])
      = A * exp(- B / T) * TROE(k0, n0, kinf, ninf, T, [M])

    Troe formula from MICM
    ----------------------
    double k0 = parameters_.k0_A_ * std::exp(parameters_.k0_C_ / temperature)
      * std::pow(temperature / 300.0, parameters_.k0_B_);

    double kinf = parameters_.kinf_A_ * std::exp(parameters_.kinf_C_ / temperature)
      * std::pow(temperature / 300.0, parameters_.kinf_B_);

    return k0 * air_number_density / (1.0 + k0 * air_number_density / kinf)
      * std::pow(parameters_.Fc_, parameters_.N_
      / (parameters_.N_ + std::pow(std::log10(k0 * air_number_density / kinf), 2)));

    MICM     KPP
    k0_A   = A * k0
    k0_B   = - n0
    k0_C   = - B
    kinf_A = kinf
    kinf_B = - ninf
    """

    logging.debug(kpp_str)
    coeffs = [float(coeff.replace(' ', '')) for coeff in
        kpp_str.split('(')[1].split(')')[0].split(',')]
    logging.debug(coeffs)
    troe_dict = dict()
    troe_dict['type'] = 'TROE'

    if ('TROEE' in kpp_str):
        # TROEE(A, B, k0, n0, kinf, ninf, T, [M])
        troe_dict['k0_A']   = coeffs[0] * coeffs[2]
        troe_dict['k0_B']   = - coeffs[3]
        troe_dict['k0_C']   = - coeffs[1]
        troe_dict['kinf_A'] = coeffs[4]
        troe_dict['kinf_B'] = - coeffs[5]
        troe_dict['kinf_C'] = 0.0
        troe_dict['Fc']     = 0.6
        troe_dict['N']      = 1.0
    elif ('TROE' in kpp_str):
        # TROE(k0, n0, kinf, ninf, T, [M])
        troe_dict['k0_A']   = coeffs[0]
        troe_dict['k0_B']   = - coeffs[1]
        troe_dict['k0_C']   = 0.0
        troe_dict['kinf_A'] = coeffs[2]
        troe_dict['kinf_B'] = - coeffs[3]
        troe_dict['kinf_C'] = 0.0
        troe_dict['Fc']     = 0.6
        troe_dict['N']      = 1.0
    else:
        logging.error('unrecognized KPP Troe syntax')

    logging.debug(troe_dict)
    return troe_dict

