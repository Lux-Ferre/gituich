import random

from tabulate import tabulate
from collections import Counter

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


def craft_item(data: player.Player, item: entities.Craftable) -> tuple[str, player.Player]:
    for cost in item.cost:
        required_item = cost[0]
        num = cost[1]
        if not data.has_item(required_item, num):
            return f"You did not have enough {required_item}", data

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
            print(f"    0) Home")
            print(f"    1) Forest")
            selection = input("Where to: ")

            match selection:
                case "0":
                    player_data.location = regions.PlayerHouse
                case "1":
                    player_data.location = regions.Forest
                case _:
                    notification = "Invalid location selected. You have not moved."

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
