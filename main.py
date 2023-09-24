import random
from tabulate import tabulate

import regions
import entities


def forage(region, inv: dict, quantity: int) -> dict:
    possible_items = []
    weights = []

    for item in region.available_items:
        possible_items.append(item[0])
        weights.append(item[1])

    found_items = random.choices(population=possible_items, weights=weights, k=quantity)

    for item in found_items:
        if item in inv:
            inv[item] += 1
        else:
            inv[item] = 1

    return inv


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


def craft_item(data: dict, item: entities.Craftable):
    for cost in item.cost:
        if data["inventory"][cost[0]] < cost[1]:
            return data

    for cost in item.cost:
        data["inventory"][cost[0]] -= cost[1]

    # noinspection PyTypeChecker
    if issubclass(item, entities.Tool):
        if item in data["tools"]:
            data["tools"][item] += 1
        else:
            data["tools"][item] = 1

    return data


player_data = {
    "location": None,
    "inventory": {},
    "tools": {},
    "money": 0
}

player_data["inventory"] = forage(regions.Forest, player_data["inventory"], 20)

active = True
invalid_action = False

while active:
    print(f"Current location: {player_data['location']}")
    display_inventory(player_data["inventory"])
    display_tools(player_data["tools"])

    if invalid_action:
        print("You entered an invalid action.")
        invalid_action = False

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
                    new_location = "Forest"
                case _:
                    new_location = None

            if new_location:
                player_data["location"] = getattr(regions, new_location)

        case "2":
            player_data["inventory"] = forage(player_data["location"], player_data["inventory"], 1)
        case "3":
            print(f"Available crafts:")
            print(f"    1) Basket - {entities.Basket.description}")
            selection = input("Select craftable: ")

            match selection:
                case "1":
                    new_item = "Basket"
                case _:
                    new_item = None

            if new_item:
                player_data = craft_item(player_data, getattr(entities, new_item))

        case "4":
            active = False
        case _:
            invalid_action = True
