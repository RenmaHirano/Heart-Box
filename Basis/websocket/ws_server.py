from websocket_server import WebsocketServer
import logging

class Websocket_Server():

    def __init__(self, host, port):
        self.client_id_username_map = {}
        self.server = WebsocketServer(port, host = host, loglevel = logging.DEBUG)

    def new_client(self, client, server):
        print("new client connected and was given id {}".format(client['id']))
        self.server.send_message(client,"make connection : success!!")

    def client_left(self, client, server):
        print("client({}) disconnected".format(client['id']))

    def message_received(self, client, server, message):
        if message.startswith("init:username:"):
            username = message.replace("init:username:", "")
            print(username)
            self.client_id_username_map[client["id"]] = username
            self.server.send_message_to_all(message)
        else:

            self.server.send_message_to_all(message)
    
    def run(self):
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received) 
        self.server.run_forever()

IP_ADDR = "0.0.0.0"
PORT=9001
ws_server = Websocket_Server(IP_ADDR, PORT)
ws_server.run()

