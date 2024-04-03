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


class Game:
    def __init__(self, ws):
        self.ws: WebsocketHandler = ws
        self.client_connected = False
        self.player = Player("Lux")
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

        game_main.player.location = self.regions.get(new_location, "home")
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

        self.ws.update_display(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

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

        self.ws.update_display(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    def craft_item(self, item: str):
        item_data = self.entities[item]
        for cost in item_data.cost:
            required_item = cost[0]
            num = cost[1]

            if not self.player.has_item(required_item, num):
                self.notification = f"You did not have enough {required_item}"
                return

        for cost in item_data.cost:
            self.player.inventory[cost[0]] -= cost[1]

        if item_data.is_tool:
            self.player.add_tool(item, 1)
        else:
            self.player.add_item(item, 1)

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
        game_main.display_inventory()
        game_main.display_tools()

        self.ws.update_display(f"**{self.notification}**")
        self.notification = ""

        self.ws.update_display("""Available actions:
        1) Travel
        2) Forage
        3) Craft
        4) Exit
        """)

        self.action = "main"

    def start(self):
        self.player.location = self.regions.get("forest")
        self.forage(20)
        self.player.location = self.regions.get("home")
        print(os.getcwd())

        client_path = r"ui\index.html"

        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", client_path])
        else:
            os.startfile(client_path)

        os.startfile(r"ui\index.html")


class WebsocketHandler:
    def __init__(self):
        self.server = WebsocketServer(port=8099)
        self.server.set_fn_new_client(self.on_connect)
        self.server.set_fn_message_received(self.message_received)
        self.game_client = None

    def run(self):
        server_thread = threading.Thread(target=self.server.run_forever)
        server_thread.start()

    def close(self):
        self.server.shutdown_gracefully()

    def on_connect(self, client: dict, server: WebsocketServer):
        print(f"New client connected and was given id {client['id']}")
        response = {
            "command": "log",
            "payload": f"You have been assigned client id: {client['id']}"
        }
        self.game_client = client
        game_main.display_main_menu()
        server.send_message(client, json.dumps(response))

    def message_received(self, client: dict, server: WebsocketServer, message: str):
        game_main.dispatch_action(message)

    def update_display(self, message, clear: bool = False):
        response = {
            "command": "display",
            "payload": {
                "clear": clear,
                "message": "\n" + message
            }
        }
        self.server.send_message(self.game_client, json.dumps(response))


ws_handler = WebsocketHandler()
ws_handler.run()

game_main = Game(ws_handler)
game_main.start()
