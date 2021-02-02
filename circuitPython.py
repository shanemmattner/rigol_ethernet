import board
import busio

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import sqlite3 as sql

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

conn = sql.connect('i2c_data.db')

t_ms = 0

while(1):
    chan = AnalogIn(ads, ADS.P0)
    current = (chan.voltage - 1.65) /.055
    print(current)
    sleep(0.001)
