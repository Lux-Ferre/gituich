from dataclasses import dataclass

import entities


@dataclass
class Region:
    available_items: list[tuple[entities.Obtainable, int]]
    display: str = ""


@dataclass
class Forest(Region):
    display = "The Forest"
    available_items = [
        (entities.Stick, 65),
        (entities.Vine, 10),
        (entities.Stone, 25),
    ]


@dataclass
class PlayerHouse(Region):
    display = "Your home."
    available_items = []
