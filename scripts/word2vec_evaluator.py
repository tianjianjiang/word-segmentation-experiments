#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from gensim.models import Word2Vec
import sys
import multiprocessing


class Word2vecEvaluator:
    def __init__(self, word2vec_model, total_checks):
        self.model = word2vec_model
        self.total_checks = total_checks

    def eval(self, record):
        checked_id = record[0]
        tri_char = record[1]
        entries = record[2]
        print('{:>8} of {: <20}'.format(checked_id, self.total_checks),
              end='\r', file=sys.stderr)
        freq = entries[0][1]
        entry_map = {e[0]: e[1] for e in entries
                     if '<s>' != e[0] and '</s>' != e[0]}
        if len(entry_map) != 1:
            return freq, 0
        if tri_char.startswith('<s>') or tri_char.endswith('</s>'):
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
            return freq, freq
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
    pool = multiprocessing.Pool(processes=2)
    tester = Word2vecEvaluator(model, len(triCharBoundaryMap))
    penalty = 0
    totalPenalty = 0
    items = [(i, item[0], item[1])
             for i, item in enumerate(triCharBoundaryMap.items())]
    for cost, waste in pool.imap_unordered(tester.eval, items, chunksize=100000):
        totalPenalty += cost
        penalty += waste

    print()
    print(penalty, '/', totalPenalty)
