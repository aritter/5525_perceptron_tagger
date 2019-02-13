# accuracy.py
#
# Licensing Information:  You are free to use or extend this project for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to The Ohio State University, including a link to http://aritter.github.io/courses/5525_spring19.html
#
# Attribution Information: This assignment was developed at The Ohio State University
# by Alan Ritter (ritter.1492@osu.edu).

import sys

predicted = []
gold = []

for line in open(sys.argv[1]):
    fields = line.strip().split()
    if len(fields) == 2:
        predicted.append(fields)

for line in open(sys.argv[2]):
    fields = line.strip().split()
    if len(fields) == 2:    
        gold.append(fields)

accuracy = float(len([i for i in range(len(predicted)) if predicted[i][1] == gold[i][1]])) / len(predicted)

#print [(predicted[i], gold[i]) for i in range(len(predicted))]

print "ACCURACY=%s" % accuracy
