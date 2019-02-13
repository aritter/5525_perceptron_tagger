import pstats, cProfile

#import pyximport; pyximport.install()
import sys
from Tagger import *

#import pickle
import cPickle as pickle
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tagger")
    parser.add_argument('--save', default=None)
    parser.add_argument('--dumpParameters', default='parameters.txt')
    parser.add_argument('--load', default=None)
    parser.add_argument('--profile', default=False, type=bool)
    parser.add_argument('--nIter', default=10, type=int)
    parser.add_argument('--train', default='wnut/train_notypes')
    parser.add_argument('--tag', default='wnut/dev_notypes')
    parser.add_argument('--taggerType', default='ViterbiTagger', help="ViterbiTagger|SemiMarkovViterbiTagger")

    args = parser.parse_args()

    if args.load:
        tagger = pickle.load(open(args.load, 'rb'))
    else:
        tagger = eval(args.taggerType)(args.train)
        if args.profile:
            cProfile.runctx("tagger.Train(args.nIter)", globals(), locals(), "Profile.prof")
            s = pstats.Stats("Profile.prof")
            s.strip_dirs().sort_stats("time").print_stats()
        else:
            tagger.Train(args.nIter)

    if args.tag:
        tagger.TagFile(args.tag)

    if args.save:
        pickle.dump(tagger, open(args.save, 'wb'))

    if args.dumpParameters:
        tagger.DumpParameters(args.dumpParameters)
