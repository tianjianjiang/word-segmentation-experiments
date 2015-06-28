#!/bin/bash
CORPUS=$1
W2V_DIM=$2
W2V_WIN=$3
W2V_NEG=$4
W2V_OP=$5
W2V_FEAT=$6
CRF_C2=$7

./word_to_char_labeler.py $CORPUS gold
./word_to_char_labeler.py $CORPUS training
./char_delimiter.py $CORPUS
./word2vec_model_trainer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG
./crfsuite_word2vec_feature_writer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG gold $W2V_OP $W2V_FEAT
./crfsuite_word2vec_feature_writer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG training $W2V_OP $W2V_FEAT
./crfsuite_caller.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT learn $CRF_C2
./crfsuite_caller.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT tag $CRF_C2
./concatenate_labeled_chars_to_word.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT $CRF_C2
./scorer.py $CORPUS $W2V_DIM $W2V_WIN $W2V_NEG $W2V_OP $W2V_FEAT $CRF_C2
