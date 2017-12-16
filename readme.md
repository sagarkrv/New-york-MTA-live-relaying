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

$ python sample4.py
