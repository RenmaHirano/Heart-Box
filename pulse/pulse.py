import spidev
import time
import sys

"""Setting"""
Vref = 3.3 # Working Voltage
Criteria = 530 # Threshold
adc_channel = 0 # SPI channel = 0
delay = 0.01 # Reading interval
pulse = 0

"""Open access to SPI-paths"""
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

"""Reading data from A/D converter"""
def ReadPulse(val):
    adc = spi.xfer2([1, (8 + val)<<4, 0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data

"""main"""
try:
    while True:
        analog_level = ReadPulse(adc_channel)

        """Detecting peaks"""
        if (analog_level == 0):
            time.sleep(delay)
            continue
        
        if ((analog_level < Criteria) and (pulse == 1)):
            print("Pulse")
        
        if (analog_level < Criteria):
            pulse = 0
        
        else:
            pulse = 1
        
        time.sleep(delay)

except KeyboardInterrupt:
    print("Exit!")