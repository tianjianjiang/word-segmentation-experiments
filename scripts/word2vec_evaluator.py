#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec
import sys
import multiprocessing
from time import sleep


class Word2vecEvaluator:
    def __init__(self, word2vec_model):
        self.model = word2vec_model

    def eval(self, record):
        (queue, tri_char, entries) = record
        freq = entries[0][1]
        entry_map = {e[0]: e[1] for e in entries
                     if '<s>' != e[0] and '</s>' != e[0]}
        if len(entry_map) != 1:
            queue.put(1)
            return freq, 0
        if tri_char.startswith('<s>') or tri_char.endswith('</s>'):
            queue.put(1)
            return freq, 0
        chars = list(tri_char)
        sim_vec = self.model.most_similar_cosmul(
            [chars[0], chars[2]], [chars[1]], topn=1)[0]
        neg01 = self.model.similarity(chars[0], sim_vec[0])
        neg12 = self.model.similarity(chars[2], sim_vec[0])
        if neg01 > neg12:
            neg_char = chars[0]
        elif neg01 < neg12:
            neg_char = chars[2]
        else:
            neg_char = None
        if not neg_char or neg_char not in entry_map:
            queue.put(1)
            return freq, freq
        queue.put(1)
        return freq, 0


if __name__ == '__main__':
    filename = sys.argv[1]
    triCharBoundaryFile = sys.argv[2]
    triCharBoundaryMap = {}
    print('loading...', file=sys.stderr)
    model = Word2Vec.load(filename)
    with open(triCharBoundaryFile) as f:
        for line in f:
            entry = line.strip().split('\t')
            triChar = entry[0]
            boundary = entry[1]
            count = int(entry[2])
            if triChar in triCharBoundaryMap:
                if triCharBoundaryMap[triChar][-1][1] < count:
                    triCharBoundaryMap[triChar] = [(boundary, count)]
                elif triCharBoundaryMap[triChar][-1][1] == count:
                    triCharBoundaryMap[triChar].append((boundary, count))
            else:
                triCharBoundaryMap[triChar] = [(boundary, count)]

    print('threading...', file=sys.stderr)
    tester = Word2vecEvaluator(model)
    pool = multiprocessing.Pool(processes=8)
    manager = multiprocessing.Manager()
    q = manager.Queue()
    penalty = 0
    totalPenalty = 0
    totalCount = len(triCharBoundaryMap)
    items = [(q, item[0], item[1]) for item in triCharBoundaryMap.items()]
    rs = pool.map_async(tester.eval, items, chunksize=100000)
    while not rs.ready():
        completed = q.qsize()
        progress = completed / totalCount
        print('{:>8,}/{:<,}={:.1%}'.format(completed, totalCount, progress),
              end='\r', file=sys.stderr)
        sleep(2)
    for cost, waste in rs.get():
        totalPenalty += cost
        penalty += waste
    print()
    print(penalty, '/', totalPenalty)
