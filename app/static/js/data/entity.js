class Entity{
	constructor(data_pack){
		this.display = ""
		this.description= ""
		this.max_quantity = Infinity
		this.weight = 0
		this.value = 0
		this.cost = []
		this.is_obtainable = false
		this.is_alive = false
		this.is_craftable = false
		this.is_equippable = false
		this.foraging_multiplier = 1
		this.capacity = 0
		this.equipment_slots = []
		
		for (const [key, value] of Object.entries(data_pack)){
			this[key] = value
		}
	}
}