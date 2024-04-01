window.addEventListener('load', function() {
	window.websocket = new WebsocketHandler
	websocket.connect_to_socket()
	
	window.ui = new UI
})

document.getElementById("submissionForm").addEventListener("submit", event => {
	event.preventDefault();
	const formInput = document.getElementById("formInput")

	const message = formInput.value
	formInput.value = ""

	websocket.send(message)
});