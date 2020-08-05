import websocket
import ast
try:
    import thread
except ImportError:
    import _thread as thread
import time

import RPi.GPIO as GPIO


class Websocket_Client():

    def __init__(self, host_addr):

        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp(host_addr,
                                         on_message=lambda ws, msg: self.on_message(
                                             ws, msg),
                                         on_error=lambda ws, msg: self.on_error(
                                             ws, msg),
                                         on_close=lambda ws: self.on_close(
                                             ws),
                                         on_open=lambda ws: self.on_open(ws))
        self.username = "box"
        self.ready = True
        GPIO.setmode(GPIO.BCM)  # use GPIO No.(not pin No.)
        GPIO.setup(2, GPIO.OUT)  # LED
        GPIO.setup(17, GPIO.OUT)  # solenoid
        self.beat = True

    def on_message(self, ws, message):
        try:
            self.dict_message = ast.literal_eval(message)  # string -> dict
            print("{} : {}".format(
                self.dict_message['client'], self.dict_message['val']))

            # msg from suit? when peak?
            if (self.dict_message['client'].startswith("suit")) and self.dict_message['val'].startswith("peak"):
                thread.start_new_thread(self.led_controll, ())

                GPIO.output(17, self.beat)  # move solenoid
                self.beat = not self.beat  # invert flg

        except SyntaxError:  # cannot change to dict
            message = message
            print("{} : {}".format(self.username, message))
        if not message.startswith("make connection"):
            self.ready = True

    def led_controll(self):
        GPIO.output(2, True)
        time.sleep(0.3)
        GPIO.output(2, False)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        self.ws.send("username : {}".format(self.username))
        self.ready = False

        thread.start_new_thread(self.run, ())

    def run(self, *args):
        while True:
            while not self.ready:
                time.sleep(0.1)
                # self.val = 200
                # self.message = str("{'client':'"+str(self.username)+"',"+"'val':'"+str(self.val)+"'}")
                # self.ws.send(self.message)
            self.ready = False

        self.ws.close()
        print("thread terminating...")

    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://3.19.252.112:9001/"  # AWS server IP(fixed)
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()
