# Character-embbeding based Word Segmentation Experiments

### prerequisite
1. [CRFsuite](http://www.chokkan.org/software/crfsuite/)
2. [gensim.models.word2vec](http://radimrehurek.com/gensim/models/word2vec.html)
3. [The Second International Chinese Word Segmentation Bakeoff's data and score.pl](http://sighan.cs.uchicago.edu/bakeoff2005/)
4. [conlleval.pl](http://www.cnts.ua.ac.be/conll2000/chunking/conlleval.txt)

### hypothesis
Characters of a word have *something* in common

### feature design
* Given a three-character string ABC
* B's features are
  * *something*(A) **OP** *something*(B) **OP** *something*(C)
  * ~*something*(A) **OP** *something*(B) **OP** *something*(C)
  * *something*(A) **OP** *something*(B) **OP** ~*something*(C)
  * ~*something*(A) **OP** *something*(B) **OP** ~*something*(C)

### experiment
* *something*: word2vec character-embedding (vector)
* **OP**: cosadd or cosmul
