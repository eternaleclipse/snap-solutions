#!/usr/bin/env python3

import re
import sys
from typing import Tuple
import json
import pokecalc

WELCOME_MESSAGE = '''Pokemon damage multiplier calculator by {}!
Enter your query in the form of:
move_name -> pokemon_name

Example:
fire punch -> bulbasaur'''


def parse_user_query(line: str) -> Tuple[str]:
    '''Parse user query into move name and pokemon name.'''

    line = re.sub(r'\s+', ' ', line).strip() # Remove extra whitespace
    line_parts = line.split(' -> ')

    try:
        attack_name, pokemon_name = line_parts[0], line_parts[1]
    except IndexError:
        raise ValueError('Invalid input format')
    
    if not attack_name or not pokemon_name:
        raise ValueError('Invalid input format')

    attack_name = attack_name.replace(' ', '-')
    pokemon_name = pokemon_name.replace(' ', '-')

    return (attack_name, pokemon_name)


def main():
    '''
    Parse move and pokemon names from user, retrieve and print
    the attack multiplier.
    '''

    calculator = pokecalc.DamageCalculator()
    print(WELCOME_MESSAGE)

    try:
        attack_name, pokemon_name = parse_user_query(input())
        attack_type = pokecalc.get_attack_type(attack_name)
        defense_types = pokecalc.get_pokemon_types(pokemon_name)
        multiplier = calculator.get_damage_multiplier(attack_type, defense_types)
    except (IndexError, json.JSONDecodeError):
        print('Error: Could not parse response, probably wrong pokemon / move name')
    except ValueError as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)

    print('x{:g}'.format(multiplier))


if __name__ == '__main__':
    main()
