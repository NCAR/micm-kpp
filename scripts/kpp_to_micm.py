"""
Copyright (C) 2023, 2024
National Center for Atmospheric Research,
SPDX-License-Identifier: Apache-2.0
(Software Package Data Exchange)

File:
    kpp_to_micm.py

Usage:
    python kpp_to_micm.py
    python kpp_to_micm.py --help

Description:
    kpp_to_micm.py translates KPP config files to MICM JSON config files
    (desginated by the suffixes .kpp, .spc, .eqn, .def)
    from a single directory specified by the
    --kpp_dir and --kpp_name arguments.

    In the initial implementation,
    the KPP sections #ATOMS (not yet used), #DEFFIX,
    #DEFVAR, and #EQUATIONS are read and parsed.
    Equations with the hv reactant are MICM PHOTOLYSIS reactions,
    equations with a single coefficient are assumed to be ARRHENIUS reactions.

TODO:
    (1) Add pytest unit test for method micm_equation_json.
    (2+) Add support for several other reaction types ...
"""

import os
import sys
import argparse
import logging
import json
from glob import glob

from parse_kpp_utils import is_float, parse_term
from rxn_arrhenius import parse_kpp_arrhenius
from rxn_troe import parse_kpp_troe
from rxn_special import parse_kpp_k45, parse_kpp_k57

__version__ = 'v1.05'


def read_kpp_config(kpp_dir, kpp_name):
    """
    Read all KPP config files in a directory

    Parameters
        (str) kpp_dir: KPP directory

    Returns
        (list of str): all lines from all config files
    """

    suffixes = ['.kpp', '.spc', '.eqn', '.def']

    lines = list()

    for suffix in suffixes:
        files = glob(os.path.join(kpp_dir, kpp_name + '*' + suffix))
        logging.debug(files)
        for filename in files:
            with open(filename, 'r') as f:
                lines.extend(f.readlines())

    # remove empty lines and tabs
    lines = [line.replace('\t', '') for line in lines if line.strip()] 

    for line in lines:
        logging.debug(line.strip())

    return lines


def split_by_section(lines):
    """
    Split KPP config lines by section

    Parameters
        (list of str) lines: all lines config files

    Returns
        (dict of list of str): lines in each section
    """

    sections = {'#ATOMS': [],
                '#DEFVAR': [],
                '#DEFFIX': [],
                '#EQUATIONS': []}

    joined_lines = ''.join(lines)
    section_blocks = joined_lines.split('#')

    for section in sections:
        for section_block in section_blocks:
            if section.replace('#', '') in section_block:
                sections[section].extend(section_block.split('\n')[1:-1])

    return sections


def micm_species_json(lines, fixed=False, tolerance=1.0e-12):
    """
    Generate MICM species JSON

    Parameters
        (list of str) lines: lines of species section
        (bool) fixed: set constant tracer
        (float) tolerance: absolute tolerance

    Returns
        (list of dict): list of MICM species entries
    """

    species_json = list() # list of dict

    for line in lines:
        lhs, rhs = tuple(line.split('='))
        logging.debug((lhs, rhs))
        species_dict = {'name': lhs.replace('{', '').replace('}', '').strip().lstrip(),
            'type': 'CHEM_SPEC'}
        if fixed:
            species_dict['tracer type'] = 'CONSTANT'
        else:
            species_dict['absolute tolerance'] = tolerance
        species_json.append(species_dict)

    return species_json


