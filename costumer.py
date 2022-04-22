from typing import Dict

from coin import Coin
from drink import Drink


class Costumer:
    def __init__(self, drink: Drink, coins: Dict[Coin, int]):
        self.drink = drink
        self.coins = coins

    def get_total_money(self) -> float:
        total: float = 0
        for coin in self.coins.keys():
            total += coin.value * self.coins[coin]
        return total

    def is_money_sufficient_for_drink(self) -> bool:
        if not self.drink.cost <= self.get_total_money():
            print('Sorry, not enough money.')
            return False
        return True
