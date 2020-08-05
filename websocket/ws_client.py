import websocket
import ast
try:
    import thread
except ImportError:
    import _thread as thread
import time


class Websocket_Client():

    def __init__(self, host_addr):

        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp(host_addr,
                                         on_message=lambda ws, msg: self._on_message(
                                             ws, msg),
                                         on_error=lambda ws, msg: self._on_error(
                                             ws, msg),
                                         on_close=lambda ws: self._on_close(
                                             ws),
                                         on_open=lambda ws: self._on_open(ws))
        self.ready = True

    def _on_message(self, ws, message):
        try:
            dict_message = ast.literal_eval(message)
            print("{} : {}".format(
                dict_message['client'], dict_message['val']))
        except SyntaxError:
            message = message
            print("{} : {}".format(self.username, message))
        if not message.startswith("make connection"):
            self.ready = True

    def _on_error(self, ws, error):
        print(error)

    def _on_close(self, ws):
        print("### closed ###")

    def _on_open(self, ws):
        self.username = input("please input username : ")

        while True:

            if self.username.startswith("box"):
                self.val = 222
                self.ws.send("username : {}".format(self.username))
                break
            elif self.username.startswith("suit"):
                self.val = 999
                self.ws.send("username : {}".format(self.username))
                break
            else:
                print('*** username must start with "box" or "suit" ***')
                self.username = input("*** please input username *** : ")
        self.ready = False

        thread.start_new_thread(self._run, ())

    def _run(self, *args):
        while True:
            while not self.ready:
                time.sleep(0.1)
                self.message = str(
                    "{'client':'"+str(self.username)+"',"+"'val':'"+str(self.val)+"'}")
            self.ws.send(self.message)
            self.ready = False

        self.ws.close()
        print("thread terminating...")

    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://3.19.252.112:9001/"  # AWS server IP(fixed)
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()
