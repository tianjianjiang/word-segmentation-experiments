#! /usr/bin/env python3.4

__author__ = 'Mike Tian-Jian Jiang'

from collections import namedtuple
from collections import defaultdict


CharOfWord = namedtuple('CharOfWord',
                        ['char_text', 'char_pos_in_word',
                         'word_text', 'word_pos'])


class BoundarySeeker:
    def __init__(self):
        self.trichar_boundaries = defaultdict(lambda: defaultdict(int))

    @staticmethod
    def get_words(line):
        return [w for w in line.strip().split() if '' != w.strip()]

    @staticmethod
    def get_chars_of_words(words):
        chars_of_words = []
        for word_pos, word_text in enumerate(words):
            char_list = list(word_text)
            for char_pos, char_text in enumerate(char_list):
                chars_of_words.append(CharOfWord._make(
                    [char_text, char_pos, word_text, word_pos]))
        return chars_of_words

    def get_boundaries_of_trichars(self, chars_of_words):
        char_count = len(chars_of_words)
        for i in range(char_count):
            if i > 0:
                left = chars_of_words[i - 1]
            else:
                left = CharOfWord._make(['<s>', 0, '<s>', -1])
            if i < char_count - 1:
                right = chars_of_words[i + 1]
            else:
                right = CharOfWord._make(['</s>', 0, '</s>', char_count])
            center = chars_of_words[i]
            trichar_text = left.char_text + center.char_text + right.char_text
            is_left = False
            is_right = False
            if left.word_pos != center.word_pos:
                self.trichar_boundaries[trichar_text][left.char_text] += 1
                is_left = True
            if right.word_pos != center.word_pos:
                self.trichar_boundaries[trichar_text][right.char_text] += 1
                is_right = True
            if is_left and is_right:
                self.trichar_boundaries[trichar_text][center.char_text] += 1

if __name__ == '__main__':
    import sys

    root = '../'
    corpusFolder = 'icwb2-data/training/'
    corpusName = sys.argv[1]
    corpusFileName = corpusName + '_training.utf8'
    corpusFilePath = root + corpusFolder + corpusFileName
    corpusFile = open(corpusFilePath)
    boundariesFilePath = root + 'boundaries/' + corpusFileName + '-3char.txt'

    print('Converting "%s"' % corpusFilePath)
    print('\tto "%s"...' % boundariesFilePath)

    reader = BoundarySeeker()
    for l in corpusFile:
        reader.get_boundaries_of_trichars(
            BoundarySeeker.get_chars_of_words(
                BoundarySeeker.get_words(l)))

    charFile = open(boundariesFilePath, 'w')
    for triChar in sorted(reader.trichar_boundaries.keys()):
        boundaries = reader.trichar_boundaries[triChar]
        for char in sorted(boundaries, key=boundaries.get):
            count = boundaries[char]
            charFile.write('{}\t{}\t{}\n'.format(triChar, char, count))

    print('\tdone.')
