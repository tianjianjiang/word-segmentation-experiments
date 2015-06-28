#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'


def output_features(seq):
    for i in range(1, len(seq) - 1):
        fs = [
            'U01=%s' % seq[i - 1][0],
            'U02=%s' % seq[i][0],
            'U03=%s' % seq[i + 1][0],
            'U10=%s/%s' % (seq[i - 1][0], seq[i][0]),
            'U11=%s/%s' % (seq[i][0], seq[i + 1][0]),
            'U20=%s/%s' % (seq[i - 1][0], seq[i + 1][0])
        ]

        yield '%s\t%s\n' % (seq[i][1], '\t'.join(fs))


def encode(x):
    x = x.replace('\\', '\\\\')
    x = x.replace(':', '\\:')
    return x


if __name__ == '__main__':
    import sys

    root = '../'
    corpusName = sys.argv[1]
    corpusType = sys.argv[2]
    if 'training' == corpusType:
        labelFilePrefix = corpusName + '_training.utf8'
    else:
        if 'as' == corpusName:
            labelFilePrefix = corpusName + '_testing_gold.utf8'
        else:
            labelFilePrefix = corpusName + '_test_gold.utf8'
    labelFilePath = '%scontrol/%s-label.txt' % (root, labelFilePrefix)
    featureSrc = labelFilePrefix
    featureFilePath = '%scontrol/%s-crfsuite-label.txt' % (root, featureSrc)

    print('Converting %s' % labelFilePath)
    print('\tto "%s"...' % featureFilePath)

    labelFile = open(labelFilePath, 'r')
    featureFile = open(featureFilePath, 'w')

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
            labels = output_features(charSeq)
            featureFile.write(''.join(labels) + '\n')
            charSeq = [d]
            print('\t' + '{:.1%}'.format(byteCount/fileStat.st_size), end='\r')
        else:
            fields = line.split('\t')
            charSeq.append((encode(fields[0]), encode(fields[1])))

    print('\n\tdone.')
