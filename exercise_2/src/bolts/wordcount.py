from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

    def process(self, tup):
        word = tup.values[0]
        self.counts[word] += 1
        self.emit([word, self.counts[word]])
        self.log('%s: %d' % (word, self.counts[word]))
        if word is not None and self.counts[word] is not None:        
            # Connect to the database
            conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")

            #Create the Database

            try:
            # CREATE DATABASE can't run inside a transaction
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                cur.execute("CREATE DATABASE tcount")
                conn.close()
            except psycopg2.Error as e:
                conn.rollback()
            else:
                conn.commit()

            conn.close()


            #Connecting to tcount
            conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

            #Create a Table
            #The first step is to create a cursor. 
            try:      
                cur = conn.cursor()
                cur.execute(
                            '''CREATE TABLE tweetwordcount
                               (word  TEXT PRIMARY KEY     NOT NULL,
                                count INT                  NOT NULL);''')
            except psycopg2.Error as e:
                conn.rollback()
            else:
                conn.commit()

            cur.close()

            # insert entries
            try:
                cur1 = conn.cursor()
                uCount = self.counts[word]
                uWord = word
                self.emit([uWord, uCount])
                cur1.execute("INSERT INTO tweetwordcount(word, count) VALUES (%s, %s)", (uWord, uCount))
            except psycopg2.IntegrityError:
                conn.rollback()
                cur1.execute("UPDATE tweetwordcount SET count = %s WHERE word = %s", (uCount, uWord))
            else:
                conn.commit()

            cur1.close()

            conn.commit()

            conn.close()

