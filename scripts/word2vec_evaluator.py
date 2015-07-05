#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec
import sys

filename = sys.argv[1]
triCharBoundariesFile = sys.argv[2]
triCharBoundariesMap = {}
model = Word2Vec.load(filename)
with open(triCharBoundariesFile) as f:
    for line in f:
        entry = line.strip().split('\t')
        triChar = entry[0]
        boundary = entry[1]
        count = int(entry[2])
        if triChar in triCharBoundariesMap:
            if triCharBoundariesMap[triChar][-1][1] < count:
                triCharBoundariesMap[triChar] = [(boundary, count)]
            elif triCharBoundariesMap[triChar][-1][1] == count:
                triCharBoundariesMap[triChar].append((boundary, count))
        else:
            triCharBoundariesMap[triChar] = [(boundary, count)]
penalty = 0
totalPenalty = 0
for triChar, entries in triCharBoundariesMap.items():
    entryMap = {entry[0]: entry[1] for entry in entries
                if '<s>' != entry[0] and '</s>' != entry[0]}
    if len(entryMap) == 0:
        continue
    least = model.doesnt_match(list(triChar))
    cost = entries[0][1]
    totalPenalty += cost
    if least not in entryMap:
        penalty += cost
print(penalty, '/', totalPenalty)
