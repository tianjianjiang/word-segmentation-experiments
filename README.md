# Character-embbeding based Word Segmentation

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
  * __~__*something*(A) **OP** *something*(B) **OP** *something*(C)
  * *something*(A) **OP** *something*(B) **OP** __~__*something*(C)
  * __~__*something*(A) **OP** *something*(B) **OP** __~__*something*(C)

### experiment design
* *something*: word2vec character-embeddings
* **OP**: cosadd or cosmul

### todo
* Tensor-based embeddings
* Define __~__
* Better negative-sampling

### references
* [Tensor Network and Natural Language](https://hackpad.com/Tensor-Network-and-Natural-Language-zkA5N1DcnYT)
* [Evaluation via Negativa of Chinese Word Segmentation for Information Retrieval](https://www.researchgate.net/publication/264742378_Evaluation_via_Negativa_of_Chinese_Word_Segmentation_for_Information_Retrieval)
