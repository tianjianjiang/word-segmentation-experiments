#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys
from gensim.models import word2vec

filename = sys.argv[1]
size = int(sys.argv[2])
window = int(sys.argv[3])
negative = int(sys.argv[4])
output = sys.argv[5]

print('reading char-delimited texts...')
data = word2vec.LineSentence(filename)
print('done.')
print('training...')
model = word2vec.Word2Vec(sentences=data, size=size, window=window, min_count=1, workers=4,
                          negative=negative)
print('done.')
print('saving model...')
model.save(output)
print('done.')
