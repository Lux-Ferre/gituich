import random

from tabulate import tabulate
from collections import Counter
from typing import Type

import player
import utils
import regions
import entities


def forage(data: player.Player, quantity: int) -> tuple[str, player.Player]:
    region = data.location
    possible_items = []
    weights = []

    if not region.available_items:
        return "No items available here!", data

    for item in region.available_items:
        possible_items.append(item[0])
        weights.append(item[1])

    found_items = random.choices(population=possible_items, weights=weights, k=quantity)

    notify = f"You found: "
    item_count = Counter(found_items).most_common()

    for item in item_count:
        data.add_item(item[0], item[1])
        notify += f"{item[0].display}: {item[1]} |"

    return notify, data


def change_region(data: player.Player, selection: str, region_list: list[Type[regions.Region]]) -> tuple[str, player.Player]:
    if selection.isdigit():
        selection = int(selection)
        if 0 <= selection <= len(region_list):
            new_region = region_list[selection]
            data.location = new_region

            return f"You have moved to {new_region.display}.", data

    return "Invalid location selected. You have not moved.", data


def display_inventory(inv: dict):
    titles = ["Item", "Qty", "Value(ea)", "Value(tot)", "Weight(ea)", "Weight(tot)"]
    table = [titles]

    for item in inv:
        name = item.__name__
        qty = inv[item]
        value = item.value
        weight = item.weight
        total_value = value * qty
        total_weight = weight * qty

        new_row = [name, qty, value, total_value, weight, total_weight]

        table.append(new_row)

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def display_tools(player_tools: dict):
    titles = ["Name", "Qty", "Max Qty", "Description"]
    table = [titles]

    for tool in player_tools:
        name = tool.__name__
        qty = player_tools[tool]
        max_qty = tool.max_quantity
        desc = tool.description

        new_row = [name, qty, max_qty, desc]

        table.append(new_row)

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))


def get_available_crafts(data: player.Player) -> list:
    craftables = [
        entities.Basket,
        entities.Rope,
    ]

    print(f"Available crafts:")

    available = []

    for craft in craftables:
        max_allowed = craft.max_quantity
        if issubclass(craft, entities.Tool):
            if not data.has_tool(craft, max_allowed):
                available.append(craft)
        else:
            if not data.has_item(craft, max_allowed):
                available.append(craft)

    return available


def display_crafts(crafts: list):
    for i, craft in enumerate(crafts):
        print(f"\t {i+1}) {craft.display} - {craft.description}")


def display_regions(region_list: list[Type[regions.Region]]):
    print(f"Available regions:")

    for i, region in enumerate(region_list):
        print(f"{i}) {region.display}")


def display_notification(notify: str):
    print(f"**{notify}**")
    return ""


def craft_item(data: player.Player, item: entities.Craftable) -> tuple[str, player.Player]:
    for cost in item.cost:
        required_item = cost[0]
        num = cost[1]
        if not data.has_item(required_item, num):
            return f"You did not have enough {required_item.display}", data

    for cost in item.cost:
        data.inventory[cost[0]] -= cost[1]

    # noinspection PyTypeChecker
    if issubclass(item, entities.Tool):
        data.add_tool(item, 1)
    else:
        data.add_item(item, 1)

    return f"{item.display} successfully crafted", data


player_data = player.Player(display="Lux")

active = True
notification = ""

while active:
    utils.clear()
    print(f"Current location: {player_data.location.display}")
    display_inventory(player_data.inventory)
    display_tools(player_data.tools)

    notification = display_notification(notification)

    print("""Available actions:
    1) Travel
    2) Forage
    3) Craft
    4) Exit
    """)

    action = input("Pick an action: ")

    match action:
        case "1":
            all_regions = [regions.PlayerHouse, regions.Forest]
            display_regions(all_regions)
            user_input = input("Where to: ")

            notification, player_data = change_region(player_data, user_input, all_regions)

        case "2":
            notification, player_data = forage(player_data, 5)
        case "3":
            available_crafts = get_available_crafts(player_data)

            display_crafts(available_crafts)
            selection = int(input("Select craftable: ")) - 1        # Change to int and decrement to match list index

            new_item = available_crafts[selection]

            if new_item:
                notification, player_data = craft_item(player_data, new_item)

        case "4":
            active = False
        case _:
            notification = "That is an invalid action."
