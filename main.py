# Full imports
import random
import subprocess
import os
import sys

# Partial imports
from queue import Queue
from collections import Counter

# Local imports
import regions
from websocket_handler import WebsocketHandler
from player import Player
from entities import generate_entities
from player_home import get_default_home


class Game:
    def __init__(self, ws, ui_queue: Queue):
        self.ws: WebsocketHandler = ws
        self.ui_queue = ui_queue
        self.client_connected = False
        self.player = Player("Lux")
        self.player_home = get_default_home("clearing")
        self.regions = regions.generate_regions()
        self.entities = generate_entities()
        self.current_craftables = None

    def dispatch_action(self, instruction):
        match instruction["method"]:
            case "change_region":
                self.change_region(instruction)
            case "forage":
                self.forage()
            case "craft":
                pass
                # selection = int(instruction["payload"]) - 1
                #
                # crafted_item = self.current_craftables[selection]
                #
                # self.craft_item(crafted_item)
                # game_main.display_inventory(self.player.location.display)
            case "close_game":
                self.ws.update_display("", True)
                self.ws.show_notification("Game closed.")
                self.ws.close()

    def change_region(self, selection: dict):
        new_region = selection["payload"]
        self.player.location = self.regions.get(new_region, self.regions["home"])

        if self.player.location == self.regions["home"]:
            self.drop_off_items()

        region_display_name = self.player.location.display

        self.ws.show_notification(f"Location changed to {region_display_name}")
        self.ws.set_location(region_display_name)
        self.display_inventory(self.player.location.display)

    def forage(self, quantity: int = 1):
        possible_items = []
        weights = []
        current_region = self.player.location

        if not current_region.available_items:
            self.ws.show_notification("No items available here!")
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

        self.ws.show_notification(notify)
        self.display_inventory(self.player.location.display)

    def display_inventory(self, inventory_id: str):
        if inventory_id == "Your home":
            inventory = self.player_home.storage
        else:
            inventory = self.player.inventory

        item_list = []

        for item_name in inventory:
            item = self.entities[item_name]

            name = item.display
            qty = inventory[item_name]
            value = item.value
            weight = item.weight
            total_value = value * qty
            total_weight = weight * qty

            item_list.append({
                "name": name,
                "qty": qty,
                "value": value,
                "weight": weight,
                "total_value": total_value,
                "total_weight": total_weight
            })

        self.ws.show_inventory(item_list)

    def craft_item(self, item: str):
        item_data = self.entities[item]
        for cost in item_data.cost:
            required_item = cost[0]
            num = cost[1]

            if not self.player_home.is_in_storage(required_item, num):
                self.ws.show_notification(f"You did not have enough {required_item}")
                return

        for cost in item_data.cost:
            self.player_home.storage[cost[0]] -= cost[1]

        self.player_home.add_to_storage(item, 1)

        self.ws.show_notification(f"{item} successfully crafted")

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

    def drop_off_items(self):
        for item, qty in self.player.inventory.items():
            self.player_home.add_to_storage(item, qty)

        self.player.inventory = {}

    def start(self):
        client_path = os.path.join("ui", "index.html")

        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", client_path])
        else:
            os.startfile(client_path)

        while True:
            instruction = self.ui_queue.get()   # {"method": "methodName", "payload": {}}

            self.dispatch_action(instruction)


if __name__ == "__main__":
    user_input_queue = Queue()

    ws_handler = WebsocketHandler(user_input_queue)
    ws_handler.run()

    game_main = Game(ws_handler, user_input_queue)
    game_main.start()
