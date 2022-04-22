from enum import Enum


class Resource(Enum):
    MILK = 'milk'
    WATER = 'water'
    COFFEE = 'coffee'

    def get_unit(self) -> str:
        return 'g' if self.COFFEE else 'ml'
