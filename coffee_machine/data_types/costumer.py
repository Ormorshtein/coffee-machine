from dataclasses import dataclass
from coffee_machine.data_types.inventorymanager import CoinInventoryManager
from coffee_machine.data_types.drink import Drink


@dataclass
class Costumer:
    drink: Drink
    coins: CoinInventoryManager

    def has_sufficient_money(self) -> bool:
        return self.coins.total_amount >= self.drink.cost
