#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

corpusFilePath = sys.argv[1]
corpusFile = open(corpusFilePath)
charFilePath = sys.argv[2]
charFile = open(charFilePath, 'w')
for line in corpusFile:
    chars = list(line.strip())
    charFile.write(' '.join(c for c in chars if c.strip()) + '\n')

