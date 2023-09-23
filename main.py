import random
from tabulate import tabulate

import regions
import tools


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


def craft_item(data: dict, item: tools.Craftable):
    for cost in item.cost:
        if data["inventory"][cost[0]] < cost[1]:
            return data

    for cost in item.cost:
        data["inventory"][cost[0]] -= cost[1]

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
while active:
    print(f"Current location: {player_data['location']}")
    display_inventory(player_data["inventory"])
    print(player_data["tools"])
    action = input("Enter an action: ")

    match action:
        case "travel":
            new_location = input("Where to: ")
            player_data["location"] = getattr(regions, new_location)
        case "forage":
            player_data["inventory"] = forage(player_data["location"], player_data["inventory"], 1)
        case "craft":
            new_item = input("Select craftable: ")
            player_data = craft_item(player_data, getattr(tools, new_item))
        case "exit":
            active = False
