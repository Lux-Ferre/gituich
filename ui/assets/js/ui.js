class UI{
	constructor() {
		this.displayField = document.getElementById("displayField")
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
}