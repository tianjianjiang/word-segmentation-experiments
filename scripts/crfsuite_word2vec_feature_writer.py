#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec


class CrfsuiteWord2VecFeatureWriter:
    def __init__(self, model, n, add_or_mul, name_or_value):
        self.model = model
        self.top_n = n
        self.add_or_mul = add_or_mul
        self.name_or_value = name_or_value

    @staticmethod
    def formulate(center, left, right):
        if not right:
            formulae = [([center], [left]), ([center, left], [])]
        elif not left:
            formulae = [([center], [right]), ([center, right], [])]
        else:
            formulae = [([center], [left, right]), ([center, left], [right]),
                        ([center, right], [left]), ([center, left, right], [])]
        return formulae

    def get_feature(self, center, left, right):
        f = CrfsuiteWord2VecFeatureWriter.formulate(center, left, right)
        f_index = 0
        for formula in f:
            positives = formula[0]
            negatives = formula[1]
            f_index += 1
            if self.add_or_mul == 'add':
                try:
                    e = self.model.most_similar(
                        positives, negatives, self.top_n)
                except KeyError:
                    e = None
            else:
                try:
                    e = self.model.most_similar_cosmul(
                        positives, negatives, self.top_n)
                except KeyError:
                    e = None
            if e is not None:
                for j in range(self.top_n):
                    if self.name_or_value == 'name':
                        yield 'U9%d%de=%s' % (f_index, j, e[j][0])
                    else:
                        yield 'U9%d%de=%s:%g' % (f_index, j, '1', e[j][1])

    def output_features(self, seq):
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
            fs += list(self.get_feature(current, left, right))

            yield '%s\t%s\n' % (seq[i][1], '\t'.join(fs))


def encode(x):
    x = x.replace('\\', '\\\\')
    x = x.replace(':', '\\:')
    return x


if __name__ == '__main__':
    import sys

    topN = 1
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
    featureWriter = CrfsuiteWord2VecFeatureWriter(word2VecModel, topN,
                                                  addOrMul, nameOrValue)
    for line in trainingFile:
        line = line.strip()
        if not line:
            charSeq.append(d)
            labels = featureWriter.output_features(charSeq)
            labelFile.write(''.join(labels) + '\n')
            charSeq = [d]
        else:
            fields = line.split('\t')
            charSeq.append((encode(fields[0]), encode(fields[1])))
    labelFile.close()
    trainingFile.close()
