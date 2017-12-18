# -*- coding: utf-8 -*-
# code by: Boris Garber
# This code evaluates the time delays based on actual and scheduled time at station
# This version of the code uses a csv snapshot of the realtime data
# Future implementations will get the realtime data from postgres

import pandas as pd
from datetime import datetime, timedelta
#import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# import realtime data snapshot
realtime_data = {}
records = pd.read_csv("gtfs_vehicles.csv")
for rec in records.iterrows():
    vehicle_current_status = rec[1][10]
    if vehicle_current_status != 1: # only evaluate treains stopped at a station
        continue
    try:
        line = rec[1][4] # route_id
        if line not in ['1', '2', '3', '4', '5', '6', 'GS', 'L', 'SI']: # limit to lines in schedule
            continue
        stop = rec[1][9] #stop_id
        trip_id=rec[1][2]
        key = (trip_id, line, stop)
        timestamp = rec[1][11]
        timestamp_dt = datetime.utcfromtimestamp(timestamp-5*60*60) # convert from utc to est
        timestamp_dt = timestamp_dt.replace(year=1900, month=1, day=1)    # get consistent date as schedule for deltas
        realtime_data.setdefault(key, []).append(timestamp_dt)
    except:
        continue
    
# import schedule data
sched_trips = {}
with open('stop_times.txt') as f:
    next(f)
    for i, row in enumerate(f):
        row = row.strip().split(',')
        trip_id, arr, dep, stop_id  = row[:4]
        #if ('WKD' or 'SAT' or 'SUN') not in trip_id:
        #    continue
        trip_id_clean = trip_id.split('_')[1]+"_"+trip_id.split('_')[2]
        sub_line = trip_id.split('_')[2].split('.')[0] # make a consistent primary key
        if sub_line not in ['1', '2', '3', '4', '5', '6', 'GS', 'L', 'SI']: # limit to lines in schedule
                continue
        key = (trip_id_clean, sub_line, stop_id)
        if int(arr.split(":")[0])>23:   # get rid of crazy times
            arr=str(int(arr.split(":")[0])-24)+":"+arr.split(":")[1]+":"+arr.split(":")[2]
        arr = datetime.strptime(arr, '%H:%M:%S')
        arr = arr.replace(year=1900, month=1, day=1)    # get consistent date as realtime for deltas
        sched_trips.setdefault(key, []).append(arr)

# Analysis and plots
deltas_line={}
errors={}
for key, stops in realtime_data.items():
    trip_id, line, stop_id = key
    try:
        wait_time = realtime_data[key][0]-sched_trips[key][0]
        wait_time = wait_time.total_seconds()
        deltas_line.setdefault(line,[]).append(wait_time)
    except:
        errors.setdefault(line,[]).append(key)
        continue # trip_id mismatch
        
delays_line={}
for key in deltas_line:
    delays=[x for x in deltas_line[key] if x>0]
    delays_line[key]=delays

early_line={}
for key in deltas_line:
    early=[x for x in deltas_line[key] if x<0]
    early_line[key]=early

y1=[max(x) for x in deltas_line.values()]
y21=[len(x) for x in delays_line.values()]
y22=[len(x) for x in early_line.values()]

y2=[]
for i in range(len(y21)):
    y2.append(y21[i]/(y22[i]+y21[i]))

y3=[np.mean(x) for x in delays_line.values()]

x=[x for x in deltas_line.keys()]

y_pos = np.arange(len(x))

plt.figure()
plt.bar(y_pos, y1, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('seconds')
plt.title('Max wait time')

plt.figure()
plt.bar(y_pos, y2, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('ratio')
plt.title('ratio of delays over total')

plt.figure()
plt.bar(y_pos, y3, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('seconds')
plt.title('Average delay')

for line in x:
    plt.figure()
    plt.hist(deltas_line[line], alpha=0.5)
    plt.xlabel('delay (seconds)')
    plt.ylabel('frequency')
    title=line + " line histogram of delays"
    plt.title(title)
