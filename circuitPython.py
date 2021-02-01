import board
import busio

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import sqlite3 as sql

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

ads.mode = Mode.CONTINUOUS
conn = sql.connect('i2c_data.db')

t_ms = 0

while(1):
    chan = AnalogIn(ads, ADS.P0)
    print(chan.value)
    sleep(0.001)
