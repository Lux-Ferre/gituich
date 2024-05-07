class UI{
	constructor() {
		this.mainPanel = $("#mainPanel")
		this.invPanel = $("#invPanel")
		
		this.panelSelectorMain = $("#panelSelectorMain")
		this.panelSelectorInv = $("#panelSelectorInv")
		
		this.displayField = $("#displayData")
		this.notifications = $("#displayNotification")
		this.current_location = $("#displayCurrentLocation")
		this.player = $("#displayPlayer")
		this.inventory = $("#displayInventory")
	}
	
	changePanel(panelName){
		const panelList = [this.mainPanel, this.invPanel]
		panelList.forEach(panel=>{
			panel.addClass("d-none")
		})
		switch(panelName) {
			case "main":
				this.mainPanel.removeClass("d-none")
				break;
			case "inv":
				this.invPanel.removeClass("d-none")
				break;
			default:
				console.log(panelName)
		} 
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