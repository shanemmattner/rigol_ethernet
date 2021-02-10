# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 08:17:59 2021

@author: smattner
"""

import sqlite3 
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default='browser'

#for motor current ic
volt_amp_ratio = 0.055

#function that takes a table and returns a list containing
#  a df with the single test data
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

def make_traces(trace_buff, df_table, num_test):
    for x in range(num_test):
        df_plot = df_table[x]
        for col in df_plot:
            if ('TIME' in col) or ('index' in col):
                pass 
            elif ('Trigger' in col):
                df_plot[col] = df_plot[col] * 3
                trace_buff.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y1'))
            elif ('ANA_CURRENT' in col):
                df_plot[col] = df_plot[col].apply(lambda x: (x - 1.65) /volt_amp_ratio)
                trace_buff.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y1'))
            elif ('FLUKE_CURRENT' in col):
                df_plot[col]  = (df_plot[col]-3.5) 
                trace_buff.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col) ,opacity=0.8, yaxis='y1'))
            elif ('V_Triac_DS' in col):
                trace_buff.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y2'))
            else:
                pass 

    return trace_buff

conn = sqlite3.connect("usb/g3v2_motor_drive_signals_10-Feb-2021-11-48.db")
t_query = "SELECT sql from sqlite_master where type = 'table'"
df = pd.read_sql_query(t_query, conn)
conn.close()




lock_inrush = split_into_tests('lock_inrush')
# lock_stall = split_into_tests('lock_stall')
unlock_inrush = split_into_tests('unlock_inrush')
# unlock_stall = split_into_tests('unlock_stall')

#make traces from all the data
trace_buf = []
make_traces(trace_buf, lock_inrush,1)
make_traces(trace_buf, unlock_inrush,1)


fig =  go.Figure(data=trace_buf[:])
fig.update_layout(
            xaxis_title = "Time (s)",
            yaxis_title = "Volts (V)",
            showlegend = True,
            hovermode='closest',
            yaxis2 = dict
                (
                    side = 'right'
                )
            )

fig.show()