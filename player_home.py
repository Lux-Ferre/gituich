class Home:
    def __init__(self, display="", description="", storage_capacity=0, building_slots={}):
        self.display = display
        self.description = description
        self.storage = {}
        self.storage_capacity = storage_capacity
        self.building_slots = building_slots

    def __str__(self):
        str_rep = f"""{self.display}: '{self.description}'"""

        return str_rep

    def add_to_storage(self, item: str, qty: int):
        if item in self.storage:
            self.storage[item] += qty
        else:
            self.storage[item] = qty

    def is_in_storage(self, item: str, num: int):
        if item in self.storage:
            if self.storage[item] >= num:
                return True

        return False


def get_default_home(home_id: str):
    default_home_data = {
        "clearing": {
            "display": "A Clearing",
            "description": "Just a clearing in a forest.",
            "storage_capacity": 50,
            "building_slots": {
                "storage": {0: None},
                "manufacturing": {0, None},
            }
        }
    }

    new_home_data = default_home_data[home_id]
    new_home = Home()

    for key, value in new_home_data.items():
        setattr(new_home, key, value)

    return new_home
