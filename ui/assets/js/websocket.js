//socket.addEventListener('open', function (event) {
//	socket.send('Connection Established');
//});

class WebsocketHandler{
	constructor(){
		this.dispatch_map = {
			log: this.log_this,
			display: this.display_message
		}
	}
	
	connect_to_socket(){
		const socket = new WebSocket('ws://localhost:8099');
		this.ws = socket
		this.ws.addEventListener('message', event => {
			this.dispatch_ws_message(event.data)
		});
	}
	
	send(message){
		this.ws.send(message)
	}
	
	dispatch_ws_message(message){
		const parsed_message = JSON.parse(message)
		const command = parsed_message.command
		this.dispatch_map[command].apply(this, [parsed_message])
	}
	
	log_this(parsed_message){
		console.log(parsed_message)
	}
	
	display_message(parsed_message){
		window.ui.update_display(parsed_message.payload)
	}
}