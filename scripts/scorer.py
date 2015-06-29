#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys
from subprocess import call, check_output

print('Scoring...')

root = '../'
icwb2Folder = root + 'icwb2-data/'
scorerPath = '%sscripts/score' % icwb2Folder
corpusName = sys.argv[1]
group = sys.argv[2]
c2 = sys.argv[3]

if 'as' == corpusName:
    inputCharSrc = corpusName + '_testing_gold.utf8'
else:
    inputCharSrc = corpusName + '_test_gold.utf8'

if 'w2v' == group:
    size = int(sys.argv[4])
    window = int(sys.argv[5])
    negative = int(sys.argv[6])
    addOrMul = sys.argv[7]
    nameOrVal = sys.argv[8]
    word2VecSrc = corpusName + '_training.utf8-char.txt'
    inputSrc = inputCharSrc + '-' + word2VecSrc
    inputSrc = '%s-word2vec_d%dw%dn%d' % (inputSrc, size, window, negative)
    inputAffix = '%s-cos%s_%s_3vec-crfsuite' % (inputSrc, addOrMul, nameOrVal)
else:
    inputAffix = inputCharSrc + '-crfsuite'
rebuiltFilePath = '%sresult/%s-c%s-label-word.txt' % (root, inputAffix, c2)
dicFilePath = '%sgold/%s_training_words.utf8' % (icwb2Folder, corpusName)
goldFilePath = '%sgold/%s' % (icwb2Folder, inputCharSrc)
scoreFilePath = '%sresult/%s-c%s-label-word-score.txt' % (root, inputAffix, c2)
args = [scorerPath, dicFilePath, goldFilePath, rebuiltFilePath]
scoreOutput = check_output(args)
with open(scoreFilePath, 'wb') as f:
    f.write(scoreOutput)

args = ['tail', '-n', '7', scoreFilePath]
call(args)
