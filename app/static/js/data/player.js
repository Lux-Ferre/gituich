class Player{
    constructor(player_name = "Player"){
        this.display = player_name
        this.location = null
        this.inventory = {}
        this.equipped_items = {}
        this.money = 0
	}	

    has_item(item, num){
        if (item in this.inventory){
			if (this.inventory[item] >= num){
				return true
			}
		}
        return false
	}

    add_item(item, qty){
        if (item in this.inventory){
            this.inventory[item] += qty
		} else{
            this.inventory[item] = qty
		}
	}

    reset_equips(){
        this.equipped_items = {
            head: null,
            neck: null,
            torso: null,
            left_hand: null,
            right_hand: null,
            belt: null,
            legs: null,
            feet: null,
        }
	}	
}