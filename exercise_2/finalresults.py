import psycopg2, sys
from optparse import OptionParser

#Connecting to tcount
conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

# parse commandline arguments
op = OptionParser()
op.add_option("--word",
              action="store_true", dest="print_report",
              help="Count number of occurrences of a word")

cur1 = conn.cursor()

argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args)>0:
    argv = argv[0]
else:
    argv = None

try:
    if argv is None:
        cur1.execute("SELECT word, count FROM tweetwordcount")
        records = cur1.fetchall()
        for idx, rec in enumerate(records):
            print idx, "word = ",  rec[0], "count = ", rec[1]
    else:
        cur1.execute("SELECT word, count FROM tweetwordcount WHERE word = %s ORDER BY %s", (argv, 'WORD'))
        records = cur1.fetchone()
        print "Total number of occurrences of ", records[0], ": ", records[1]
    
except psycopg2.Error as e:
    print(e.pgerror)
    print(e.diag.message_detail)

cur1.close()
conn.close()

