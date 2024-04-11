import threading
import json

from websocket_server import WebsocketServer


class WebsocketHandler:
    def __init__(self):
        self.server = WebsocketServer(port=8099)
        self.server.set_fn_new_client(self.on_connect)
        self.server.set_fn_message_received(self.message_received)
        self.game_client = None

    def run(self):
        server_thread = threading.Thread(target=self.server.run_forever)
        server_thread.start()

    def close(self):
        self.server.shutdown_gracefully()

    def on_connect(self, client: dict, server: WebsocketServer):
        print(f"New client connected and was given id {client['id']}")
        response = {
            "command": "log",
            "payload": f"You have been assigned client id: {client['id']}"
        }
        self.game_client = client
        game_main.display_main_menu()
        server.send_message(client, json.dumps(response))

    def message_received(self, client: dict, server: WebsocketServer, message: str):
        game_main.dispatch_action(message)

    def update_display(self, message, clear: bool = False):
        response = {
            "command": "display",
            "payload": {
                "clear": clear,
                "message": "\n" + message
            }
        }
        self.server.send_message(self.game_client, json.dumps(response))
