import websocket
import ast
try:
    import thread
except ImportError:
    import _thread as thread
import spidev
import time
import sys


class Heartbeat():

    def __init__(self):
        # Setting
        self.Vef = 3.3  # Working Voltage
        self.Criteria = 530  # Threshold
        self.adc_channel = 0  # SPI channel = 0
        self.delay = 0.01  # Reading interval
        self.pulse_flg = 0
    # Open access to SPI-paths
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1350000

    # Reading data from A/D converter
    def ReadPulse(self, val):
        self.adc = self.spi.xfer2([1, (8 + val) << 4, 0])
        self.data = ((self.adc[1] & 3) << 8) + self.adc[2]
        return self.data

    # main
    def peak(self):
        try:
            while True:
                self.analog_level = self.ReadPulse(self.adc_channel)

                # Detecting peaks
                if (self.analog_level == 0):
                    time.sleep(self.delay)
                    continue

                if ((self.analog_level < self.Criteria) and (self.pulse_flg == 1)):
                    print("analog_level = {}".format(self.analog_level))
                    self.pulse_flg = 0
                    break

                if (self.analog_level < self.Criteria):
                    self.pulse_flg = 0
                else:
                    self.pulse_flg = 1

                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Exit!")


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
        self.username = "suit"
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
        self.ws.send("username : {}".format(self.username))
        self.ready = False

        thread.start_new_thread(self._run, ())

    def _run(self, *args):
        while True:
            while not self.ready:
                # self.message = str("{'client':'"+str(self.username)+"',"+"'val':'"+str(self.val)+"'}")
                _heartbeat.peak()
                self.message = str(
                    "{'client':'"+str(self.username)+"',"+"'val':'peak'}")
            self.ws.send(self.message)
            self.ready = False

        self.ws.close()
        print("thread terminating...")

    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://3.133.103.49:9001/"
ws_client = Websocket_Client(HOST_ADDR)
_heartbeat = Heartbeat()
ws_client.run_forever()
