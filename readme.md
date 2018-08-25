This is a data mining project developed using POSTGRESSQL, PSYCOPG2 & Python.
Live data from New York MTA is pulled from Google's API sources, stored in POSTGRES, and the results are visualized for statistical calculations. The whole project was executed in a few weeks, and completely on AWS EC2 instance.

## Step by step procedure :

1) Create a new instance using public amazon machine image ami-d4dd4ec3
2) Add a EBS device 100GB
2) Connect to the instance and
   $ fdisk -l

3) Note down the new volume
   Lets say it is /dev/xvdf
4) $ mkfs.ext4 /dev/xvdf
5) $ wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh
6) $ chmod +x ./setup_ucb_complete_plus_postgres.sh

7) ./setup_ucb_complete_plus_postgres.sh <*the device path from step 2*>
  ./setup_ucb_complete_plus_postgres.sh /dev/xvdf

8) $ mkdir /data
9) $ chmod a+rwx /data

    mount -t ext4 /dev/<your device> /data
    
    example: $ mount -t ext4 /dev/xvdf /data
10) $ chmod a+rwx /data
11) $ /data/start_postgres.sh





## Now create a new Python virtual environment so that these libraries dont break anything else in the system

$ virtualenv final_project

$ cd final_project

$ pip install psycopg2

$ pip install pandas

$ pip install numpy

$ easy_install --upgrade gtfs-realtime-bindings

$ /data/start_postgres.sh

$ psql -U "postgres"

$ python fetch_mta_data.py 30

 This would fill up the POSTGRES Database tables gtfs_vehicles, gtfs_alerts and gtfs_tuc (trip updates)
 30 stands for 30 fetches from the MTA end point separated across 30 seconds (15 min run time)
 
$ python generate_delay_data.py

spools the output of gtfs_vehicles in gtfs_vehicles.CSV file for data subsequent visualization in a graphical environment



Run the last python programme in a Python environment with MATPLOTLIB libary installed

$ python subway_analysis.py
