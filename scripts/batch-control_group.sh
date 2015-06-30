#!/usr/bin/env bash
CORPUS=$1
CRF_C2=$2

./crfsuite_feature_writer.py $CORPUS gold
./crfsuite_feature_writer.py $CORPUS training
./crfsuite_caller.py $CORPUS control $CRF_C2 learn
./crfsuite_caller.py $CORPUS control $CRF_C2 tag
./concatenate_labeled_chars_to_word.py $CORPUS control $CRF_C2
./scorer.py $CORPUS control $CRF_C2
