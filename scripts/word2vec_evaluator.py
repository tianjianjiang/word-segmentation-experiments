#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec
import sys

filename = sys.argv[1]
model = Word2Vec.load(filename)


def s(p, n, c=5, m=model):
    print('+'.join(p) + '-' + '-'.join(n))
    cnt = 1
    result = m.most_similar_cosmul(positive=p, negative=n, topn=c)
    print('3cosmul')
    for r in result:
        print(cnt, r[0], r[1])
        cnt += 1
    cnt = 1
    result = m.most_similar(positive=p, negative=n, topn=c)
    print('3cosadd')
    for r in result:
        print(cnt, r[0], r[1])
        cnt += 1

positives = sys.argv[2]
negatives = sys.argv[3]

s(list(positives), list(negatives), int(sys.argv[4]))
