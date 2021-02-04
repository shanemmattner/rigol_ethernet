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


volt_amp_ratio = 0.055

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
# lock_stall = split_into_tests('lock_stall')
# unlock_inrush = split_into_tests('unlock_inrush')
# unlock_stall = split_into_tests('unlock_stall')

# fig = lock_inrush[0].plot()
# fig.show()

trace_buf = []

for x in range(len(lock_inrush)):
    df_plot = lock_inrush[x]
    for col in df_plot:
        if ('TIME' in col) or ('index' in col):
            pass 
         # elif ('CHAN1' in col):
         #    df_plot[col] = df_plot[col].apply(lambda x: (x *5))
         #    trace_buf.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y1'))
        elif ('CHAN2' in col):
            trace_buf.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y2'))
        elif ('CHAN3' in col):
            df_plot[col] = df_plot[col].apply(lambda x: (x - 1.65) /0.055)
            trace_buf.append(go.Scattergl(x=df_plot['TIME'],y=df_plot[col],mode='lines',name=str(col),opacity=0.8, yaxis='y1'))
        else:
            pass


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