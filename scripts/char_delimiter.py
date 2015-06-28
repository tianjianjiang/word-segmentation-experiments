#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

root = '../'
corpusFolder = 'icwb2-data/training/'
corpusName = sys.argv[1]
corpusFileName = corpusName + '_training.utf8'
corpusFilePath = root + corpusFolder + corpusFileName
corpusFile = open(corpusFilePath)
charFilePath = root + 'char-delimited_texts/' + corpusFileName + '-char.txt'

print('Converting "%s"' % corpusFilePath)
print('\tto "%s"...' % charFilePath)

charFile = open(charFilePath, 'w')
for line in corpusFile:
    chars = list(line.strip())
    charFile.write(' '.join(c for c in chars if c.strip()) + '\n')

print('\tdone.')
