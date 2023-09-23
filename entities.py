from dataclasses import dataclass


@dataclass
class Entity:
    pass


@dataclass
class NonLiving(Entity):
    weight: int = 0


@dataclass
class Obtainable:
    value: int = 0


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
