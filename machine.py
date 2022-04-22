from typing import Dict, Set

from coin import Coin
from costumer import Costumer
from drink import Drink
from resource import Resource


def print_coins(coins: Dict[Coin, int]):
    for coin in coins.keys():
        print(f'{coin.name}: {coins[coin]}')


class NoSuchDrinkError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Machine:

    def __init__(self, resources: Dict[Resource, int], coins: Dict[Coin, int], drinks: Set[Drink]):
        self.resources = resources
        self.coins = coins
        self.drinks = drinks

    # private methods

    def _increase_money(self, new_coins: Dict[Coin, int]) -> None:
        for coin in new_coins.keys():
            self.coins[coin] += new_coins[coin]

    def _decrease_money(self, coins_to_decrease: Dict[Coin, int]) -> None:
        for coin in coins_to_decrease.keys():
            self.coins[coin] -= coins_to_decrease[coin]

    def _increase_resources(self, new_resources: Dict[Resource, int]) -> None:
        for resource in new_resources.keys():
            self.resources[resource] -= new_resources[resource]

    def _decrease_resources(self, resources_to_decrease: Dict[Resource, int]) -> None:
        for resource in resources_to_decrease.keys():
            self.resources[resource] -= resources_to_decrease[resource]

    def _print_resources_inventory(self) -> None:
        for resource in self.resources.keys():
            print(f'{resource.name}: {self.resources[resource]}{resource.get_unit()}')

    def _get_total_money(self) -> float:
        total: float = 0
        for coin in self.coins.keys():
            total += coin.value * self.coins[coin]
        return total

    def _print_money_inventory(self) -> None:
        print(f'Money: ${self._get_total_money()}')

    def _validate_sufficient_resources(self, costumer: Costumer) -> bool:
        costumer_resources: Dict[Resource, int] = costumer.drink.resources
        for resource in costumer_resources.keys():
            if self.resources[resource] < costumer_resources[resource]:
                print(f'Sorry, there is not enough {resource.name}.')
                return False
        return True

    def _validate_sufficient_change(self, costumer: Costumer) -> bool:
        if not self._get_total_money() >= costumer.get_total_money() - costumer.drink.cost:
            print('Sorry, there is not enough money for change.')
            return False
        return True

    def _validate_reservation(self, costumer: Costumer) -> bool:
        return self._validate_sufficient_resources(costumer) and \
               costumer.is_money_sufficient_for_drink() and \
               self._validate_sufficient_change(costumer)

    def _return_change_rec(self, change: float, coins_to_return: Dict[Coin, int]) -> bool:
        if change == 0:
            return True
        if change < 0:
            return False
        for coin in self.coins.keys():
            if self.coins[coin] - 1 >= 0:
                self.coins[coin] -= 1
                coins_to_return[coin] += 1
                if not self._return_change_rec(change - coin.value, coins_to_return):
                    self.coins[coin] += 1
                    coins_to_return[coin] -= 1
                else:
                    return True
        return False

    def _return_change(self, change: int) -> None:
        coins_to_return: Dict[Coin, int] = {coin: 0 for coin in Coin}
        if self._return_change_rec(change, coins_to_return):
            print('Here is your change: ')
            print_coins(coins_to_return)

    def _make_order(self, costumer) -> None:
        self._decrease_resources(costumer.drink.resources)
        self._increase_money(costumer.coins)
        self._return_change(costumer.get_total_money() - costumer.drink.cost)

    # public methods
    def get_drink_by_name(self, drink_name: str) -> Drink:
        for drink in self.drinks:
            if drink.name == drink_name:
                return drink
        raise NoSuchDrinkError(f'No Such drink {drink_name}.')

    def print_report(self) -> None:
        self._print_resources_inventory()
        self._print_money_inventory()

    def validate_make_order(self, costumer: Costumer) -> None:
        if self._validate_reservation(costumer):
            self._make_order(costumer)
            print(f'Here is your {costumer.drink.name}. Enjoy!')

    @staticmethod
    def turn_off() -> None:
        exit(0)
