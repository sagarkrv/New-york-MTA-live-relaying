Get into exercise_2 folder

$ sparse run

Doing so would fill the postgresql table tweetwordcount in tcount database


For final results:
~~~~~~~~~~~~~~~~~~~~~
$ cat finalresults.py
You should be able to see the output

Usage 1: $ python finalresults.py 
displays all contents of tweetwordcount table

Usage 2: $ python finalresults.py this
displays the count of the word "this" in your stream


For histograms:
~~~~~~~~~~~~~~~~
Inside the exercise_2 folder, check whether histogram.py exists
$ cat histogram.py
If the output is seen, then issue the command
$ python histogram.py 3 8
