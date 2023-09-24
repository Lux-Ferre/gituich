from dataclasses import dataclass

import entities


@dataclass
class Tool:
    pass


@dataclass
class Craftable(Tool):
    cost: list[tuple[entities.Obtainable, int]]


@dataclass
class Basket(Craftable):
    cost = [
        (entities.Vine, 1),
        (entities.Stick, 10),
    ]