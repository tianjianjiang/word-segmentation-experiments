#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

root = '../'
corpusFolder = 'icwb2-data/'
corpusName = sys.argv[1]
corpusType = sys.argv[2]
if 'training' == corpusType:
    corpusFileNameSuffix = '_training.utf8'
else:
    if 'as' == corpusName:
        corpusFileNameSuffix = '_testing_gold.utf8'
    else:
        corpusFileNameSuffix = '_test_gold.utf8'
corpusFileName = corpusName + corpusFileNameSuffix
corpusFilePath = root + corpusFolder + corpusType + '/' + corpusFileName
labelFilePath = root + 'control/' + corpusFileName + '-label.txt'

print('Converting "%s"' % corpusFilePath)
print('\tto "%s"...' % labelFilePath)

corpusFile = open(corpusFilePath)
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

print('\tdone.')
