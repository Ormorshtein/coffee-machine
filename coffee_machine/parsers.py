from typing import Dict, Set

from coffee_machine.data_types.drink import Drink
from coffee_machine.data_types.inventorymanager import ResourceInventoryManager

from coffee_machine.enums.resources import Resource


def parse_resources(resources_str: Dict[str, int]) -> Dict[Resource, int]:
    drink_resources: Dict[Resource, int] = {}
    for resource, amount in resources_str.items():
        drink_resources[Resource(resource)] = amount
    return drink_resources


def parse_menu(menu) -> Set[Drink]:
    drinks: Set[Drink] = set()
    for drink_name, drink_data in menu.items():
        drink_resources: ResourceInventoryManager = ResourceInventoryManager(parse_resources(drink_data['ingredients']))
        drink_cost = drink_data['cost']
        drinks.add(Drink(name=drink_name, resources=drink_resources, cost=drink_cost))

    return drinks
