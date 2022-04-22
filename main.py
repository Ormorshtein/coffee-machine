from typing import Dict, Set

from coin import Coin
from costumer import Costumer
from drink import Drink
from machine import Machine, NoSuchDrinkError
from resource import Resource

STARTING_COIN = 10

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def parse_resources(resources_str: Dict[str, int]) -> Dict[Resource, int]:
    drink_resources: Dict[Resource, int] = {}
    for resource, amount in resources_str.items():
        drink_resources[Resource(resource)] = amount
    return drink_resources


def parse_menu() -> Set[Drink]:
    drinks: Set[Drink] = set()
    for drink_name, drink_data in MENU.items():
        drink_resources: Dict[Resource, int] = parse_resources(drink_data['ingredients'])
        drink_cost = drink_data['cost']
        drinks.add(Drink(name=drink_name, resources=drink_resources, cost=drink_cost))
    return drinks


def setup() -> Machine:
    machine_resources: Dict[Resource, int] = parse_resources(resources)
    machine_coins: Dict[Coin, int] = {coin: STARTING_COIN for coin in Coin}
    machine_drinks: Set[Drink] = parse_menu()
    return Machine(machine_resources, machine_coins, machine_drinks)


def ask_for_coins() -> Dict[Coin, int]:
    print('Please enter coins.')
    costumer_coins: Dict[Coin, int] = {}
    for coin in Coin:
        amount: int = int(input(f'How many {coin.name}? '))
        costumer_coins[coin] = amount
    return costumer_coins


def interactive_machine() -> None:
    machine: Machine = setup()
    while True:
        costumer_choice: str = input('What would you like? (espresso/latte/cappuccino):')
        if costumer_choice == 'report':
            machine.print_report()
        elif costumer_choice == 'off':
            print('Goodbye.')
            machine.turn_off()
        else:
            try:
                costumer_drink: Drink = machine.get_drink_by_name(costumer_choice)
                print(f'The price is ${costumer_drink.cost}.')
                costumer_coins: Dict[Coin, int] = ask_for_coins()
                costumer: Costumer = Costumer(costumer_drink, costumer_coins)
                machine.validate_make_order(costumer)
            except NoSuchDrinkError as e:
                print(e.msg)


interactive_machine()
