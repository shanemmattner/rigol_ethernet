# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 08:17:59 2021

@author: smattner
"""

import sqlite3 
import pandas as pd


def split_into_tests(table_name):    
    conn = sqlite3.connect("g3v2_motor_drive_signals.db")
    t_query = "SELECT * from " + str(table_name)
    df = pd.read_sql_query(t_query, conn)
    conn.close()
    
    df_list = []
    for x in range(int(len(df)/1200)):
        start = x * 1200
        end = start + 1200
        t_df = df[start:end]
        t_df.drop(columns = ['index'], inplace=True)
        df_list.append( t_df )
    
    return df_list



conn = sqlite3.connect("g3v2_motor_drive_signals.db")
t_query = "SELECT sql from sqlite_master where type = 'table'"
df = pd.read_sql_query(t_query, conn)
conn.close()
print(df)

lock_inrush = split_into_tests('lock_inrush')

lock_stall = split_into_tests('lock_stall')
unlock_inrush = split_into_tests('unlock_inrush')
unlock_stall = split_into_tests('unlock_stall')

lock_inrush[0].plot()
