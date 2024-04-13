class UI{
	constructor() {
		this.displayField = document.getElementById("displayData")
		this.notifications = document.getElementById("displayNotification")
		this.current_location = document.getElementById("displayCurrentLocation")
		this.player = document.getElementById("displayPlayer")
		this.inventory = $("#displayInventory")
	}
	
	update_display(instruction){
		const clear = instruction.clear
		const message = instruction.message
		
		if(clear){
			this.displayField.value = message
		} else {
			this.displayField.value = this.displayField.value + message
		}
	}
	
	show_notification(instruction){
		const message = instruction.payload.message
		this.notifications.value = message
	}
	
	show_inventory(instruction){
		const inv_items = instruction.payload.items
		this.inventory.empty()
		inv_items.forEach(item=>{
			const element_string = `<tr><td>${item.name}</td><td>${item.qty}</td><td>${item.value}</td><td>${item.total_value}</td><td>${item.weight}</td><td>${item.total_weight}</td></tr>`

			const element = $.parseHTML(element_string)
			this.inventory.append(element)
		})
		console.log(inv_items)
	}
	
	set_location(instruction){
		const new_location = instruction.payload.location
		this.current_location.textContent = new_location
	}
}