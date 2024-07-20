class DataStore{
	constructor(){
		this.entities = {}
		this.regions = {}
		this.player_homes = {}
		
		this.loadData()
	}
	
	loadData(){
		import("../data/entity_data.js").then(mod=>{
			this.entity_data = JSON.parse(mod.entity_json)
			for (const [key, value] of Object.entries(this.entity_data)){
				this.entities[key] = new Entity(value)
			}
		})
		
		import("../data/region_data.js").then(mod=>{
			this.region_data = JSON.parse(mod.region_json)
			for (const [key, value] of Object.entries(this.region_data)){
				this.regions[key] = new Region(value)
			}
		})
		
		import("../data/player_home_data.js").then(mod=>{
			this.player_home_data = JSON.parse(mod.player_home_json)
			for (const [key, value] of Object.entries(this.player_home_data)){
				this.player_homes[key] = new Home(value)
			}
		})
	}
}

window.ds = new DataStore()