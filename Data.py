###################################################################################################
# Data.py
# Code for reading in CONLL format and extracting features
#
# Licensing Information:  You are free to use or extend this project for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to The Ohio State University, including a link to http://aritter.github.io/courses/5525_spring19.html
#
# Attribution Information: This assignment was developed at The Ohio State University
# by Alan Ritter (ritter.1492@osu.edu).
###################################################################################################

import sys
import math
import Features
from Vocab import Vocab

import numpy as np
import numpy as np

from scipy.sparse import csr_matrix

class Data(object):
    """ Reads in data in Conll format and extracts features... """
    def __init__(self, inFile):
        self.tags                = set()
        self.data                = self.ReadData(inFile)

    def ReadData(self, inFile):
        sentence  = []
        self.sentences = []
        for line in open(inFile):
            line = line.strip()
            if line == '':
                self.sentences.append(sentence)
                sentence = []
                continue
            #fields = line.split('\t')
            fields = line.split()
            if len(fields) == 2:
                #Word + tag
                (word,tag) = fields
            self.tags.add(tag)
            sentence.append((word,tag))
        return self.sentences

class LinearChainData(Data):
    def __init__(self, inFile, vocab=None):
        self.fe = Features.FeatureExtractor()
        Data.__init__(self, inFile)

        self.tagVocab = Vocab()   #Create a vocab for indexing tags
        self.tagVocab.GetID('START')
        for t1 in self.tags:
            self.tagVocab.GetID(t1)
        self.tagVocab.Lock()

        self.featurizedSentences = self.ExtractFeatures(vocab)

    def ExtractFeatures(self, vocab=None):
        featurizedSentences = []

        if vocab == None:
            self.vocab = Vocab()
            #Pass 1 (to figure out vocab size...)
            self.vocab.GetID('BIAS')
            for s in self.sentences:
                words = [w[0] for w in s]
                for i in range(len(s)):
                    for f in self.fe.Extract(words, i):
                        self.vocab.GetID(f)
            self.vocab.Lock()
        else:
            self.vocab = vocab

        #Pass 2 (read in the data...)
        for s in self.sentences:
            featurizedSentences.append(self.ExtractFeaturesSent(s))
        
        return featurizedSentences

    def ExtractFeaturesSent(self, s):
        """ Helper function for ExtractFeatures """
        sentenceTags     = np.zeros(len(s), dtype=np.int)

        MAX_FEATURES = 100000  #Maximum number of features per sentence (just set to some big number)
        BIAS = self.vocab.GetID('BIAS')

        #For creating csr_matrix
        sf_row = np.zeros(MAX_FEATURES, dtype=np.int)
        sf_col = np.zeros(MAX_FEATURES, dtype=np.int)
        sf_val = np.zeros(MAX_FEATURES)
        sf_idx = 0

        #print s
        words = [w[0] for w in s]

        for i in range(len(s)):
            sentenceTags[i] = self.tagVocab.GetID(s[i][1])

            sf_row[sf_idx] = i
            sf_col[sf_idx] = BIAS
            sf_val[sf_idx] = 1
            sf_idx += 1

            for f in self.fe.Extract([w[0] for w in s], i):
                featureID = self.vocab.GetID(f)
                if featureID < 0:
                    continue
                sf_row[sf_idx] = i
                sf_col[sf_idx] = featureID
                sf_val[sf_idx] = 1
                sf_idx += 1                
                
        sentenceFeatures = csr_matrix((sf_val[0:sf_idx], (sf_row[0:sf_idx], sf_col[0:sf_idx])), shape=(len(s), self.vocab.GetVocabSize()))
        return (sentenceFeatures.tocsr(),sentenceTags)
