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