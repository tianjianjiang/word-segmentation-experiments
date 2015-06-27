#!/bin/bash
./word_to_char_labeler.py ../icwb2-data/training/pku_training.utf8 ../control/pku_training.utf8.label
./word_to_char_labeler.py ../icwb2-data/gold/pku_test_gold.utf8 ../control/pku_test_gold.utf8.label
./char_delimiter.py ../icwb2-data/training/pku_training.utf8 ../char-delimited_texts/pku_training.utf8-char.txt
./word2vec_model_trainer.py ../char-delimited_texts/pku_training.utf8-char.txt 300 10 5 ../word2vec_models/pku_training.utf8-char.txt-word2vec_d300w10n5.model
./crfsuite_word2vec_feature_writer.py ../word2vec_models/pku_training.utf8-char.txt-word2vec_d300w10n5.model ../control/pku_test_gold.utf8.label mul value ../exp/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec.label
./crfsuite_word2vec_feature_writer.py ../word2vec_models/pku_training.utf8-char.txt-word2vec_d300w10n5.model ../control/pku_training.utf8.label mul value ../exp/pku_training.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec.label
crfsuite learn -m ../crfsuite_models/pku_training.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.model -a lbfgs -p c2=0.01 -p feature.possible_states=1 -p feature.possible_transitions=1 ../exp/pku_training.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec.label
crfsuite tag -m ../crfsuite_models/pku_training.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.model ../exp/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec.label | paste ../control/pku_test_gold.utf8.label - > ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.prediction
./concatenate_labeled_chars_to_word.py ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.prediction ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.result
../icwb2-data/scripts/score ../icwb2-data/gold/pku_training_words.utf8 ../icwb2-data/gold/pku_test_gold.utf8 ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.result > ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.score
tail ../result/pku_test_gold.utf8.crfsuite-embedding_d300w10n5_cosmul_value_3vec-c100.score
