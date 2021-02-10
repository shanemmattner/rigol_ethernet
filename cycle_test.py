from instruments import DS1000Z
import numpy as np
import pandas as pd
import ds1054z_cp as dscp
import sqlite3 as sql
import time
import os
import RPi.GPIO as GPIO

lock_pin = 4
unlock_pin = 17
trig_pin = 27
trig_chan = 'CHAN1'

timebase_offset = 0.02
timebase_scale = 0.01
timebase_offset_inrush = 0.05

chan1_label = 'Trigger'
chan2_lbael = 'ANA_CURRENT'
chan3_label = 'FLUKE_CURRENT'
chan4_label = 'V_Triac_DS'



def log_to_db(df, table):
    try:
        conn = sql.connect('g3v2_motor_drive_signals.db')
        print("connected")
        df.to_sql(table, conn, if_exists='append')
        conn.close()

    except Exception as e:
        print(e)

        

def set_trig_inrush(t_scope):
    t_scope.write(':TRIG:EDGE:SOUR '+ trig_chan)
    t_scope.write(':TRIG:EDGE:SLOP POS')
    t_scope.write(':TRIG:EDGE:LEV 1')
    t_scope.write(':ACQ:TYPE HRES')
    print(str(t_scope.query(':ACQ:TYPE?')))
    #set time offset to 0ms
    t_scope.timebase_offset = timebase_offset_inrush
    t_scope.timebase_scale = timebase_scale
    
def set_trig_stall(t_scope):
    t_scope.write(':TRIG:EDGE:SOUR '+ trig_chan)
    t_scope.write(':TRIG:EDGE:SLOP POS')
    t_scope.write(':TRIG:EDGE:LEV 1')
    t_scope.write(':ACQ:TYPE?')
    t_scope.write(':ACQ:TYPE HRES')

    #set time offset to 0ms
    t_scope.timebase_offset = timebase_offset
    t_scope.timebase_scale = timebase_scale


def get_data(t_scope):

    time_data = t_scope.waveform_time_values
    df = pd.DataFrame(time_data, columns = ['TIME'])
    chan4_data = t_scope.get_waveform_samples('CHAN4')
    df.insert(1, chan4_label, chan4_data)
    chan3_data = t_scope.get_waveform_samples('CHAN3')
    df.insert(1, chan3_label, chan3_data)
    chan2_data = t_scope.get_waveform_samples('CHAN2')
    df.insert(1, chan2_lbael, chan2_data)
    chan1_data = t_scope.get_waveform_samples('CHAN1')
    df.insert(1, chan1_label, chan1_data)

    return df


def GPIO_setup():
    GPIO.cleanup()
    time.sleep(0.1)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lock_pin, GPIO.OUT)
    GPIO.setup(unlock_pin, GPIO.OUT)
    GPIO.setup(trig_pin, GPIO.OUT)

def stall_lock_test():
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()
    set_trig_stall(scope)
    
    time.sleep(1)
    scope.single()
    
    GPIO.output(lock_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(trig_pin, GPIO.HIGH)
    GPIO.output(lock_pin, GPIO.LOW)
    time.sleep(1)
    scope.stop()
    GPIO.output(trig_pin, GPIO.LOW)

    signal_df = get_data(scope)
    print(signal_df)
    log_to_db(signal_df,'lock_stall')
    


#Need to set the oscilloscope to trigger on the output going low
def stall_unlock_test():
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()

    set_trig_stall(scope)

    #scope.run()
    time.sleep(1)
    scope.single()
    
    GPIO.output(unlock_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(trig_pin, GPIO.HIGH)
    GPIO.output(unlock_pin, GPIO.LOW)
    time.sleep(1)
    scope.stop()
    GPIO.output(trig_pin, GPIO.LOW)
    
    
    df = get_data(scope)
    print(df)

    signal_df = get_data(scope)
    print(signal_df)
    log_to_db(signal_df,'unlock_stall')


def inrush_lock_test():
   
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()
    set_trig_inrush(scope)

    scope.single()
    time.sleep(1)
    GPIO.output(lock_pin, GPIO.HIGH)
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(lock_pin, GPIO.LOW)
    GPIO.output(trig_pin, GPIO.LOW)
    scope.stop()


    df = get_data(scope)
    print(df)


    signal_df = get_data(scope)
    print(signal_df)
    log_to_db(signal_df,'lock_inrush')


def inrush_unlock_test():
   
    scope = dscp.DS1054Z('169.254.145.221')
    scope.stop()
    set_trig_inrush(scope)

    scope.single()
    time.sleep(1)
    GPIO.output(unlock_pin, GPIO.HIGH)
    GPIO.output(trig_pin, GPIO.HIGH)

    time.sleep(1)
    GPIO.output(unlock_pin, GPIO.LOW)
    GPIO.output(trig_pin, GPIO.LOW)
    scope.stop()


    df = get_data(scope)
    print(df)

    signal_df = get_data(scope)
    print(signal_df)
    log_to_db(signal_df,'unlock_inrush')

   
def check_run_bit():
    f = open('run_testing.txt','r')
    msg = f.read()
    f.close()
    #having intermittent problems with errors for string index
    try:
        run = int(msg[0])
    except:
        f = open('run_testing.txt', 'w')
        f.write('0')
        f.close()
        run = 0
    if run == 1:
        return 1
    else:
        return 0

#from ds1054z import DS1054Z 
def cycle_test():
    print("Cycle testing...")

    time.sleep(3)
    inrush_lock_test()
    time.sleep(3)
    stall_lock_test()
    time.sleep(3)
    inrush_unlock_test()
    time.sleep(3)
    stall_unlock_test()
    time.sleep(3)



######################   RUNNING CODE    ################

GPIO_setup()

#set run bit to 0 on start up of this script
f = open('run_testing.txt', 'w')
f.write('0')
f.close()
    
while True:
    time.sleep(1)
    if check_run_bit()==1:
        cycle_test()
