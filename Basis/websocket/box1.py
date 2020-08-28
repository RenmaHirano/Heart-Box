import websocket
import ast
try:
    import thread
except ImportError:
    import _thread as thread
import time
import spidev
import RPi.GPIO as GPIO
# import Pressure_Sensor


SOLENOID = 5
LED = 6
PEAK = 100


class Pressure_Sensor():

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000

    # A/D converter
    def readadc(self, ch):
        self.command1 = 0xd | (ch << 1)
        self.command1 <<= 3
        self.ret = self.spi.xfer2([self.command1, 0, 0])
        self.y = (self.ret[0] & 0x3) << 8 | self.ret[1]
        return self.y

    def run(self):
        self.val = max(self.readadc(0), self.readadc(1))
        # print(self.val)

    def close(self):
        self.spi.close()


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
        self.username = "box1"
        self.ready = True
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # use GPIO No.(not pin No.)
        GPIO.setup(LED, GPIO.OUT)  # set pinmode
        GPIO.setup(SOLENOID, GPIO.OUT)  # set pinmode
        GPIO.output(6, False)  # first state

    def on_message(self, ws, message):
        try:
            self.dict_message = ast.literal_eval(message)  # string -> dict
            print("{} : {}".format(
                self.dict_message['client'], self.dict_message['val']))

            # msg from suit? when peak?
            if (self.dict_message['client'].startswith("suit1")) and self.dict_message['val'] == 'peak':
                thread.start_new_thread(self.solenoid_controll, ())

        except SyntaxError:  # cannot change to dict
            message = message
            print("{} : {}".format(self.username, message))
        if not message.startswith("make connection"):
            self.ready = True

    def solenoid_controll(self):
        GPIO.output(LED, True)
        GPIO.output(SOLENOID, True)
        time.sleep(0.1)
        GPIO.output(LED, False)
        GPIO.output(SOLENOID, False)

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
                _Pressure_Sensor.run()
                self.message = str(
                    "{'client':'"+str(self.username)+"',"+"'val':'"+str(_Pressure_Sensor.val)+"'}")
                self.ws.send(self.message)
            self.ready = False

        self.ws.close()
        print("thread terminating...")

    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://3.19.252.112:9001/"  # AWS server IP(fixed)
ws_client = Websocket_Client(HOST_ADDR)
_Pressure_Sensor = Pressure_Sensor()
ws_client.run_forever()
