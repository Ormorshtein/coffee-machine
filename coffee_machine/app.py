from typing import Dict, Set

from coffee_machine.parsers import parse_resources, parse_menu
from enums.coin import Coin
from coffee_machine.data_types.costumer import Costumer
from coffee_machine.data_types.drink import Drink
from coffee_machine.data_types.machine import Machine
from coffee_machine.data_types.inventorymanager import ResourceInventoryManager, CoinInventoryManager
from coffee_machine.config import settings, STARTING_COIN


# TODO: separate ui & logic. ie. DO NOT add prints to code except in one module which will represent the program's UI


def setup() -> Machine:
    machine_resources: ResourceInventoryManager = ResourceInventoryManager(parse_resources(settings.resources))
    machine_coins: CoinInventoryManager = CoinInventoryManager({coin: STARTING_COIN for coin in Coin})
    machine_drinks: Set[Drink] = parse_menu(settings.MENU)
    return Machine(machine_resources, machine_coins, machine_drinks)


def ask_for_coins() -> Dict[Coin, int]:
    print('Please enter coins.')
    costumer_coins: Dict[Coin, int] = {}
    for coin in Coin:
        try:
            amount: int = int(input(f'How many {coin.name}? '))
            costumer_coins[coin] = amount
        except ValueError as ve:
            # TODO: figure out a way to iterate over an enum and loop when encountered an error like this
            print('Error!!!! you need to insert an integer.')

    return costumer_coins


# TODO: add options in the ui (to off, report ...)
def interactive_machine() -> None:
    machine: Machine = setup()
    while True:
        costumer_choice: str = input('What would you like? (espresso/latte/cappuccino):')
        if costumer_choice == 'report':
            machine.print_report()
        elif costumer_choice.lower() == 'off':
            print('Goodbye.')
            exit(0)
        else:
            costumer_drink: Drink = machine.get_drink_by_name(costumer_choice)
            print(f'The price is ${costumer_drink.cost}.')
            costumer_coins: CoinInventoryManager = CoinInventoryManager(ask_for_coins())
            costumer: Costumer = Costumer(costumer_drink, costumer_coins)
            machine.validate_make_order(costumer)


if __name__ == '__main__':
    interactive_machine()
