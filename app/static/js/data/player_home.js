class Home{
    constructor(data_pack){
        this.display = ""
        this.description = ""
        this.storage = {}
        this.storage_capacity = 0
        this.building_slots = {}
		
		for (const [key, value] of Object.entries(data_pack)){
			this[key] = value
		}
	}

    toString = () => {
		return `${this.display}: '${this.description}'`
	}
        

    add_to_storage(item, qty){
        if (item in this.storage){
            this.storage[item] += qty
		} else{
            this.storage[item] = qty
		}
	}
	
    is_in_storage(item, num){
        if (item in this.storage){
			if (this.storage[item] >= num){
				return true
			}
		}
        return false
	}	
}		