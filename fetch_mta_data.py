############# Author: Pragnesh K R V ###################################
######## New York MTA mass live data fetch #############################
from __future__ import absolute_import, print_function, unicode_literals
from google.transit import gtfs_realtime_pb2
import urllib
import psycopg2
import contextlib
import time
import sys
from optparse import OptionParser
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from collections import Counter
from streamparse.bolt import Bolt

@contextlib.contextmanager
def timer(name="duration"):
    'Utility function for timing execution'
    start=time.time()
    yield
    duration=time.time()-start
    print("{0}: {1} second(s)".format(name,duration))
def is_number(s):
    try:
        complex(s) # for int, long. float and complex
    except ValueError:
        return False
    return True
class gtfs_mtafetch():
    def initialize(self):
        self.counts = Counter()
        self.fetch_counts = Counter()
        self.tuc = []
        # Connect to the database
        conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")
        #Create the Database
        try:
        # CREATE DATABASE can't run inside a transaction
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute("CREATE DATABASE gtfs_count")
            conn.close()
        except psycopg2.Error as e:
            conn.rollback()
        else:
            conn.commit()
        conn.close()
        #Connecting to gtfs_count
        conn = psycopg2.connect(database="gtfs_count", user="postgres", password="pass", host="localhost", port="5432")
        #Create a Table
        #The first step is to create a cursor.
        try:
            cur = conn.cursor()
            cur.execute(
                        '''CREATE TABLE gtfs_tuc
                           (
                           tstamp BIGINT,
                           entity_id INTEGER,
                           trip_id VARCHAR(20),
                           start_date INTEGER,
                           route_id VARCHAR (5),
                           stop_id VARCHAR (4),
                           stop_sequence VARCHAR (10),
                           arrival_time BIGINT,
                           arrival_delay INTEGER,
                           departure_time BIGINT,
                           departure_delay INTEGER,
                           schedule_relationship VARCHAR (10),
                           PRIMARY KEY (tstamp, entity_id, trip_id, start_date, route_id, stop_id))                           
                           ;''')
            cur.execute(
                        '''CREATE TABLE gtfs_alerts
                           (
                           tstamp BIGINT,
                           entity_id INTEGER,
                           trip_id VARCHAR (20),
                           route_id VARCHAR (5),
                           cause VARCHAR (20),
                           effect VARCHAR (20),
                           txt VARCHAR (20), PRIMARY KEY (tstamp, entity_id, trip_id, route_id) )
                           ;''')
            cur.execute(
                        '''CREATE TABLE gtfs_vehicles
                           (
                           tstamp BIGINT,
                           entity_id INTEGER,
                           trip_id VARCHAR (20),
                           start_date INTEGER,
                           route_id VARCHAR (5),
                           vehicle VARCHAR (5),
                           position_lat real,
                           position_long real,
                           current_stop_sequence VARCHAR (10),
                           stop_id VARCHAR (4),
                           current_status INTEGER,
                           vehtstamp BIGINT,
                           congestion_level INTEGER,
                           occupancy_status INTEGER,
                           PRIMARY KEY (tstamp, entity_id, trip_id) )
                           ;''')
        except psycopg2.Error as e:
            conn.rollback()
            print('DB table creation failure')
            print(e.pgerror)
            print(e.diag.message_detail)
        else:
            conn.commit()
            print('success')
        cur.close()
        self.conn = conn
    def process(self):
