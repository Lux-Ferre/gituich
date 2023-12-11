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


def generate_entities():
    entity_data = {
        "stick": {"display": "Stick",
                  "value": 1,
                  "weight": 3,
                  "is_obtainable": True,
                  },
        "vine": {"display": "Vine",
                 "value": 4,
                 "weight": 1,
                 "is_obtainable": True
                 },
        "stone": {"display": "Stone",
                  "value": 2,
                  "weight": 5,
                  "is_obtainable": True
                  },
        "rope": {"display": "Rope",
                 "value": 15,
                 "weight": 3,
                 "is_obtainable": True,
                 "is_craftable": True,
                 "cost": [
                     ("vine", 3),
                 ],
                 "description": "A simple rope made from braided vines."
                 },
        "basket": {"display": "Basket",
                   "is_obtainable": True,
                   "is_craftable": True,
                   "is_tool": True,
                   "cost": [
                       ("vine", 1),
                       ("stick", 10),
                   ],
                   "description": "Allows you to carry more items when foraging.",
                   "max_quantity": 1
                   },
    }

    entities = {}

    for entity, raw_data in entity_data.items():
        data = Entity()
        for key, value in raw_data.items():
            setattr(data, key, value)
        entities[entity] = data

    return entities
