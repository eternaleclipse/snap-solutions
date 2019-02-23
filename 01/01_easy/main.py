#!/usr/bin/env python3

import re
import sys
from typing import Tuple
import pokecalc

WELCOME_MESSAGE = '''Pokemon damage multiplier calculator!
Enter your query in the form of:
attack_type -> defense_type [, defense_type, ..]

Example:
fire -> water ice grass'''

def parse_user_query(line: str) -> Tuple[str, Tuple[str]]:
    '''Parse user query into attack type and defense types.'''

    line = re.sub(r'\s+', ' ', line).strip() # Remove extra whitespace
    line_parts = line.split(' ')

    try:
        (attack_type, arrow), defense_types = line_parts[:2], line_parts[2:]
    except ValueError:
        raise ValueError('Invalid input format')
    
    if (not attack_type) or (arrow != '->') or (not defense_types):
        raise ValueError('Invalid input format')

    defense_types = tuple(set(defense_types)) # Remove duplicates
    return (attack_type, defense_types)


def main():
    '''
    Parse attack and defense types from user, retrieve and print
    the attack multiplier.
    '''

    calculator = pokecalc.DamageCalculator('data.csv')
    print(WELCOME_MESSAGE)

    try:
        attack_type, defense_types = parse_user_query(input())
        multiplier = calculator.get_damage_multiplier(attack_type, defense_types)
    except ValueError as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)

    print('x{:g}'.format(multiplier))


if __name__ == '__main__':
    main()
