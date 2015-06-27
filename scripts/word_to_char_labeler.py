#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

corpusFilePath = sys.argv[1]
corpusFile = open(corpusFilePath)
labelFilePath = sys.argv[2]
labelFile = open(labelFilePath, 'w')
for line in corpusFile:
    words = line.split()
    for word in words:
        chars = list(word)
        wordLength = len(chars)
        labels = []
        for i in range(wordLength):
            if 0 == i:
                if 1 == wordLength:
                    label = 'S'
                else:
                    label = 'B'
            elif wordLength - 1 == i:
                label = 'E'
            elif i < 3:
                label = str(i)
            else:
                label = 'I'
            labels.append(label)
        labelFile.write('\n'.join(c + '\t' + l for c, l in zip(chars, labels))
                        + '\n')
    labelFile.write('\n')
