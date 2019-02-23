import csv
import functools
import operator
from typing import Tuple, Union
import requests

TYPE_API_URL = 'https://pokeapi.co/api/v2/type/{}'
ATTACK_API_URL = 'https://pokeapi.co/api/v2/move/{}'
POKEMON_API_URL = 'https://pokeapi.co/api/v2/pokemon/{}'


class DamageCalculator():
    @functools.lru_cache(maxsize=128)
    def get_single_type_damage_multiplier(self,
                                          attack_type: str,
                                          defense_type: str) -> Union[int, float]:
        '''
        Returns damage multiplier for the specified attack and defense types.
        '''

        url = TYPE_API_URL.format(attack_type)
        damage_data = requests.get(url).json()['damage_relations']

        relations_multipliers = (
            ('no_damage_to', 0),
            ('half_damage_to', 0.5),
            ('double_damage_to', 2))

        for relation, multiplier in relations_multipliers:
            # Get list of types associated with that relation
            types = [_type['name'] for _type in damage_data[relation]]
            if defense_type in types:
                return multiplier

        return 1


    @functools.lru_cache(maxsize=128)
    def get_damage_multiplier(self,
                              attack_type: str,
                              defense_types: Tuple[str]) -> float:
        '''
        Calculate damage multiplier for specified attack and defense types.
        Supports multiple defense types.
        '''
        
        multipliers = []

        for defense_type in defense_types:
            multipliers.append(
                self.get_single_type_damage_multiplier(attack_type, defense_type))

        return functools.reduce(operator.mul, multipliers)

@functools.lru_cache(maxsize=128)
def get_attack_type(name: str) -> str:
    '''Returns type for the specified attack.'''
    url = ATTACK_API_URL.format(name)
    return requests.get(url).json()['type']['name']

@functools.lru_cache(maxsize=128)
def get_pokemon_types(name: str) -> Tuple[str]:
    '''Returns type for the specified Pokemon.'''
    url = POKEMON_API_URL.format(name)
    types = tuple([slot['type']['name'] for slot in
                    requests.get(url).json()['types']])

    return types