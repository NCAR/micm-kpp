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
    """
    kpp_A, kpp_B, kpp_k0, kpp_n0, kpp_kinf, kpp_ninf \
        = 1.0, 2000.0, 3.0e-11, 4, 5.0e-12, 6
    kpp_T, kpp_n_M = 300.0, 2.0e19

    arr_dict = parse_kpp_troe(
        'TROEE(%.2f, %.2f, %.2e, %.2f, %.2e, %.2f, %.2f, %.2e)'
        % (kpp_A, kpp_B, kpp_k0, kpp_n0, kpp_kinf, kpp_ninf,
           kpp_T, kpp_n_M))

    assert True

