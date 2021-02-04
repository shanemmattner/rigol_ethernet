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

def stall_lock_test():
    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)
    scope.stop()
    print("currently displayed channels: ", str(scope.displayed_channels))
    #make sure the the trigger source is the correct channel
    scope.write(':TRIG:EDGE:SOUR CHAN3')
    scope.write(':TRIG:EDGE:SLOP NEG')
    
    
    
    time.sleep(1)
    scope.single()
    GPIO.output(lock_pin, GPIO.HIGH)
    time.sleep(0.5)
    print("GPIO high")
    GPIO.output(lock_pin, GPIO.LOW)
    while(scope.running):
        print("scope still running, lock stall")
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
    df.to_sql('lock_stall', conn, if_exists='append')
    conn.close()



#Need to set the oscilloscope to trigger on the output going low
def stall_unlock_test():
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()

    #make sure the the trigger source is the correct channel
    scope.write(':TRIG:EDGE:SOUR CHAN4')
    scope.write(':TRIG:EDGE:SLOP NEG')
    scope.write(':TRIG:EDGE:LEV 1')

    #scope.run()
    time.sleep(1)
    scope.single()
    GPIO.output(unlock_pin, GPIO.HIGH)
    time.sleep(0.5)
    print("GPIO high")
    GPIO.output(unlock_pin, GPIO.LOW)
    while(scope.running):
        print("scope still running, unlock stall")
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
    df.to_sql('unlock_stall', conn, if_exists='append')
    conn.close()



def inrush_lock_test():
   
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()

    scope.write(':TRIG:EDGE:SOUR CHAN3')
    scope.write(':TRIG:EDGE:SLOP POS')
    scope.write(':TRIG:EDGE:LEV 1')


    scope.single()
    time.sleep(1)
    GPIO.output(lock_pin, GPIO.HIGH)
    time.sleep(1)
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
    scope.write(':TRIG:EDGE:SOUR CHAN4')
    scope.write(':TRIG:EDGE:SLOP POS')
    scope.write(':TRIG:EDGE:LEV 1')

    scope.single()
    time.sleep(1)
    GPIO.output(unlock_pin, GPIO.HIGH)
    time.sleep(1)
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
    for x in range(2):
        inrush_lock_test()
        time.sleep(3)
        stall_lock_test()
        time.sleep(3)
        inrush_unlock_test()
        time.sleep(3)
        stall_unlock_test()
        time.sleep(3)
 
if __name__ == "__main__":
    main()
