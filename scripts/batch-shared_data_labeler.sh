#!/usr/bin/env bash
CORPUS=$1

./word_to_char_labeler.py $CORPUS gold
./word_to_char_labeler.py $CORPUS training
./char_delimiter.py $CORPUS