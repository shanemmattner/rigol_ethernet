from instruments import DS1000Z
import numpy as np
import pandas as pd
import ds1054z_cp as dscp
import sqlite3 as sql
import time

#from ds1054z import DS1054Z 
def main():

    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)

    scope.stop()
    print("currently displayed channels: ", str(scope.displayed_channels))
    scope.single()
    time.sleep(1)
    #wait until the scope has stopped running
    #TODO: make sure we don't sit here forever
    t_count = 0
    while(scope.running != False and t_count < 10000):
        t_count = t_count + 1

    print(str(scope.running))
    scope.stop()
    print("Getting sample data")
    samples_list = scope.get_waveform_samples('CHAN1')
    df = pd.DataFrame(samples_list, columns = ['samples'])
    df['time']=scope.waveform_time_values
    

    conn = sql.connect('triac.db')
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_list = []
    for name in tables:
        table_list.append(name[0])
    print(table_list)
    df.to_sql('traic', conn, if_exists='replace')
 
if __name__ == "__main__":
    main()
