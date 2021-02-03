from instruments import DS1000Z
import numpy as np
import pandas as pd
import ds1054z_cp as dscp
import sqlite3 as sql
import time
import RPi.GPIO as GPIO

lock_pin = 4
unlock_pin = 17


def GPIO_setup():
    GPIO.cleanup()
    time.sleep(0.1)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lock_pin, GPIO.OUT)
    GPIO.setup(unlock_pin, GPIO.OUT)

def inrush_lock_test():
   
    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)

    scope.stop()
    print("currently displayed channels: ", str(scope.displayed_channels))
    scope.run()
    time.sleep(0.5)
    scope.tforce()
    GPIO.output(lock_pin, GPIO.HIGH)
    time.sleep(1)
    print("GPIO high")
    GPIO.output(lock_pin, GPIO.LOW)
    scope.stop()

    print("Getting sample data")
    time_data = scope.waveform_time_values
    df = pd.DataFrame(time_data, columns = ['TIME'])
    chan4_data = scope.get_waveform_samples('CHAN4')
    df.insert(1, 'CHAN4', chan4_data)
    chan3_data = scope.get_waveform_samples('CHAN3')
    df.insert(1, 'CHAN3', chan3_data)
    chan2_data = scope.get_waveform_samples('CHAN2')
    df.insert(1, 'CHAN2', chan2_data)
    chan1_data = scope.get_waveform_samples('CHAN1')
    df.insert(1, 'CHAN1', chan1_data)

    print(df) 

    conn = sql.connect('g3v2_motor_drive_signals.db')
    df.to_sql('lock_inrush', conn, if_exists='append')
    conn.close()


def inrush_unlock_test():
   
    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)

    scope.stop()
    print("currently displayed channels: ", str(scope.displayed_channels))
    scope.run()
    time.sleep(0.5)
    scope.tforce()
    GPIO.output(unlock_pin, GPIO.HIGH)
    time.sleep(1)
    print("GPIO high")
    GPIO.output(unlock_pin, GPIO.LOW)
    scope.stop()


    print("Getting sample data")
    time_data = scope.waveform_time_values
    df = pd.DataFrame(time_data, columns = ['TIME'])
    chan4_data = scope.get_waveform_samples('CHAN4')
    df.insert(1, 'CHAN4', chan4_data)
    chan3_data = scope.get_waveform_samples('CHAN3')
    df.insert(1, 'CHAN3', chan3_data)
    chan2_data = scope.get_waveform_samples('CHAN2')
    df.insert(1, 'CHAN2', chan2_data)
    chan1_data = scope.get_waveform_samples('CHAN1')
    df.insert(1, 'CHAN1', chan1_data)
    
    
    

    print(df) 

    conn = sql.connect('g3v2_motor_drive_signals.db')
    df.to_sql('unlock_inrush', conn, if_exists='append')
    conn.close()

    
#from ds1054z import DS1054Z 
def main():

    GPIO_setup()
    
    #inrush_lock_test()
    for x in range(5):
        time.sleep(5)
        inrush_lock_test()
        time.sleep(5)
        inrush_unlock_test()
    #append test number

    #get time data
    
   # print("Scope not running anymore")
   # print(str(scope.running))
   # scope.stop()
   # print("Getting sample data")
   # samples_list = scope.get_waveform_samples('CHAN1')
   # df = pd.DataFrame(samples_list, columns = ['samples'])
   # df['time']=scope.waveform_time_values
   # print(df) 

    #conn = sql.connect('triac.db')
    #tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #table_list = []
    #for name in tables:
    #    table_list.append(name[0])
    #print(table_list)
    #df.to_sql('traic', conn, if_exists='replace')
 
if __name__ == "__main__":
    main()
