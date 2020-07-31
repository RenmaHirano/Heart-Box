import spidev
import time
import sys

"""Setting"""
start_time = time.time()
adc_channel = 0 # SPI channel = 0
delay = 0.01 # Reading interval

"""Open access to SPI-paths"""
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

"""Saving data"""
f = open('pulse.csv', 'w')
nowtime = 0.0
analog_level = 0

"""Reading data from A/D converter"""
def ReadPulse(val):
    adc = spi.xfer2([1, (8 + val)<<4, 0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data

"""main"""
try:
    while True:
        analog_level = ReadPulse(adc_channel)
        now_time = time.time() - start_time

        data = "{}, {}\n".format(now_time, analog_level)
        
        f.write(data)
        time.sleep(delay)

except KeyboardInterrupt:
    print("Exit!")
    f.close()
