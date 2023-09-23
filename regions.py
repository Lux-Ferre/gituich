from dataclasses import dataclass

import entities


@dataclass
class Region:
    available_items: list[tuple[entities.Obtainable, int]]


@dataclass
class Forest(Region):
    available_items = [
        (entities.Stick, 65),
        (entities.Vine, 10),
        (entities.Stone, 25),
    ]
