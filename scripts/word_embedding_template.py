#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec
import sys


def formulate(center, left, right):
    formulae = []
    if not right:
        formulae.append(([center], [left]))
        formulae.append(([center, left], []))
    elif not left:
        formulae.append(([center], [right]))
        formulae.append(([center, right], []))
    else:
        formulae.append(([center], [left, right]))
        formulae.append(([center, left], [right]))
        formulae.append(([center, right], [left]))
        formulae.append(([center, left, right], []))
    return formulae


def get_feature(model, center, left, right, n, add_or_mul, name_or_value):
    f = formulate(center, left, right)
    f_index = 0
    for formula in f:
        positives = formula[0]
        negatives = formula[1]
        f_index += 1

        if add_or_mul == 'add':
            try:
                e = model.most_similar(positives, negatives, n)
            except:
                e = None
        else:
            try:
                e = model.most_similar_cosmul(positives, negatives, n)
            except:
                e = None
        if e is not None:
            for j in range(n):
                if name_or_value == 'name':
                    yield 'U9%d%de=%s' % (f_index, j, e[j][0])
                else:
                    yield 'U9%d%de=%s:%g' % (f_index, j, '1', e[j][1])


TOP_N = 1


def output_features(seq, model, add_or_mul, name_or_value):
    for i in range(1, len(seq) - 1):
        fs = [
            'U01=%s' % seq[i - 1][0],
            'U02=%s' % seq[i][0],
            'U03=%s' % seq[i + 1][0],
            'U10=%s/%s' % (seq[i - 1][0], seq[i][0]),
            'U11=%s/%s' % (seq[i][0], seq[i + 1][0]),
            'U20=%s/%s' % (seq[i - 1][0], seq[i + 1][0])
        ]
        left = seq[i - 1][0]
        current = seq[i][0]
        right = seq[i + 1][0]
        fs += list(get_feature(model, current, left, right,
                               TOP_N, add_or_mul, name_or_value))

        yield '%s\t%s\n' % (seq[i][1], '\t'.join(fs))


def encode(x):
    x = x.replace('\\', '\\\\')
    x = x.replace(':', '\\:')
    return x


d = ('', '')
charSeq = [d]
modelFilePath = sys.argv[1]
word2VecModel = Word2Vec.load(modelFilePath)
trainingFilePath = sys.argv[2]
trainingFile = open(trainingFilePath, 'r')
addOrMul = sys.argv[3]
nameOrValue = sys.argv[4]
labelFilePath = sys.argv[5]
labelFile = open(labelFilePath, 'w')
for line in trainingFile:
    line = line.strip()
    if not line:
        charSeq.append(d)
        labels = output_features(charSeq, word2VecModel, addOrMul, nameOrValue)
        labelFile.write(''.join(labels) + '\n')
        charSeq = [d]
    else:
        fields = line.split('\t')
        charSeq.append((encode(fields[0]), encode(fields[1])))
labelFile.close()
trainingFile.close()
