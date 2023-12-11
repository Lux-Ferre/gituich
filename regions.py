class Region:
    def __init__(self, display: str, available_items: list[tuple[str, int]]):
        self.available_items = available_items
        self.display = display


def generate_regions():
    region_data = {
        "home": {
            "display": "Your home",
            "available_items": [],
            },
        "forest": {
            "display": "Forest",
            "available_items": [
                ("stick", 65),
                ("vine", 10),
                ("stone", 25),
            ]
        },
    }

    regions = {}
    for region, data in region_data.items():
        regions[region] = Region(data["display"], data["available_items"])

    return regions
