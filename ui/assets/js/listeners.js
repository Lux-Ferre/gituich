window.addEventListener('load', function() {
	window.websocket = new WebsocketHandler
	websocket.connect_to_socket()
	
	window.ui = new UI
})

$(document).on("click", "#displayRegions", function(e){
	if(e.target && e.target.nodeName == "BUTTON"){
		window.websocket.change_region(e.target.dataset.region)
	}
});

$(document).on("click", "#displayActions", function(e){
	if(e.target && e.target.nodeName == "BUTTON"){
		window.websocket.take_action(e.target.dataset.action)
	}
});

$(document).on("click", "#panelSelectionContainer", function(e){
	if(e.target){
		let node
		if ($(e.target).data("target-panel")) {
			node = $(e.target)
		} else if(e.target.nodeName === "SPAN"){
			node = $(e.target.parentNode)
		}
		if(node){
			window.ui.changePanel(node.data("target-panel"))
		}
	}
});