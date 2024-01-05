"""
Copyright (C) 2023
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0

File:
    test_parse_kpp_utils.py

Usage:
    pytest test_parse_kpp_utils.py --log-cli-level=DEBUG
"""

from parse_kpp_utils import is_float, parse_coeffs, parse_term


def test_is_float():
    assert is_float('a') == False
    assert is_float('1a') == False
    assert is_float(1) == True
    assert is_float(1.0) == True
    assert is_float(- 1.0) == True
