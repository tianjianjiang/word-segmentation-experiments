#!/bin/bash
./word_embedding_template.py pku_training.utf8-char.txt-word2vec_d300w10n5.model ../control/pku_test_gold.utf8.label add name pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec.label
./word_embedding_template.py pku_training.utf8-char.txt-word2vec_d300w10n5.model ../control/pku_training.utf8.label add name pku_training.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec.label
crfsuite learn -m pku_training.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.model -a lbfgs -p c2=0.01 -p feature.possible_states=1 -p feature.possible_transitions=1 pku_training.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec.label
crfsuite tag -m pku_training.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.model pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec.label | paste ../control/pku_test_gold.utf8.label - > pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.prediction
crfsuite tag -r -m pku_training.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.model -qt pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec.label
./conlleval.pl -r -d '\t' < pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.prediction > pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.eval
cat pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.eval
./concatenate_labeled_chars_to_word.py pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.prediction pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.result
./score.pl ../dic/pku_training_words.utf8 ../gold/pku_test_gold.utf8 pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.result > pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.score
tail pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosadd_name_3vec-c100.score
