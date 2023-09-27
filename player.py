from dataclasses import dataclass, field
from typing import Type

import regions
import entities


@dataclass
class Player:
    display: str = "Player"
    location: regions.Region = regions.PlayerHouse
    inventory: dict = field(default_factory=dict)
    tools: dict = field(default_factory=dict)
    money: int = 0

    def has_tool(self, tool: Type[entities.Tool], num: int):
        if tool in self.tools:
            if self.tools[tool] >= num:
                return True

    def add_tool(self, tool: Type[entities.Tool], num: int):
        if tool in self.tools:
            self.tools[tool] += num
        else:
            self.tools[tool] = num

    def has_item(self, item: entities.Obtainable | Type[entities.Obtainable], num: int):
        if item in self.inventory:
            if self.inventory[item] >= num:
                return True

        return False

    def add_item(self, item: entities.Obtainable, num: int):
        if item in self.inventory:
            self.inventory[item] += num
        else:
            self.inventory[item] = num
