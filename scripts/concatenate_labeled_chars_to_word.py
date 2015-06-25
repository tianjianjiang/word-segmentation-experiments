#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

labelFilePath = sys.argv[1]
labelFile = open(labelFilePath)
rebuiltFilePath = sys.argv[2]
rebuiltFile = open(rebuiltFilePath, 'w')
charStack = list()
wordStack = list()
for line in labelFile:
    pair = line.split()
    if len(pair) > 1:
        if pair[-1].startswith('E') or pair[-1].startswith('S')\
                or pair[-1].startswith('P'):
            charStack.append(pair[0])
            wordStack.append(''.join(charStack))
            charStack = list()
        else:
            charStack.append(pair[0])
    else:
        if len(wordStack) > 0:
            rebuiltFile.write(' '.join(wordStack))
        wordStack = list()
        rebuiltFile.write('\n')
