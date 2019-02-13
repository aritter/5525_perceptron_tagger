#!/bin/bash

function train_and_predict() {
    taggerType=$1
    trainFile=$2
    tagFile=$3
    outputFile=$4
    nIter=$5
    parametersOut=$6
    
    python run_tagger.py --nIter $nIter --taggerType $taggerType --train $trainFile --tag $tagFile --dumpParameters $parametersOut > $outputFile
}

function conll_eval() {
    gold=$1
    predicted=$2

    paste -d "\t" $gold $predicted | awk -F "\t" '{print $1 " " $2 " " $4}' | perl conlleval.pl | tee $predicted.eval
}

mkdir -p eval

time train_and_predict ViterbiTagger data/$1_train_universal.txt data/twitter_test_universal.txt eval/$1_ViterbiTagger.out 10 eval/$1_params.txt

#time train_and_predict ViterbiTagger data/twitter_ner_train.txt data/twitter_ner_test.txt eval/ner_ViterbiTagger.out 50 eval/$1_params.txt
#conll_eval data/twitter_ner_test.txt eval/ner_ViterbiTagger.out
