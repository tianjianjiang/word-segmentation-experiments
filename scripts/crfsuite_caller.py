#!/usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

import sys
from subprocess import call

root = '../'

corpusName = sys.argv[1]
size = int(sys.argv[2])
window = int(sys.argv[3])
negative = int(sys.argv[4])
addOrMul = sys.argv[5]
nameOrValue = sys.argv[6]
mode = sys.argv[7]
c2 = sys.argv[8]

charSrc = corpusName + '_training.utf8'
word2VecSrc = corpusName + '_training.utf8-char.txt'
modelSrc = charSrc + '-' + word2VecSrc
modelPrefix = '%s-word2vec_d%dw%dn%d' % (modelSrc, size, window, negative)
modelAffix = '%s-cos%s_%s_3vec-crfsuite' % (modelPrefix, addOrMul, nameOrValue)
modelFilePath = '%scrfsuite_models/%s-c%s.model' % (root, modelAffix, c2)

if 'learn' == mode:
    inputCharSrc = corpusName + '_training.utf8'
else:
    if 'as' == corpusName:
        inputCharSrc = corpusName + '_testing_gold.utf8'
    else:
        inputCharSrc = corpusName + '_test_gold.utf8'
inputSrc = inputCharSrc + '-' + word2VecSrc
inputPrefix = '%s-word2vec_d%dw%dn%d' % (inputSrc, size, window, negative)
inputAffix = '%s-cos%s_%s_3vec-crfsuite' % (inputPrefix, addOrMul, nameOrValue)
inputFilePath = '%sexp/%s-label.txt' % (root, inputAffix)

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
    tagFilePath = '%sresult/%s-crfsuite-tag.txt' % (root, inputAffix)
    args += ['>', tagFilePath]
    call(args)

    controlFilePath = '%scontrol/%s-label.txt' % (root, inputCharSrc)
    labelFilePath = '%sresult/%s-c%s-label.txt' % (root, inputAffix, c2)
    args = ['paste', controlFilePath, tagFilePath, '>', labelFilePath]
    call(args)
