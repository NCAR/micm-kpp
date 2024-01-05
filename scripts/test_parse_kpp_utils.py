"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    test_parse_kpp_utils.py

Usage:
    pytest test_parse_kpp_utils.py --log-cli-level=DEBUG
"""

def test_is_float():
    from parse_kpp_utils import is_float
    assert is_float('a') == False
    assert is_float('1a') == False
    assert is_float(1) == True
    assert is_float(1.0) == True
    assert is_float(- 1.0) == True


def test_parse_coeffs():
    from parse_kpp_utils import parse_coeffs
    coeffs = parse_coeffs('f(0.0, 1.0, 2.0, 3.0)')
    assert coeffs[0] == 0.0
    assert coeffs[1] == 1.0
    assert coeffs[2] == 2.0
    assert coeffs[3] == 3.0
    coeffs = parse_coeffs(' ( f(0.0, 1.0, 2.0, 3.0) )')
    assert coeffs[0] == 0.0
    assert coeffs[1] == 1.0
    assert coeffs[2] == 2.0
    assert coeffs[3] == 3.0


def test_parse_term():
    from parse_kpp_utils import parse_term
    x, M = parse_term('3H2O')
    assert x == 3
    assert M == 'H2O'
    x, M = parse_term('3 H2O')
    assert x == 3
    assert M == 'H2O'
    x, M = parse_term(' 3 H2O')
    assert x == 3
    assert M == 'H2O'
    x, M = parse_term('1.23H2O')
    assert x == 1.23
    assert M == 'H2O'
    x, M = parse_term('1.23 H2O')
    assert x == 1.23
    assert M == 'H2O'
    x, M = parse_term('.12H2O')
    assert x == 0.12
    assert M == 'H2O'
    x, M = parse_term('.12 H2O')
    assert x == 0.12
    assert M == 'H2O'

