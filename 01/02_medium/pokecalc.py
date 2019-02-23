import csv
import functools
import operator
from typing import Iterable, Union
import requests

TYPE_API_URL = 'https://pokeapi.co/api/v2/type/{}'


class DamageCalculator():
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

        try:
            for relation, multiplier in relations_multipliers:
                # Get list of types associated with that relation
                types = [_type['name'] for _type in damage_data[relation]]
                if defense_type in types:
                    return multiplier
        except KeyError:
            raise ValueError('Invalid JSON API response format')

        return 1


    def get_damage_multiplier(self,
                              attack_type: str,
                              defense_types: Iterable[str]) -> float:
        '''
        Calculate damage multiplier for specified attack and defense types.
        Supports multiple defense types.
        '''
        
        multipliers = []

        for defense_type in defense_types:
            multipliers.append(
                self.get_single_type_damage_multiplier(attack_type, defense_type))

        return functools.reduce(operator.mul, multipliers)
