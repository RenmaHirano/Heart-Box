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
        self.pulse = 0
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

                if ((self.analog_level < self.Criteria) and (self.pulse == 1)):
                    print("Pulse")
                    self.pulse = 0
                elif (self.analog_level < self.Criteria):
                    self.pulse = 0
                else:
                    self.pulse = 1

                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Exit!")


_heartbeat = Heartbeat()
_heartbeat.peak()
