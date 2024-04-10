class Player:
    def __init__(self, player_name: str = "Player"):
        self.display = player_name
        self.location = None
        self.inventory = {}
        self.equipped_items = {}
        self.money = 0

    def has_item(self, item: str, num: int):
        if item in self.inventory:
            if self.inventory[item] >= num:
                return True

        return False

    def add_item(self, item: str, num: int):
        if item in self.inventory:
            self.inventory[item] += num
        else:
            self.inventory[item] = num

    def reset_equips(self):
        self.equipped_items = {
            "head": "",
            "neck": "",
            "torso": "",
            "left_hand": "",
            "right_hand": "",
            "belt": "",
            "legs": "",
            "feet": "",
        }
