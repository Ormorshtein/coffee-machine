from typing import Set

from coffee_machine.data_types.costumer import Costumer
from coffee_machine.data_types.drink import Drink
from coffee_machine.data_types.inventorymanager import CoinInventoryManager, ResourceInventoryManager


class Machine:

    def __init__(self, resources_inventory: ResourceInventoryManager, coins_inventory: CoinInventoryManager, drinks: Set[Drink]):
        self.resources_inventory = resources_inventory
        self.coins_inventory = coins_inventory
        self.drinks = drinks

    def _has_sufficient_resources(self, costumer: Costumer) -> bool:
        costumer_resources: ResourceInventoryManager = costumer.drink.resources
        for resource in costumer_resources.products():
            if self.resources_inventory.amount_of(resource) < costumer_resources.amount_of(resource):
                # print(f'Sorry, there is not enough {resource.name}.')
                return False
        return True

    def _has_sufficient_change(self, costumer: Costumer) -> bool:
        return self.coins_inventory.total_amount >= costumer.coins.total_amount - costumer.drink.cost

    def _validate_reservation(self, costumer: Costumer) -> bool:
        return self._has_sufficient_resources(costumer) and \
               costumer.has_sufficient_money() and \
               self._has_sufficient_change(costumer)

    # TODO: think of a way of changing it
    def _make_order(self, costumer) -> None:
        self.resources_inventory -= costumer.drink.resources
        self.coins_inventory -= costumer.coins
        self.coins_inventory.return_change(costumer.coins.total_amount - costumer.drink.cost)

    def get_drink_by_name(self, drink_name: str) -> Drink:
        for drink in self.drinks:
            if drink.name == drink_name:
                return drink

    def print_report(self) -> None:
        print(self.resources_inventory)
        print(self.coins_inventory)

    # TODO: rename & separate ui and logic
    def validate_make_order(self, costumer: Costumer) -> None:
        if self._validate_reservation(costumer):
            self._make_order(costumer)
            print(f'Here is your {costumer.drink.name}. Enjoy!')