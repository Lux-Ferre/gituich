class UI{
	constructor() {
		this.dataField = document.getElementById("displayData")
		this.notification = document.getElementById("displayNotification")
		this.player = document.getElementById("displayPlayer")
		this.region = document.getElementById("displayRegions")
	}
	
	update_display(instruction){
		const clear = instruction.clear
		const message = instruction.message
		
		if(clear){
			this.dataField.value = message
		} else {
			this.dataField.value = this.dataField.value + message
		}
	}

	update_notification(instruction){
		const clear = instruction.clear
		const message = instruction.message

		if(clear){
			this.notification.value = message
		} else {
			this.notification.value = this.notification.value + message
		}
	}
}