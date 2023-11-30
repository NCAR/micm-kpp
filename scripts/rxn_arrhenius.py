"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    rxn_arrhenius.py
"""

import logging

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

    KPP_REAL ARR_abc( float A0, float B0, float C0 )
    {
      double ARR_RES;

      ARR_RES = (double)A0
        * exp( -(double)B0/TEMP )
        * pow( (TEMP/300.0), (double)C0 );

    return (KPP_REAL)ARR_RES;
    }

    Arrhenius formula from MICM
    ---------------------------

    inline double ArrheniusRateConstant::calculate(
      const double& temperature, const double& pressure) const
    {
    return parameters_.A_ * std::exp(parameters_.C_ / temperature)
      * pow(temperature / parameters_.D_, parameters_.B_) *
      (1.0 + parameters_.E_ * pressure);
    }
    """
    logging.debug(kpp_str)
    coeffs = [float(coeff.replace(' ', '')) for coeff in
        kpp_str.split('(')[1].split(')')[0].split(',')]
    logging.debug(coeffs)
    arr_dict = dict()
    arr_dict['type'] = 'ARRHENIUS' 
    # note the interchange of B and C, and change of sign
    # in the KPP and MICM conventions
    if ('_abc(' in kpp_str):
        arr_dict['A'] = coeffs[0]
        arr_dict['B'] = coeffs[2]
        arr_dict['C'] = - coeffs[1]
        arr_dict['D'] = 300.0
    elif ('_ab(' in kpp_str):
        arr_dict['A'] = coeffs[0]
        arr_dict['C'] = - coeffs[1]
        arr_dict['D'] = 300.0
    elif ('_ac(' in kpp_str):
        arr_dict['A'] = coeffs[0]
        arr_dict['B'] = coeffs[1]
        arr_dict['D'] = 300.0
    else:
        logging.error('unrecognized KPP Arrhenius syntax')
    logging.debug(arr_dict)
    return arr_dict
