
import psycopg2, sys
from optparse import OptionParser

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True


#Connecting to tcount
conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

# parse commandline arguments
op = OptionParser()
cur1 = conn.cursor()

argv = sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args)>0:
    from_ct = argv[0]
    to_ct   = argv[1]
    if is_number(from_ct):
        from_ct = int((complex(from_ct)).real)
    if is_number(to_ct):
        to_ct = int((complex(to_ct)).real)
else:
    argv = None

try:
    if argv is None:
        print('Enter python histogram.py 3 8')
        exit
    else:
        print(from_ct, to_ct)
        cur1.execute("SELECT word, count FROM tweetwordcount WHERE count BETWEEN %s AND %s", (from_ct, to_ct))
        records = cur1.fetchall()
        for idx, rec in enumerate(records):
            print idx, 'word = ',  rec[0], 'count = ', rec[1]

except psycopg2.Error as e:
    print(e.pgerror)
    print(e.diag.message_detail)

cur1.close()
conn.close()
