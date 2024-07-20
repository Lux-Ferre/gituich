class Region{
	constructor(data_pack){
		this.display = ""
		this.available_items = []
		
		for (const [key, value] of Object.entries(data_pack)){
			this[key] = value
		}
	}
}