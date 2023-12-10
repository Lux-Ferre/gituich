from dataclasses import dataclass, field


@dataclass
class Entity:
    display: str = ""
    description: str = ""
    max_quantity: float = float('inf')
    weight: int = 0
    value: int = 0
    cost: list = field(default_factory=list)
    is_obtainable: bool = False
    is_alive: bool = False
    is_craftable: bool = False
    is_tool: bool = False


entity_data = {
    "stick": Entity(value=1, weight=3, is_obtainable=True),
    "vine": Entity(value=4, weight=1, is_obtainable=True),
    "stone": Entity(value=2, weight=5, is_obtainable=True),
    "rope": Entity(value=15,weight=3, is_obtainable=True, is_craftable=True, cost=[("vine", 3)], description="A simple rope made from braided vines."),
    "basket": Entity(is_obtainable=True, is_craftable=True, cost=[("vine", 1), ("stick", 10)], description="Allows you to carry more items when foraging.",max_quantity=1),
}
