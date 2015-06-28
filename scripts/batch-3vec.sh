#!/bin/bash
CORPUS=$1
CRF_C2=$2
W2V_DIM=$3
W2V_WIN=$4
W2V_NEG=$5
W2V_OP=$6
W2V_FEAT=$7

./word_to_char_labeler.py $CORPUS gold
./word_to_char_labeler.py $CORPUS training

./crfsuite_feature_writer.py $CORPUS
./crfsuite_caller.py $CORPUS control $CRF_C2 learn
./crfsuite_caller.py $CORPUS control $CRF_C2 tag
./concatenate_labeled_chars_to_word.py $CORPUS control $CRF_C2

./char_delimiter.py $CORPUS
./word2vec_model_trainer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG
./crfsuite_word2vec_feature_writer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG gold $W2V_OP $W2V_FEAT
./crfsuite_word2vec_feature_writer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG training $W2V_OP $W2V_FEAT
./crfsuite_caller.py $CORPUS w2v $CRF_C2 learn $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT
./crfsuite_caller.py $CORPUS w2v $CRF_C2 tag $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT
./concatenate_labeled_chars_to_word.py $CORPUS w2v $CRF_C2 $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT

./scorer.py $CORPUS control $CRF_C2
./scorer.py $CORPUS w2v $CRF_C2 $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT
