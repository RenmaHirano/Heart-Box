import websocket
import ast
try:
    import thread
except ImportError:
    import _thread as thread
import spidev
import RPi.GPIO as GPIO
import time
import sys
import pygame
import math

PEAK = 100
LED = 5


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

    # A/D converter
    def ReadPulse(self, val):
        self.adc = self.spi.xfer2([1, (8 + val) << 4, 0])
        self.data = ((self.adc[1] & 3) << 8) + self.adc[2]
        return self.data

    # detect peak and send
    def peak(self):
        try:
            while True:
                self.analog_level = self.ReadPulse(self.adc_channel)

                # Detecting peaks
                if (self.analog_level == 0):
                    time.sleep(self.delay)
                    continue

                if ((self.analog_level < self.Criteria) and (self.pulse_flg == 1)):  # peak down
                    # print("analog_level = {}".format(self.analog_level))
                    self.pulse_flg = 0
                    break

                if (self.analog_level < self.Criteria):  # keep low
                    self.pulse_flg = 0
                else:  # keep high or peak up
                    self.pulse_flg = 1

                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Exit!")


class Led_Controller():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # use GPIO No.(not pin No.)
        GPIO.setup(LED, GPIO.OUT)  # set pinmode
        GPIO.output(LED, False)

    def lchika(self):
        time.sleep(0.1)
        GPIO.output(LED, True)
        time.sleep(24/ws_client._Audio.beat)
        GPIO.output(LED, False)


class Audio():
    def __init__(self):
        pygame.mixer.pre_init(11025, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('suit2/kick.mp3')
        pygame.mixer.music.set_volume(10)
        self.beat = 0

    def play(self):
        while True:
            self.beat = math.exp(ws_client.val / 125.0) * (90 / 3500) + 60
            pygame.mixer.music.play(start=0.0)
            thread.start_new_thread(_Led_Controller.lchika, ())
            print(ws_client.val)
            print(self.beat)
            time.sleep(60/self.beat)


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
        self.username = "2"
        self.ready = True
        self.val = 0
        self.beat = 0.0
        self._Audio = Audio()

    def _on_message(self, ws, message):
        try:
            dict_message = ast.literal_eval(message)
            print("{} : {}".format(
                dict_message['client'], dict_message['val']))
            if(dict_message['client'] == 'box2'):
                self.val = int(dict_message['val'])

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
        thread.start_new_thread(self._Audio.play, ())

    def _run(self, *args):
        while True:
            while not self.ready:
                _heartbeat.peak()  # loop until peak is detected
                self.message = str(
                    "{'client':'" + str(self.username) + "'," + "'val':'peak'}")
                print("peak")
            self.ws.send(self.message)  # send peak
            time.sleep(0.3)
            self.ready = False

        self.ws.close()
        print("thread terminating...")

    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://3.19.252.112:9001/"  # AWS server IP(fixed)
ws_client = Websocket_Client(HOST_ADDR)
_heartbeat = Heartbeat()
_Led_Controller = Led_Controller()
ws_client.run_forever()
