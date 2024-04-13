//socket.addEventListener('open', function (event) {
//	socket.send('Connection Established');
//});

class WebsocketHandler{
	constructor(){
		this.dispatch_map = {
			log: this.log_this,
			display: this.display_message,
			notify: this.show_notification,
			set_location: this.set_location,
			show_inventory: this.show_inventory,
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
		console.log(parsed_message)
		const command = parsed_message.command
		this.dispatch_map[command].apply(this, [parsed_message])
	}
	
	log_this(parsed_message){
		console.log(parsed_message)
	}
	
	display_message(parsed_message){
		window.ui.update_display(parsed_message.payload)
	}
	
	show_notification(parsed_message){
		window.ui.show_notification(parsed_message)
	}
	
	set_location(parsed_message){
		window.ui.set_location(parsed_message)
	}
	
	show_inventory(parsed_message){
		window.ui.show_inventory(parsed_message)
	}
	
	take_action(action){
		const data_packet = {
			method: action,
			payload: ""
		}

		this.send(JSON.stringify(data_packet))
	}
	
	change_region(new_region){
		const data_packet = {
			method: "change_region",
			payload: new_region
		}
		
		this.send(JSON.stringify(data_packet))
	}
}