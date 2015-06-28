#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys

root = '../'

corpusName = sys.argv[1]
size = int(sys.argv[2])
window = int(sys.argv[3])
negative = int(sys.argv[4])
addOrMul = sys.argv[5]
nameOrValue = sys.argv[6]
c2 = sys.argv[7]

word2VecSrc = corpusName + '_training.utf8-char.txt'
if 'as' == corpusName:
    inputCharSrc = corpusName + '_testing_gold.utf8'
else:
    inputCharSrc = corpusName + '_test_gold.utf8'
inputSrc = inputCharSrc + '-' + word2VecSrc
inputPrefix = '%s-word2vec_d%dw%dn%d' % (inputSrc, size, window, negative)
inputAffix = '%s-cos%s_%s_3vec-crfsuite' % (inputPrefix, addOrMul, nameOrValue)
labelFilePath = '%sresult/%s-c%s-label.txt' % (root, inputAffix, c2)
rebuiltFilePath = '%sresult/%s-c%s-label-word.txt' % (root, inputAffix, c2)

print('Converting "%s"' % labelFilePath)
print('\tto "%s"...' % rebuiltFilePath)

labelFile = open(labelFilePath)
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

print('\tdone.')
