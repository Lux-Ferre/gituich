import random
import json
import subprocess
import threading
import os
import sys

from tabulate import tabulate
from collections import Counter
from websocket_server import WebsocketServer

from player import Player
import regions
from entities import generate_entities
from player_home import get_default_home


class Game:
    def __init__(self, ws):
        self.ws: WebsocketHandler = ws
        self.client_connected = False
        self.player = Player("Lux")
        self.player_home = get_default_home("clearing")
        self.regions = regions.generate_regions()
        self.entities = generate_entities()
        self.notification = ""
        self.action = None
        self.current_craftables = None

    def dispatch_action(self, response):
        if self.action == "change_region":
            self.change_region(int(response))
            self.action = "main"
        elif self.action == "craft_item":
            selection = int(response) - 1

            crafted_item = self.current_craftables[selection]

            self.craft_item(crafted_item)
            self.action = "main"
            self.display_main_menu()
        elif self.action == "main":
            match response:
                case "1":
                    self.display_regions()
                    self.ws.update_display("Where to: ")
                    self.action = "change_region"
                case "2":
                    game_main.forage()
                    self.display_main_menu()
                case "3":
                    self.display_crafts()
                    self.ws.update_display("Select craftable: ")
                    self.action = "craft_item"

                case "4":
                    self.ws.update_display("", True)
                    self.ws.update_display("Game closed.")
                    self.ws.close()
                case _:
                    self.notification = "That is an invalid action."
                    self.display_main_menu()

    def change_region(self, selection: int):
        new_location = list(self.regions.keys())[selection]

        game_main.player.location = self.regions.get(new_location, self.regions["home"])

        if game_main.player.location == self.regions["home"]:
            self.drop_off_items()

        self.display_main_menu()

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

    def display_inventory(self, inventory_id: str):
        titles = ["Item", "Qty", "Value(ea)", "Value(tot)", "Weight(ea)", "Weight(tot)"]
        table = [titles]

        if inventory_id == "Your home":
            inventory = self.player_home.storage
        else:
            inventory = self.player.inventory

        for item_name in inventory:
            item = self.entities[item_name]

            name = item.display
            qty = inventory[item_name]
            value = item.value
            weight = item.weight
            total_value = value * qty
            total_weight = weight * qty

            new_row = [name, qty, value, total_value, weight, total_weight]

            table.append(new_row)

        self.ws.update_display(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def craft_item(self, item: str):
        item_data = self.entities[item]
        for cost in item_data.cost:
            required_item = cost[0]
            num = cost[1]

            if not self.player_home.is_in_storage(required_item, num):
                self.notification = f"You did not have enough {required_item}"
                return

        for cost in item_data.cost:
            self.player_home.storage[cost[0]] -= cost[1]

        self.player_home.add_to_storage(item, 1)

        self.notification = f"{item} successfully crafted"

    def display_regions(self):
        self.ws.update_display("Available regions: ")
        for i, region in enumerate(self.regions):
            region_data = self.regions[region]
            self.ws.update_display(f"{i}) {region_data.display}")

    def display_crafts(self):
        craftables = {
            key: value for key, value in self.entities.items() if value.is_craftable
        }

        craft_list = []

        for i, (name, data) in enumerate(craftables.items()):
            self.ws.update_display(f"\t {i+1}) {data.display} - {data.description}")
            craft_list.append(name)

        self.current_craftables = craft_list

    def display_main_menu(self):
        self.ws.update_display("", True)
        self.ws.update_display(f"Current location: {game_main.player.location.display}")
        game_main.display_inventory(self.player.location.display)

        self.ws.update_display(f"**{self.notification}**")
        self.notification = ""

        self.ws.update_display("""Available actions:
        1) Travel
        2) Forage
        3) Craft
        4) Exit
        """)

        self.action = "main"

    def drop_off_items(self):
        for item, qty in self.player.inventory.items():
            self.player_home.add_to_storage(item, qty)

        self.player.inventory = {}

    def start(self):
        self.player.location = self.regions.get("forest")
        self.forage(20)
        self.player.location = self.regions.get("home")
        print(os.getcwd())

        client_path = os.path.join("ui", "index.html")

        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", client_path])
        else:
            os.startfile(client_path)


ws_handler = WebsocketHandler()
ws_handler.run()

game_main = Game(ws_handler)
game_main.start()
