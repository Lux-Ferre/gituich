class UI{
	constructor() {
		this.panels = {
			main: {
				tab: $("#panelSelectorMain"),
				panel: $("#mainPanel")
			},
			inv: {
				tab: $("#panelSelectorInv"),
				panel: $("#invPanel")
			}
		}
				
		this.displayField = $("#displayData")
		this.notifications = $("#displayNotification")
		this.current_location = $("#displayCurrentLocation")
		this.player = $("#displayPlayer")
		this.inventory = $("#displayInventory")
	}
	
	changePanel(panelName){
		for (const [ident, panel] of Object.entries(this.panels)) {
			if(ident===panelName){
				panel.panel.removeClass("d-none")
				panel.tab.removeClass("panelSelectionTabInactive").addClass("panelSelectionTabActive")
			} else {
				panel.panel.addClass("d-none")
				panel.tab.removeClass("panelSelectionTabActive").addClass("panelSelectionTabInactive")
			}
		}
	}
	
	update_display(message){
		this.displayField.val(this.displayField.val() + message)
	}
	
	show_notification(message){
		this.notifications.val(message)
	}
	
	show_inventory(inv_items){
		this.inventory.empty()
		inv_items.forEach(item=>{
			const element_string = `<tr><td>${item.name}</td><td>${item.qty}</td><td>${item.value}</td><td>${item.total_value}</td><td>${item.weight}</td><td>${item.total_weight}</td></tr>`

			const element = $.parseHTML(element_string)
			this.inventory.append(element)
		})
		console.log(inv_items)
	}
	
	set_location(new_location){
		this.current_location.html(new_location)
	}
}

window.ui = new UI()