#        word = tup.values[0]
#        counts["word"] += 1
#        emit([word, self.counts[word]])
#        self.log('%s: %d' % (word, self.counts[word]))
        #Connecting to gtfs_count
        conn = psycopg2.connect(database="gtfs_count", user="postgres", password="pass", host="localhost", port="5432")
        cur1 = self.conn.cursor()
        feed = gtfs_realtime_pb2.FeedMessage()
        response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=71be30927bb73971710696ba3f1f6a0b&feed_id=1')
        feed.ParseFromString(response.read())
        for entity in feed.entity:
             tuc_list = []
             if entity.HasField('trip_update'):
                 tuc = entity.trip_update
                 self.tuc = [
                              {
                              'tstamp': feed.header.timestamp,
                              'entity_id': entity.id,
                              'trip_id' : tuc.trip.trip_id,
                              'start_date' : tuc.trip.start_date,
                              'route_id' : tuc.trip.route_id,
                              'stop_id' : tuc.stop_time_update[i].stop_id,
                              'stop_sequence' : tuc.stop_time_update[i].stop_sequence,
                              'arrival_time' : tuc.stop_time_update[i].arrival.time,
                              'arrival_delay' : tuc.stop_time_update[i].arrival.delay,
                              'departure_time' : tuc.stop_time_update[i].departure.time,
                              'departure_delay' : tuc.stop_time_update[i].departure.delay,
                              'schedule_relationship' : tuc.stop_time_update[i].schedule_relationship
                              }
                              for i in range(len(tuc.stop_time_update))
                            ]
                 sql = '''
                       INSERT INTO gtfs_tuc (tstamp, entity_id , trip_id, start_date, route_id, stop_id , stop_sequence, arrival_time, arrival_delay, departure_time, departure_delay, schedule_relationship)
                        SELECT unnest( %(tstamp)s)::bigint,
                               unnest( %(entity_id)s)::int,
                               unnest( %(trip_id)s),
                               unnest( %(start_date)s)::int,
                               unnest( %(route_id)s),
                               unnest( %(stop_id)s),
                               unnest( %(stop_sequence)s),
                               unnest( %(arrival_time)s)::bigint,
                               unnest( %(arrival_delay)s)::int,
                               unnest( %(departure_time)s)::bigint,
                               unnest( %(departure_delay)s)::int,
                               unnest( %(schedule_relationship)s) '''
                 tstamp=[r['tstamp'] for r in self.tuc]
                 entity_id=[r['entity_id'] for r in self.tuc]
                 trip_id=[r['trip_id'] for r in self.tuc]
                 start_date=[r['start_date'] for r in self.tuc]
                 route_id=[r['route_id'] for r in self.tuc]
                 stop_id=[r['stop_id'] for r in self.tuc]
                 stop_sequence=[r['stop_sequence'] for r in self.tuc]
                 arrival_time=[r['arrival_time'] for r in self.tuc]
                 arrival_delay=[r['arrival_delay'] for r in self.tuc]
                 departure_time=[r['departure_time'] for r in self.tuc]
                 departure_delay=[r['departure_delay'] for r in self.tuc]
                 schedule_relationship = [r['schedule_relationship'] for r in self.tuc]
                 try:
                     cur1.execute(sql, locals())
                 except psycopg2.IntegrityError:
                     self.conn.rollback()
                 except psycopg2.Error as e:
                     print(e.diag.message_detail)
                 else:
                     self.conn.commit()
                     self.counts["tuc"] += len(tuc.stop_time_update)
             if entity.HasField('vehicle'):
                 veh = entity.vehicle
                 try:
                     cur1.execute("INSERT INTO gtfs_vehicles VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (feed.header.timestamp, entity.id, veh.trip.trip_id, veh.trip.start_date, veh.trip.route_id, veh.vehicle.id, veh.position.latitude, veh.position.longitude, veh.current_stop_sequence, veh.stop_id, veh.current_status, veh.timestamp, veh.congestion_level, veh.occupancy_status))
                 except psycopg2.IntegrityError:
                     self.conn.rollback()
                 else:
                     self.conn.commit()
             if entity.HasField('alert'):
                 alert = entity.alert
                 self.alerts = [
                                {
                                 'tstamp': feed.header.timestamp,
                                 'entity_id': entity.id,
                                 'trip_id' : alert.informed_entity[i].trip.trip_id,
                                 'route_id' : alert.informed_entity[i].trip.route_id,
                                 'cause' : alert.cause,
                                 'effect' : alert.effect,
                                 'txt' : alert.header_text.translation[0].text
                                }
                                for i in range(len(alert.informed_entity))
                              ]
                 sql = '''
                       INSERT INTO gtfs_alerts (tstamp, entity_id , trip_id, route_id, cause, effect, txt)
                        SELECT unnest( %(tstamp)s)::bigint,
                               unnest( %(entity_id)s)::int,
                               unnest( %(trip_id)s),
                               unnest( %(route_id)s),
                               unnest( %(cause)s),
                               unnest( %(effect)s),
                               unnest( %(txt)s)  '''
                 tstamp    = [r['tstamp'] for r in self.alerts]
                 entity_id = [r['entity_id'] for r in self.alerts]
                 trip_id   = [r['trip_id'] for r in self.alerts]
                 route_id  = [r['route_id'] for r in self.alerts]
                 cause     = [r['cause'] for r in self.alerts]
                 effect    = [r['effect'] for r in self.alerts]
                 txt       = [r['txt'] for r in self.alerts]
                 try:
                     cur1.execute(sql, locals())
                 except psycopg2.IntegrityError:
                     self.conn.rollback()
                 except psycopg2.Error as e:
                     self.conn.rollback()
                     print(e.diag.message_detail)
                 else:
                     self.conn.commit()
                     self.counts["alerts"] += len(alert.informed_entity)
        cur1.close()
        self.conn.commit()
        print('stop time records insertion progress: ', self.counts["tuc"])
        print('Alert records insertion progress: ', self.counts["alerts"])        
        # self.conn.close()


# parse commandline arguments
op = OptionParser()
argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args)>0:
    to_ct = argv[0]
    if is_number(to_ct):
        to_ct = int((complex(to_ct)).real)
else:
    to_ct = 5
x = gtfs_mtafetch()
x.initialize()
for i in range(to_ct):
    start = time.time()
    with timer('fast'):
        x.process()
    duration = time.time() - start
    time.sleep(30 - duration)


