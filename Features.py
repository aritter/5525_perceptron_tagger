# Features.py
# Licensing Information:  You are free to use or extend this project for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to The Ohio State University, including a link to http://aritter.github.io/courses/5525_spring19.html
#
# Attribution Information: This assignment was developed at The Ohio State University
# by Alan Ritter (ritter.1492@osu.edu).import sys

import re
import os
import string
import subprocess
import json

tagDict = {}
for line in open('tagDict'):
    (word, tag) = line.strip().split()
    tagDict[word] = tag

wordClusters = {}
for line in open('60K_clusters.bits.txt'):
    (cluster, word) = line.strip().split()
    wordClusters[word] = []
    for b in [4,8,12]:
        wordClusters[word].append(cluster[0:b])

def GetFeatures(word):
    features = []

    if tagDict.has_key(word):
        features.append("tagDict=%s" % tagDict[word])

    if wordClusters.has_key(word):
        for c in wordClusters[word]:
            features.append("cluster=%s" % c)

    features.append("word=%s" % word)
    features.append("word_lower=%s" % word.lower())
    if(len(word) >= 4):
        features.append("prefix=%s" % word[0:1].lower())
        features.append("prefix=%s" % word[0:2].lower())
        features.append("prefix=%s" % word[0:3].lower())
        features.append("suffix=%s" % word[len(word)-1:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-2:len(word)].lower())
        features.append("suffix=%s" % word[len(word)-3:len(word)].lower())

    if re.search(r'^[A-Z]', word):
        features.append('INITCAP')
    if re.match(r'^[A-Z]+$', word):
        features.append('ALLCAP')
    if re.match(r'.*[0-9].*', word):
        features.append('HASDIGIT')
    if re.match(r'.*[.,;:?!-+\'"].*', word):
        features.append('HASPUNCT')
    return features

class FeatureExtractor:
    def Extract(self, words, i):
        features = GetFeatures(words[i])
        return features
