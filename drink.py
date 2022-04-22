from typing import Dict

from resource import Resource


class Drink:

    def __init__(self, name: str, resources: Dict[Resource, int], cost: float):
        self.name = name
        self.resources = resources
        self.cost = cost


