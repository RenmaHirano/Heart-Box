import RPi.GPIO as GPIO
import time
import spidev

"""A/D converter"""
def readadc(ch):
    command1 = 0xd | (ch<<1)
    command1 <<= 3
    ret = spi.xfer2([command1,0,0])
    y = (ret[0]&0x3)<<8 | ret[1]
    return y


"""spidev setting"""
GPIO.setmode(GPIO.BCM)
spi=spidev.SpiDev()
spi.open(0, 0) 
spi.max_speed_hz = 1000000


"""main"""
try:
    while True:
        val0 = readadc(0)
        val1 = readadc(1)
        print(val0, val1)
        time.sleep(0.2)

except KeyboardInterrupt:
    pass

spi.close()
