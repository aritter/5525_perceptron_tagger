# Tagger.py
#
# Licensing Information:  You are free to use or extend this project for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to The Ohio State University, including a link to http://aritter.github.io/courses/5525_spring19.html
#
# Attribution Information: This assignment was developed at The Ohio State University
# by Alan Ritter (ritter.1492@osu.edu).

import sys

import numpy as np

from scipy.sparse import csr_matrix
from Data import LinearChainData

class Tagger(object):
    def __init__(self, average=True):
        self.useAveraging = average

    def ComputeThetaAverage(self):
        self.thetaAverage = self.theta

    def PrintableSequence(self, sequence):
        return [self.train.tagVocab.GetWord(x) for x in sequence]

    def DumpParameters(self, outFile):
        fOut = open(outFile, 'w')
        sortedParams = (np.argsort(self.thetaAverage, axis=None)[::-1])[0:500]
        for i in sortedParams:
            (tag1ID, tag2ID, featureID) = np.unravel_index(i, self.theta.shape)
            fOut.write("%s %s %s %s\n" % (self.train.tagVocab.GetWord(tag1ID), self.train.tagVocab.GetWord(tag2ID), self.train.vocab.GetWord(featureID), self.thetaAverage[tag1ID,tag2ID,featureID]))
        fOut.close()

    def Train(self, nIter):
        for i in range(nIter):
            nSent = 0
            for (s,g) in self.train.featurizedSentences:
                if len(g) <= 1:         #Skip any length 1 sentences - some numerical issues...
                    continue
                z = self.Viterbi(s, self.theta, len(g))

                sys.stderr.write("Iteration %s, sentence %s\n" % (i, nSent))
                sys.stderr.write("predicted:\t%s\ngold:\t\t%s\n" % (self.PrintableSequence(z), self.PrintableSequence(g)))
                nSent += 1
                self.UpdateTheta(s,g,z, self.theta, len(g))
        if self.useAveraging:
            self.ComputeThetaAverage()

class ViterbiTagger(Tagger):
    def __init__(self, inFile, average=True):
        self.train = LinearChainData(inFile)
        self.useAveraging = average

        self.ntags    = self.train.tagVocab.GetVocabSize()
        self.theta    = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.thetaSum = np.zeros((self.ntags, self.ntags, self.train.vocab.GetVocabSize()))   #T^2 parameter vectors (arc-emission CRF)
        self.nUpdates = 0

    def TagFile(self, testFile):
        self.test = LinearChainData(testFile, vocab=self.train.vocab)
        for i in range(len(self.test.sentences)):
            featurizedSentence = self.test.featurizedSentences[i][0]
            sentence = self.test.sentences[i]
            if self.useAveraging:
                v = self.Viterbi(featurizedSentence, self.thetaAverage, len(sentence))
            else:
                v = self.Viterbi(featurizedSentence, self.theta, len(sentence))
            words = [x[0] for x in sentence]
            tags  = self.PrintableSequence(v)
            for i in range(len(words)):
                print "%s\t%s" % (words[i], tags[i])
            print ""

    def Viterbi(self, featurizedSentence, theta, slen):
        """Viterbi"""

        #TODO: Implement the viterbi algorithm (with backpointers)
        viterbiSeq = [self.train.tagVocab.GetID('NOUN') for x in range(featurizedSentence.shape[0])]

        return viterbiSeq


    #Structured Perceptron update
    def UpdateTheta(self, sentenceFeatures, 
                          goldSequence, 
                          viterbiSequence,
                          theta,
                          slen):
        
        ntags = self.ntags
        START_TAG = self.train.tagVocab.GetID('START')
        nFeatures = self.train.vocab.GetVocabSize()

        for i in range(0,slen):
            #TODO: update parameters if viterbiSequence[i] != goldSequence[i] or viterbiSequence[i-1] != goldSequence[i-1]
            pass