def micm_equation_json(lines):
    """
    Generate MICM equation JSON

    Parameters
        (list of str) lines: lines of equation section

    Returns
        (list of dict): list of MICM equation entries
    """

    equations = list() # list of dict

    for line in lines:
        logging.debug(line)

        # split on equal sign into left hand and right hand sides 
        lhs, rhs = tuple(line.split('='))

        # extract reaction coefficients
        rhs, coeffs = tuple(rhs.split(':'))
        coeffs = coeffs.replace(';', '')

        # get reactants and products
        reactants = lhs.split('+')
        products = rhs.split('+')

        # extract equation label delimited by < > or { }
        if '>' in reactants[0]:
            label, reactants[0] = tuple(reactants[0].split('>'))
            label = label.lstrip('<')
        else:
            label, reactants[0] = tuple(reactants[0].split('}'))
            label = label.replace('{', '').lstrip()
        logging.info('label:' + label)

        # remove trailing and leading whitespace
        reactants = [reactant.strip().lstrip().replace('{', '').replace('}', '') for reactant in reactants]
        products = [product.strip().lstrip().replace('{', '').replace('}', '') for product in products]

        N_reactants = len(reactants)

        equation_dict = dict()
        equation_second_dict = None

        if ('SUN' in coeffs) or ('Pj_' in coeffs):
            equation_dict['type'] = 'PHOTOLYSIS'
        elif 'ARR' in coeffs:
            equation_dict = parse_kpp_arrhenius(coeffs,
                N_reactants=N_reactants)
        elif 'TROE' in coeffs:
            equation_dict = parse_kpp_troe(coeffs,
                N_reactants=N_reactants)
        elif 'k45' in coeffs:
            equation_dict, equation_second_dict = parse_kpp_k45(coeffs)
        elif 'k57' in coeffs:
            equation_dict, equation_second_dict = parse_kpp_k57(coeffs)
        else:
            # default to Arrhenius with a single coefficient
            coeffs = coeffs.replace('(', '').replace(')', '').replace(
                'D', 'E').replace('_dp', '')
            equation_dict['type'] = 'ARRHENIUS'
            if is_float(coeffs):
                equation_dict['A'] = float(coeffs)
            else:
                equation_dict['A'] = 0.0

        equation_dict['reactants'] = dict()
        equation_dict['products'] = dict()

        if equation_second_dict is not None:
            equation_second_dict['reactants'] = dict()
            equation_second_dict['products'] = dict()

        for reactant in reactants:
            if 'hv' in reactant:
                pass
            else:
                x, M = parse_term(reactant)
                equation_dict['reactants'][M] = {'qty': x}
                if equation_second_dict is not None:
                    equation_second_dict['reactants'][M] = {'qty': x}

        for product in products:
            x, M = parse_term(product)
            equation_dict['products'][M] = {'yield': x}
            if equation_second_dict is not None:
                equation_second_dict['products'][M] = {'yield': x}

        if equation_second_dict is not None:
            equation_dict['MUSICA name'] = label + '_first_term'
            equation_second_dict['MUSICA name'] = label + '_second_term'
        else:
            equation_dict['MUSICA name'] = label

        equations.append(equation_dict)

        if equation_second_dict is not None:
            equations.append(equation_second_dict)

    return equations


if __name__ == '__main__':

    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str,
        default=sys.stdout,
        help='log file (default stdout)')
    parser.add_argument('--kpp_dir', type=str,
        # default=os.path.join('..', 'configs', 'kpp'),
        default=os.path.join('..', 'racm_esrl_vcp', 'kpp'),
        help='KPP input config directory')
    parser.add_argument('--kpp_name', type=str,
        # default='test',
        default='racm_soa_vbs',
        help='KPP config name')
    parser.add_argument('--micm_dir', type=str,
        # default=os.path.join('..', 'configs', 'micm'),
        default=os.path.join('..', 'racm_esrl_vcp', 'micm'),
        help='MICM output species config file')
    parser.add_argument('--mechanism', type=str,
        # default='test',
        default='RACM_SOA_VBS',
        help='mechanism name')
    parser.add_argument('--debug', action='store_true',
        help='set logging level to debug')
    args = parser.parse_args()

    """
    Setup logging
    """
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(stream=args.logfile, level=logging_level)

    """
    Read KPP config files
    """
    lines = read_kpp_config(args.kpp_dir, args.kpp_name)

    """
    Split KPP config by section
    """
    sections = split_by_section(lines)
    for section in sections:
        logging.info('____ KPP section %s ____' % section)
        for line in sections[section]:
            logging.info(line)
        print('\n')

    """
    Generate MICM species JSON from KPP #DEFFIX section
    """
    deffix_json = micm_species_json(sections['#DEFFIX'], fixed=True)

    """
    Generate MICM species JSON from KPP #DEFVAR section
    """
    defvar_json = micm_species_json(sections['#DEFVAR'])

    """
    Generate MICM equations JSON from KPP #EQUATIONS section
    """
    equations_json = micm_equation_json(sections['#EQUATIONS'])

    """
    Assemble MICM species JSON
    """
    micm_species_json = {'camp-data': deffix_json + defvar_json}
    micm_species_json_str = json.dumps(micm_species_json, indent=4)
    logging.info('____ MICM species ____')
    logging.info(micm_species_json_str)
    print('\n')

    """
    Assemble MICM reactions JSON
    """
    micm_reactions_json = {'camp-data':
        [{'name': args.mechanism, 'type': 'MECHANISM', 'reactions': equations_json}]}
    micm_reactions_json_str = json.dumps(micm_reactions_json, indent=4)
    logging.info('____ MICM reactions ____')
    logging.info(micm_reactions_json_str)
    print('\n')

    """
    Write MICM JSON
    """
    micm_mechanism_dir = os.path.join(args.micm_dir, args.mechanism)
    if not os.path.exists(args.micm_dir):
        os.mkdir(args.micm_dir)
    if not os.path.exists(micm_mechanism_dir):
        os.mkdir(micm_mechanism_dir)
    with open(os.path.join(micm_mechanism_dir, 'species.json'), 'w') as f:
        json.dump(micm_species_json, f, indent=4)
    with open(os.path.join(micm_mechanism_dir, 'reactions.json'), 'w') as f:
        json.dump(micm_reactions_json, f, indent=4)

