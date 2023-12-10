import random

from tabulate import tabulate

from player import Player
import utils
import regions
import entities


class Game:
    def __init__(self):
        self.player = Player("Lux")
        self.regions = regions.generate_regions()

    def forage(self, quantity: int = 1) -> str:
        possible_items = []
        weights = []
        current_region = self.player.location

        if not current_region.available_items:
            return "No items available here!"

        for item in current_region.available_items:
            possible_items.append(item[0])
            weights.append(item[1])

        found_items = random.choices(population=possible_items, weights=weights, k=quantity)

        for item in found_items:
            if item in self.player.inventory:
                self.player.inventory[item] += 1
            else:
                self.player.inventory[item] = 1

        notify = f"You found: {found_items}"

        return notify

    def display_inventory(self):
        titles = ["Item", "Qty", "Value(ea)", "Value(tot)", "Weight(ea)", "Weight(tot)"]
        table = [titles]

        for item in self.player.inventory:
            name = item.__name__
            qty = self.player.inventory[item]
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

        for tool in self.player.tools:
            name = tool.__name__
            qty = self.player.tools[tool]
            max_qty = tool.max_quantity
            desc = tool.description

            new_row = [name, qty, max_qty, desc]

            table.append(new_row)

        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def craft_item(self, item: entities.Craftable) -> str:
        for cost in item.cost:
            if self.player.inventory[cost[0]] < cost[1]:
                return f"You did not have enough {cost[0]}"

        for cost in item.cost:
            self.player.inventory[cost[0]] -= cost[1]

        # noinspection PyTypeChecker
        if issubclass(item, entities.Tool):
            self.player.add_tool(item, 1)
        else:
            self.player.add_item(item, 1)

        return f"{item} successfully crafted"

    def start(self):
        self.player.location = self.regions.get("forest")
        self.forage(20)
        self.player.location = self.regions.get("home")
        active = True
        notification = ""

        while active:
            utils.clear()
            print(f"Current location: {game_main.player.location.display}")
            game_main.display_inventory()
            game_main.display_tools()

            print(f"**{notification}**")
            notification = ""

            print("""Available actions:
            1) Travel
            2) Forage
            3) Craft
            4) Exit
            """)

            action = input("Pick an action: ")

            match action:
                case "1":
                    print(f"Available regions:")
                    print(f"    1) Forest")
                    selection = input("Where to: ")

                    match selection:
                        case "1":
                            new_location = "forest"
                        case _:
                            new_location = None

                    if new_location:
                        game_main.player.location = self.regions.get(new_location, "home")

                case "2":
                    notification = game_main.forage()
                case "3":
                    print(f"Available crafts:")
                    print(f"    1) Basket - {entities.Basket.description}")
                    print(f"    2) Rope - {entities.Rope.description}")
                    selection = input("Select craftable: ")

                    match selection:
                        case "1":
                            new_item = "Basket"
                        case "2":
                            new_item = "Rope"
                        case _:
                            new_item = None

                    if new_item:
                        notification = game_main.craft_item(getattr(entities, new_item))

                case "4":
                    active = False
                case _:
                    notification = "That is an invalid action."


game_main = Game()
game_main.start()
