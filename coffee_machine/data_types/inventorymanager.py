from collections import Counter
from typing import List, Dict

from coffee_machine.enums.coin import Coin, NotEnoughMoneyError


class InventoryManager:
    def __init__(self, inventory_dict):
        self._inventory_dict = inventory_dict

    @property
    def inventory(self):
        return self._inventory_dict

    def items(self):
        return self._inventory_dict.items()

    def products(self):
        return self._inventory_dict.keys()

    def __add__(self, other):
        self._inventory_dict = dict(Counter(self._inventory_dict) + Counter(other.inventory))
        return self

    def __sub__(self, other):
        self._inventory_dict = dict(Counter(self._inventory_dict) - Counter(other.inventory))
        return self

    def __str__(self):
        product_str_list: List[str] = []
        for product, amount in self.inventory.items():
            product_str_list.append(f'{product.name}: {amount}')
        return str(product_str_list)

    def amount_of(self, product):
        return self.inventory[product]


class CoinInventoryManager(InventoryManager):

    def __init__(self, inventory_dict):
        super().__init__(inventory_dict)
        self._total_amount = 0

    @property
    def total_amount(self) -> float:
        total: float = 0
        for coin, amount in self.inventory.items():
            total += coin.value * amount
        return total

    def _validate_change_exists(self, change: float, change_in_coins: Dict[Coin, int],
                                visited_change: Dict[float, bool]) -> bool:
        if change == 0:
            return True
        if change < 0:
            return False

        if change in visited_change:
            return visited_change[change]
        for coin, amount in self.inventory.items():
            if amount >= 1:
                amount -= 1
                change_in_coins[coin] += 1
                if not self._validate_change_exists(change - coin.value, change_in_coins, visited_change):
                    amount += 1
                    change_in_coins[coin] -= 1
                else:
                    return True
        return False

    def return_change(self, change: int) -> Dict[Coin, int]:
        change_in_coins: Dict[Coin, int] = {coin: 0 for coin in Coin}
        visited_change: Dict[float, bool] = {}
        if self._validate_change_exists(change, change_in_coins, visited_change):
            return change_in_coins
        raise NotEnoughMoneyError


class ResourceInventoryManager(InventoryManager):

    def __str__(self):
        str_resources_list: List[str] = []
        for resource, amount in self.inventory.items():
            str_resources_list.append(f'{resource.name} {amount}{resource.measurement_unit.value}')
        return str(str_resources_list)
