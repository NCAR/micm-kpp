"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    test_kpp_to_micm.py

Usage:
    pytest test_kpp_to_micm.py --log-cli-level=DEBUG
"""

from rxn_arrhenius import parse_kpp_arrhenius
from rxn_troe import parse_kpp_troe
from rxn_special import parse_kpp_k45

def test_parse_kpp_arrhenius():
    """
    ARR_ab(A, B)
    ARR2(A, B)
    ARR_ac(A, C)
    ARR_abc(A, B, C)
    ARR(A, B, C)
    """

    kpp_A, kpp_B, kpp_C = 1.0e-12, 2000.0, -3.0

    arr_dict = parse_kpp_arrhenius(
        'ARR_ab(%.2e, %.2f)' % (kpp_A, kpp_B))
    assert arr_dict['A'] == kpp_A
    assert arr_dict['C'] == - kpp_B

    arr_dict = parse_kpp_arrhenius(
        'ARR2(%.2e, %.2f)' % (kpp_A, kpp_B))
    assert arr_dict['A'] == kpp_A
    assert arr_dict['C'] == - kpp_B

    arr_dict = parse_kpp_arrhenius(
        'ARR_ac(%.2e, %.2f)' % (kpp_A, kpp_C))
    assert arr_dict['A'] == kpp_A
    assert arr_dict['B'] == kpp_C

    arr_dict = parse_kpp_arrhenius(
        'ARR_abc(%.2e, %.2f, %.2f)' % (kpp_A, kpp_B, kpp_C))
    assert arr_dict['A'] == kpp_A
    assert arr_dict['C'] == - kpp_B
    assert arr_dict['B'] == kpp_C

    arr_dict = parse_kpp_arrhenius(
        'ARR(%.2e, %.2f, %.2f)' % (kpp_A, kpp_B, kpp_C))
    assert arr_dict['A'] == kpp_A
    assert arr_dict['C'] == - kpp_B
    assert arr_dict['B'] == kpp_C


def test_parse_kpp_troe():
    """
    TROEE(A, B, k0, n0, kinf, ninf, T, [M])
    TROE(k0, n0, kinf, ninf, T, [M])
    """
    kpp_A, kpp_B, kpp_k0, kpp_n0, kpp_kinf, kpp_ninf \
        = 1.0, 2000.0, 3.0e-11, 4, 5.0e-12, 6
    kpp_T, kpp_n_M = 300.0, 2.0e19

    troe_dict = parse_kpp_troe(
        'TROEE(%.2f, %.2f, %.2e, %.2f, %.2e, %.2f, %.2f, %.2e)'
        % (kpp_A, kpp_B, kpp_k0, kpp_n0, kpp_kinf, kpp_ninf,
           kpp_T, kpp_n_M))

    assert troe_dict['k0_A']   == kpp_A * kpp_k0
    assert troe_dict['k0_B']   == - kpp_n0
    assert troe_dict['k0_C']   == - kpp_B
    assert troe_dict['kinf_A'] == kpp_kinf
    assert troe_dict['kinf_B'] == - kpp_ninf
    assert troe_dict['kinf_C'] == 0.0
    assert troe_dict['Fc']     == 0.6
    assert troe_dict['N']      == 1.0

    troe_dict = parse_kpp_troe(
        'TROE(%.2e, %.2f, %.2e, %.2f, %.2f, %.2e)'
        % (kpp_k0, kpp_n0, kpp_kinf, kpp_ninf,
           kpp_T, kpp_n_M))

    assert troe_dict['k0_A']   == kpp_k0
    assert troe_dict['k0_B']   == - kpp_n0
    assert troe_dict['k0_C']   == 0.0
    assert troe_dict['kinf_A'] == kpp_kinf
    assert troe_dict['kinf_B'] == - kpp_ninf
    assert troe_dict['kinf_C'] == 0.0
    assert troe_dict['Fc']     == 0.6
    assert troe_dict['N']      == 1.0


def test_parse_kpp_45():

    kpp_T, kpp_n_M = 300.0, 2.0e19

    arr_dict, troe_dict = parse_kpp_k45(
        'k45(%.2f, %.2e)' % (kpp_T, kpp_n_M))

    assert arr_dict['A']       == 2.4e-14
    assert arr_dict['B']       == 0.0
    assert arr_dict['C']       == 460.0
    assert troe_dict['k0_A']   == 6.5e-34
    assert troe_dict['k0_B']   == 0.0
    assert troe_dict['k0_C']   == 1335.0
    assert troe_dict['kinf_A'] == 2.7e-17
    assert troe_dict['kinf_B'] == 0.0
    assert troe_dict['kinf_C'] == 2199.0
    assert troe_dict['Fc']     == 1.0
    assert troe_dict['N']      == 0.0

