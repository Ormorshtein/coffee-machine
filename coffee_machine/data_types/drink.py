from dataclasses import dataclass
from coffee_machine.data_types.inventorymanager import ResourceInventoryManager


# TODO: understand whether i should add an implementation of hash\eq etc...
@dataclass(unsafe_hash=True)
class Drink:
    name: str
    resources: ResourceInventoryManager
    cost: int
