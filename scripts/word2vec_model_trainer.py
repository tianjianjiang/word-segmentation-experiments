#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys
from gensim.models import word2vec

print('Training word2vec model...')

root = '../'
corpusFolder = 'char-delimited_texts/'
corpusName = sys.argv[1]
corpusFileName = corpusName + '_training.utf8-char.txt'
corpusFilePath = root + corpusFolder + corpusFileName

size = int(sys.argv[2])
window = int(sys.argv[3])
negative = int(sys.argv[4])
suffix = '-word2vec_d%dw%dn%d.model' % (size, window, negative)
modelFilePath = '%sword2vec_models/%s%s' % (root, corpusFileName, suffix)

print('\treading "%s"...' % corpusFilePath)
data = word2vec.LineSentence(corpusFilePath)

print('\ttraining...')
model = word2vec.Word2Vec(sentences=data, size=size, window=window,
                          min_count=0, workers=4, negative=negative)

print('\twriting "%s"...' % modelFilePath)
model.init_sims(replace=True)
model.save(modelFilePath)

print('\tdone.')
