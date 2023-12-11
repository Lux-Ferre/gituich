import random

from tabulate import tabulate
from collections import Counter

from player import Player
import utils
import regions
from entities import generate_entities


class Game:
    def __init__(self):
        self.player = Player("Lux")
        self.regions = regions.generate_regions()
        self.entities = generate_entities()
        self.notification = ""

    def forage(self, quantity: int = 1):
        possible_items = []
        weights = []
        current_region = self.player.location

        if not current_region.available_items:
            self.notification = "No items available here!"
            return

        for item in current_region.available_items:
            possible_items.append(item[0])
            weights.append(item[1])

        found_items = random.choices(population=possible_items, weights=weights, k=quantity)

        notify = f"You found: "

        item_count = Counter(found_items).most_common()

        for item in item_count:
            self.player.add_item(item[0], item[1])
            notify += f"{self.entities[item[0]].display}: {item[1]} |"

        self.notification = notify

    def display_inventory(self):
        titles = ["Item", "Qty", "Value(ea)", "Value(tot)", "Weight(ea)", "Weight(tot)"]
        table = [titles]

        for item_name in self.player.inventory:
            item = self.entities[item_name]

            name = item.display
            qty = self.player.inventory[item_name]
            value = item.value
            weight = item.weight
            total_value = value * qty
            total_weight = weight * qty

            new_row = [name, qty, value, total_value, weight, total_weight]

            table.append(new_row)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def display_tools(self):
        titles = ["Name", "Qty", "Max Qty", "Description"]
        table = [titles]

        for tool_name in self.player.tools:
            tool = self.entities[tool_name]
            name = tool.display
            qty = self.player.tools[tool]
            max_qty = tool.max_quantity
            desc = tool.description

            new_row = [name, qty, max_qty, desc]

            table.append(new_row)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def craft_item(self, item: str):
        item_data = self.entities[item]
        for cost in item_data.cost:
            required_item = cost[0]
            num = cost[1]

            if not self.player.has_item(required_item, num):
                self.notification = f"You did not have enough {item_data.display}"
                return

        for cost in item_data.cost:
            self.player.inventory[cost[0]] -= cost[1]

        if item_data.is_tool:
            self.player.add_tool(item, 1)
        else:
            self.player.add_item(item, 1)

        self.notification = f"{item} successfully crafted"

    def display_regions(self):
        region_list = []
        print("Available regions: ")
        for i, region in enumerate(self.regions):
            region_data = self.regions[region]
            print(f"{i}) {region_data.display}")
            region_list.append(region)

        return region_list

    def display_crafts(self):
        craftables = {
            key: value for key, value in self.entities.items() if value.is_craftable
        }

        craft_list = []

        for i, (name, data) in enumerate(craftables.items()):
            print(f"\t {i+1}) {data.display} - {data.description}")
            craft_list.append(name)

        return craft_list

    def start(self):
        self.player.location = self.regions.get("forest")
        self.forage(20)
        self.player.location = self.regions.get("home")
        active = True

        while active:
            utils.clear()
            print(f"Current location: {game_main.player.location.display}")
            game_main.display_inventory()
            game_main.display_tools()

            print(f"**{self.notification}**")
            self.notification = ""

            print("""Available actions:
            1) Travel
            2) Forage
            3) Craft
            4) Exit
            """)

            action = input("Pick an action: ")

            match action:
                case "1":
                    region_list = self.display_regions()
                    selection = int(input("Where to: "))

                    new_location = region_list[selection]

                    game_main.player.location = self.regions.get(new_location, "home")

                case "2":
                    game_main.forage()
                case "3":
                    craft_list = self.display_crafts()
                    selection = int(input("Select craftable: ")) -1

                    crafted_item = craft_list[selection]

                    game_main.craft_item(crafted_item)

                case "4":
                    active = False
                case _:
                    self.notification = "That is an invalid action."


game_main = Game()
game_main.start()
