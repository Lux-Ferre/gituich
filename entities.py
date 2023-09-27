from dataclasses import dataclass, field


@dataclass
class Entity:
    display: str = ""
    description: str = ""
    max_quantity: float = float('inf')


@dataclass
class NonLiving(Entity):
    weight: int = 0


@dataclass
class Obtainable(NonLiving):
    value: int = 0


@dataclass
class Craftable(Obtainable):
    cost: list[tuple[Obtainable, int]] = field(default_factory=list)


@dataclass
class Tool:
    pass


@dataclass
class Stick(Obtainable):
    display = "Stick"
    value = 1
    weight = 3


@dataclass
class Vine(Obtainable):
    display = "Vine"
    value = 4
    weight = 1


@dataclass
class Stone(Obtainable):
    display = "Stone"
    value = 2
    weight = 5


@dataclass
class Rope(Craftable):
    display = "Rope"
    cost = [
        (Vine, 3),
    ]
    value = 15
    weight = 3
    description = "A simple rope made from braided vines."


@dataclass
class Basket(Craftable, Tool):
    display = "Basket"
    cost = [
        (Vine, 1),
        (Stick, 10),
    ]
    description = "Allows you to carry more items when foraging."
    max_quantity = 1
