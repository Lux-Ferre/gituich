class Player:
    def __init__(self, player_name: str = "Player"):
        self.display = player_name
        self.location = None
        self.inventory = {}
        self.tools = {}
        self.money = 0

    def has_tool(self, tool: str, num: int):
        if tool in self.tools:
            if self.tools[tool] >= num:
                return True

    def has_item(self, item: str, num: int):
        if item in self.inventory:
            if self.inventory[item] >= num:
                return True

        return False

    def add_tool(self, tool: str, num: int):
        if tool in self.tools:
            self.tools[tool] += num
        else:
            self.tools[tool] = num

    def add_item(self, item: str, num: int):
        if item in self.inventory:
            self.inventory[item] += num
        else:
            self.inventory[item] = num
