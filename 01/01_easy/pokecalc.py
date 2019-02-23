import csv
import functools
import operator
from typing import Iterable, Union
import pandas


class DamageCalculator():
    def __init__(self, data_file: str):
        # Read CSV table, replace rows and cols for readability and turn it
        # into a dict of dicts (data[attack_type][defense_type] = multiplier)
        self.multiplier_data = pandas.read_csv(data_file, ',',
                        index_col='attack_type').transpose().to_dict()


    def get_single_type_damage_multiplier(self,
                                       attack_type: str,
                                       defense_type: str) -> Union[float, int]:
        '''
        Returns damage multiplier for the specified attack and defense types.
        '''

        try:
            return self.multiplier_data[attack_type][defense_type]
        except KeyError as e:
            raise ValueError('Invalid pokemon type {}'.format(e.args[0]))
        

    def get_damage_multiplier(self,
                            attack_type: str,
                            defense_types: Iterable[str]) -> Union[float, int]:
        '''
        Calculate damage multiplier for specified attack and defense types.
        Supports multiple defense types.
        '''
        
        multipliers = [
            self.get_single_type_damage_multiplier(attack_type, defense_type)
                for defense_type in defense_types]

        return functools.reduce(operator.mul, multipliers)
