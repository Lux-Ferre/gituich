class Dragger{
	constructor() {
		this.draggables = {}
		this.container_dims = {
			height: 800,
			width: 800,
			tile: 20
		}
		
		this.map = this.generateMap(this.container_dims)
	}
	
	generateMap(dims){
		const w = dims.width
		const h = dims.height
		const t = dims.tile
		
		const cols = w/t
		const rows = h/t
		
		const map = new Array(rows);
		
		for (var i = 0; i < map.length; i++) {
			map[i] = new Array(cols).fill(0);
		}
		
		return map
	}
	
	createDraggableElement(colour){
		const ident = `${colour}Box`
		const elementString = `<div id="${ident}" class="draggable_item bg-${colour}" data-colour="${colour}"></div>`
		const element = $.parseHTML(elementString)
		$("#draggable_container").prepend(element)
		this.makeDraggable(ident, colour)
	}
	
	makeDraggable(ident, colour){
		this.draggables[ident] = $(`#${ident}`).draggabilly({
			containment: "#draggable_container",
			grid: [20, 20]
		})
		this.draggables[ident].on("dragEnd", (event, pointer)=>{
			window.dragger.registerMouseUp(this.draggables[ident])
		})
		this.displayCoords("start", colour, this.draggables[ident].data('draggabilly').position)
	}
	
	registerMouseUp(draggable){
		const start = draggable.data('draggabilly').startPosition
		const end = draggable.data('draggabilly').position
		
		window.dragger.setMap(draggable.data("colour"), draggable.data('draggabilly').startPosition, 4, 0)
		
		if(this.checkValidMove(4, end)){
			window.dragger.setMap(draggable.data("colour"), end, 4, 1)
			window.dragger.displayCoords("end", draggable.data("colour"), end)
			window.dragger.displayCoords("start", draggable.data("colour"), start)
		} else {
			draggable.draggabilly('setPosition', start.x, start.y)
			window.dragger.setMap(draggable.data("colour"), start, 4, 1)
			window.dragger.displayCoords("start", draggable.data("colour"), start)
			window.dragger.displayCoords("end", draggable.data("colour"), start)
		}
		window.dragger.printMap()
	}
	
	displayCoords(type, colour, coords){
		$(`#${type}_coords_${colour}`).text(`${coords.x}, ${coords.y}`)
	}
	
	checkValidMove(size, end){
		const x = end.x/20
		const y = end.y/20
		
		let valid = true
		outerLoop: for(let i=y; i<y+size; i++){
			innerLoop: for(let j=x; j<x+size; j++){
				if(window.dragger.map[i][j] !== 0){
					valid = false
					break outerLoop
				}
			}
		}
		return valid
	}
	
	setMap(ident, coords, size, type){
		const x = coords.x/20
		const y = coords.y/20
				
		for(let i=y; i<y+size; i++){
			for(let j=x; j<x+size; j++){
				window.dragger.map[i][j] = type
			}
		}
	}
	
	printMap(){
		let output = window.dragger.map.map(row=>{
			return row.join("")
		})
			.join("\n")
			.replaceAll("0", "⬜")
			.replaceAll("1", "⬛")
		
		console.log("\n\n" + output)
	}
}

window.addEventListener('load', function() {
	window.dragger = new Dragger()
})

$(document).on("click", "#button_container", function(e){
	if(e.target && e.target.nodeName == "BUTTON"){
		const button = $(e.target)
		const colour = button.data("colour")
		button.prop("disabled", true)
		window.dragger.createDraggableElement(colour)
	}
})