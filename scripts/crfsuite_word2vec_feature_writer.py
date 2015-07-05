#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec


class CrfsuiteWord2VecFeatureWriter:
    def __init__(self, model, n, add_or_mul, name_or_value):
        self.model = model
        self.top_n = n
        self.add_or_mul = add_or_mul
        self.name_or_value = name_or_value
        self.feature_cache = {}

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

    def get_most_similar(self, positives, negatives):
        try:
            if 'add' == self.add_or_mul:
                e = self.model.most_similar(
                    positives, negatives, self.top_n)
            else:
                e = self.model.most_similar_cosmul(
                    positives, negatives, self.top_n)
        except KeyError:
            e = None
        return e

    def get_feature(self, center, left, right):
        f = CrfsuiteWord2VecFeatureWriter.formulate(center, left, right)
        f_index = 0
        for formula in f:
            positives = formula[0]
            negatives = formula[1]
            f_index += 1
            cache_key = ''.join(positives) + '~' + ''.join(negatives)
            if cache_key not in self.feature_cache:
                e = self.get_most_similar(positives, negatives)
                self.feature_cache[cache_key] = e
            else:
                e = self.feature_cache[cache_key]
            if e is not None:
                for j in range(self.top_n):
                    if 'name' == self.name_or_value:
                        yield 'U9%d%de=%s' % (f_index, j, e[j][0])
                    else:
                        yield 'U9%d%de=%s:%g' % (f_index, j, '1', e[j][1])

    def get_least_match_feature(self, center, left, right):
        if '' == left:
            e = '<s>'
        elif '' == right:
            e = '</s>'
        else:
            check_list = [left, center, right]
            cache_key = ''.join(check_list)
            if cache_key not in self.feature_cache:
                try:
                    e = self.model.doesnt_match(check_list)
                except ValueError:
                    e = 'UNK'
                self.feature_cache[cache_key] = e
            else:
                e = self.feature_cache[cache_key]
        yield 'U9e=' + e

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
            if 'least' == self.add_or_mul:
                fs += list(self.get_least_match_feature(current, left, right))
            else:
                fs += list(self.get_feature(current, left, right))

            yield '%s\t%s\n' % (seq[i][1], '\t'.join(fs))


def encode(x):
    x = x.replace('\\', '\\\\')
    x = x.replace(':', '\\:')
    return x


if __name__ == '__main__':
    import sys

    root = '../'
    corpusName = sys.argv[1]
    size = int(sys.argv[2])
    window = int(sys.argv[3])
    negative = int(sys.argv[4])
    modelSrc = corpusName + '_training.utf8-char.txt'
    modelAffix = '%s-word2vec_d%dw%dn%d' % (modelSrc, size, window, negative)
    modelFilePath = '%sword2vec_models/%s.model' % (root, modelAffix)

    corpusType = sys.argv[5]
    if 'training' == corpusType:
        labelFilePrefix = corpusName + '_training.utf8'
    else:
        if 'as' == corpusName:
            labelFilePrefix = corpusName + '_testing_gold.utf8'
        else:
            labelFilePrefix = corpusName + '_test_gold.utf8'
    labelFilePath = '%scontrol/%s-label.txt' % (root, labelFilePrefix)

    addOrMul = sys.argv[6]
    nameOrValue = sys.argv[7]
    featureSrc = labelFilePrefix + '-' + modelAffix
    featureAffix = '%s-cos%s_%s_3vec' % (featureSrc, addOrMul, nameOrValue)
    featureFilePath = '%sexp/%s-crfsuite-label.txt' % (root, featureAffix)

    print('Converting %s' % labelFilePath)
    print('\tto "%s"...' % featureFilePath)

    word2VecModel = Word2Vec.load(modelFilePath)
    labelFile = open(labelFilePath, 'r')
    featureFile = open(featureFilePath, 'w')

    topN = 1
    featureWriter = CrfsuiteWord2VecFeatureWriter(word2VecModel, topN,
                                                  addOrMul, nameOrValue)

    import os
    fileStat = os.stat(labelFilePath)
    byteCount = 0

    d = ('', '')
    charSeq = [d]
    for line in labelFile:
        byteCount += len(line.encode('utf-8'))
        line = line.strip()
        if not line:
            charSeq.append(d)
            labels = featureWriter.output_features(charSeq)
            featureFile.write(''.join(labels) + '\n')
            charSeq = [d]
            print('\t' + '{:.1%}'.format(byteCount/fileStat.st_size), end='\r')
        else:
            fields = line.split('\t')
            charSeq.append((encode(fields[0]), encode(fields[1])))

    print('\n\tdone.')
