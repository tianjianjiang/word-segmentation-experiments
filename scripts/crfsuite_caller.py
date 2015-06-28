#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys
from subprocess import call, check_output

root = '../'

corpusName = sys.argv[1]
group = sys.argv[2]
c2 = sys.argv[3]
mode = sys.argv[4]

if 'learn' == mode:
    inputCharSrc = corpusName + '_training.utf8'
else:
    if 'as' == corpusName:
        inputCharSrc = corpusName + '_testing_gold.utf8'
    else:
        inputCharSrc = corpusName + '_test_gold.utf8'

charSrc = corpusName + '_training.utf8'
if 'w2v' == group:
    size = int(sys.argv[5])
    window = int(sys.argv[6])
    negative = int(sys.argv[7])
    addOrMul = sys.argv[8]
    nameOrVal = sys.argv[9]
    word2VecSrc = corpusName + '_training.utf8-char.txt'
    modelSrc = charSrc + '-' + word2VecSrc
    modelSrc = '%s-word2vec_d%dw%dn%d' % (modelSrc, size, window, negative)
    modelAffix = '%s-cos%s_%s_3vec-crfsuite' % (modelSrc, addOrMul, nameOrVal)
    modelAffix += '-c' + c2

    inputSrc = inputCharSrc + '-' + word2VecSrc
    inputSrc = '%s-word2vec_d%dw%dn%d' % (inputSrc, size, window, negative)
    inputAffix = '%s-cos%s_%s_3vec-crfsuite' % (inputSrc, addOrMul, nameOrVal)
    inputFileFolder = root + 'exp/'
else:
    modelAffix = charSrc + '-crfsuite-c' + c2
    inputAffix = inputCharSrc + '-crfsuite'
    inputFileFolder = root + 'control/'
modelFilePath = '%scrfsuite_models/%s.model' % (root, modelAffix)
inputFilePath = '%s%s-label.txt' % (inputFileFolder, inputAffix)

commands = []
args = ['crfsuite', mode, '-m', modelFilePath]
if 'learn' == mode:
    args += ['-a', 'lbfgs', '-p', 'c2=%f' % (1 / int(c2))]
    args += ['-p', 'feature.possible_states=1']
    args += ['-p', 'feature.possible_transitions=1']
    args += [inputFilePath]
    call(args)
else:
    args += [inputFilePath]
    tagFilePath = '%sresult/%s-c%s-tag.txt' % (root, inputAffix, c2)
    tags = check_output(args, universal_newlines=True)
    with open(tagFilePath, 'w') as f:
        f.write(tags)

    controlFilePath = '%scontrol/%s-label.txt' % (root, inputCharSrc)
    labelFilePath = '%sresult/%s-c%s-label.txt' % (root, inputAffix, c2)
    controlFile = open(controlFilePath)
    tagFile = open(tagFilePath)
    labelFile = open(labelFilePath, 'w')
    for controlLine, tagLine in zip(controlFile, tagFile):
        labelFile.write(controlLine.strip() + '\t' + tagLine)
