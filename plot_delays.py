import json
import datetime
import numpy
import math
import pandas
import psycopg2

stations = {}
# Connecting to gtfs_count database
conn = psycopg2.connect(database="gtfs_count", user="postgres", password="pass", host="localhost", port="5432")
cur1 = conn.cursor()
cur1.execute("SELECT route_id, stop_id, current_status, vehtstamp  FROM gtfs_vehicles")
records = cur1.fetchall()
for rec in records:
    vehicle_current_status = rec[2]
    if vehicle_current_status != 1: # STOPPED_AT
        continue
    try:
        line = rec[0] # route_id
        if line not in ['1', '2', '3', '4', '5', '6', 'GS', 'L', 'SI']:
            print 'weird line', line
            continue
        stop = rec[1] #stop_id
        key = (line, stop)
        timestamp = rec[3] # datetime.datetime.utcfromtimestamp(vehicle['timestamp'])
        stations.setdefault(key, set()).add(timestamp)
    except:
        print 'weird vehicle', vehicle
        continue

    #if n_lines >= 10000:
    #    break


# Look at all intervals between subway arrivals
def next_whole_minute(t):
    return t+59 - (t+59)%60

deltas = []
next_subway = []
next_subway_by_time_of_day = [[] for x in xrange(24 * 60)]
next_subway_by_line_ts = []
next_subway_by_line_ls = []
next_subway_rush_hour = []
max_limit = 4 * 3600 # cap max value so that Seaborn's KDE works better
for key, values in stations.iteritems():
    line, stop = key
    values = sorted(values)
    print key, len(values)
    last_value = None
    for i in xrange(1, len(values)):
        last_value, value = values[i-1], values[i]
        if value - last_value >= max_limit:
            continue
        deltas.append(1. / 60 * (value - last_value))
        for t in xrange(next_whole_minute(last_value), value, 60):
            x = (t // 60 + 19 * 60) % (24 * 60) # 19 from UTC offset
            waiting_time = 1. / 60 * (value - t)
            next_subway_by_time_of_day[x].append(waiting_time)
            next_subway.append(waiting_time)
            next_subway_by_line_ts.append(waiting_time)
            next_subway_by_line_ls.append(line)
            if x >= 7 * 60 and x < 19 * 60:
                next_subway_rush_hour.append(waiting_time)

f = open('next_subway_waiting_time.txt','w')
for item in next_subway:
    f.write("%s\n" % str(item))
f.close()

f = open('next_subway_by_line_ts_waiting_time.txt','w')
for item in next_subway_by_line_ts:
    f.write("%s\n" % str(item))
f.close()

f = open('next_subway_by_line_ls_line.txt','w')
for item in next_subway_by_line_ls:
    f.write("%s\n" % str(item))
f.close()

f = open('next_subway_rush_hour_waiting_time.txt','w')
for item in next_subway_rush_hour:
    f.write("%s\n" % str(item))
f.close()

f = open('deltas.txt','w')
for item in deltas:
    f.write("%s\n" % str(item))
f.close()

