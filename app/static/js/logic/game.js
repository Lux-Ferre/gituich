class Game{
	constructor(){
		this.player = new Player("Lux")
		this.player_home = window.ds.player_homes.clearing
		this.current_craftables = null
	}

	change_region(new_region){
		this.player.location = ds.regions[new_region]|| ds.regions["home"]

		if (this.player.location === ds.regions["home"]){
			this.drop_off_items()
		}

		const region_display_name = this.player.location.display

		window.ui.show_notification(`Location changed to ${region_display_name}`)
		window.ui.set_location(region_display_name)
		this.display_inventory(this.player.location.display)
	}		

	forage(quantity = 1){
		const possible_items = []
		const weights = []
		const current_region = this.player.location
		
		if (current_region.available_items.length === 0){
			window.ui.show_notification("No items available here!")
			return
		}

		current_region.available_items.forEach(datum=>{
			possible_items.push(datum.id)
			weights.push(datum.weight)
		})

		const found_items = {}

		for(let i = 0; i < quantity; i++){
			const item = window.t.w_rand(possible_items, weights)
			if(item in found_items){
				found_items[item] += 1
			} else {
				found_items[item] = 1
			}
		}

		let notify = "You found: "

		const sorted_items = Object.entries(found_items).sort((a, b) => b[1] - a[1])
		
		sorted_items.forEach(datum=>{
			this.player.add_item(datum[0], datum[1])
			notify += `${window.ds.entities[datum[0]].display}: ${datum[1]} |`
		})
	
		window.ui.show_notification(notify)
		this.display_inventory(this.player.location.display)
	}

    display_inventory(inventory_id){
		let inventory
		if (inventory_id === "Your home"){
			inventory = this.player_home.storage
		} else{
            inventory = this.player.inventory
		}	

        const item_list = []

		Object.keys(inventory).forEach(item_name => {
			const item = window.ds.entities[item_name]

            const name = item.display
			const qty = inventory[item_name]
			const value = item.value
			const weight = item.weight
			const total_value = value * qty
			const total_weight = weight * qty

            item_list.push({
                "name": name,
                "qty": qty,
                "value": value,
                "weight": weight,
                "total_value": total_value,
                "total_weight": total_weight
            })
		})

        window.ui.show_inventory(item_list)
	}	

    craft_item(item){
        const item_data = window.ds.entities[item]
		item_data.cost.forEach(cost =>{
			const id = cost.id
			const qty = cost.qty
			
			if(!this.player_home.is_in_storage(id, qty)){
				window.ui.show_notification(`You did not have enough ${required_item}`)
				return
			}
		})
		
		item_data.cost.forEach(cost =>{
			const id = cost.id
			const qty = cost.qty
			
			this.player_home.storage[id] -= qty
		})


        this.player_home.add_to_storage(item, 1)

        window.ui.show_notification(`${item} successfully crafted`)
	}
	
    display_regions(){
        window.ui.update_display("Available regions: ")
		Object.values(window.ds.regions).forEach((region, i) => {
			window.ui.update_display(`${i}) ${region.display}`)
		})
	}
	
    drop_off_items(){
		for (const [key, value] of Object.entries(this.player.inventory)){
			this.player_home.add_to_storage(key, value)
		}
		
		this.player.inventory = {}
	}
	
	start(){
		this.player_home = window.ds.player_homes["clearing"]
		this.change_region("home")
	}
}

window.game = new Game()