from dataclasses import dataclass, field


@dataclass
class Entity:
    description: str = ""
    max_quantity: float = float('inf')


@dataclass
class NonLiving(Entity):
    weight: int = 0


@dataclass
class Obtainable():
    value: int = 0


@dataclass
class Craftable(Obtainable):
    cost: list[tuple[Obtainable, int]] = field(default_factory=list)


@dataclass
class Tool:
    pass


@dataclass
class Stick(NonLiving, Obtainable):
    value = 15
    weight = 3


@dataclass
class Vine(NonLiving, Obtainable):
    value = 20
    weight = 1


@dataclass
class Stone(NonLiving, Obtainable):
    value = 5
    weight = 5


@dataclass
class Basket(Craftable, Tool):
    cost = [
        (Vine, 1),
        (Stick, 10),
    ]
    description = "Allows you to carry more items when foraging."
    max_quantity = 1
