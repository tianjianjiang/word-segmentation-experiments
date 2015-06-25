# Character-embbeding based Word Segmentation

### prerequisite
1. [CRFsuite](http://www.chokkan.org/software/crfsuite/)
2. [gensim.models.word2vec](http://radimrehurek.com/gensim/models/word2vec.html)
3. [The Second International Chinese Word Segmentation Bakeoff's data and score.pl](http://sighan.cs.uchicago.edu/bakeoff2005/)
4. [conlleval.pl](http://www.cnts.ua.ac.be/conll2000/chunking/conlleval.txt)

### hypothesis
Characters of a word have *something* in common.  
(Or: before someone measure it, every character was in superposition state)

### feature design
For example:
* Given a three-character string ABC
* B's features are
  * *something*(B) **OP** *something*(A)&nbsp;&nbsp;&nbsp;**OP** *something*(C)
  * *something*(B) **OP** __~__*something*(A)&nbsp;**OP** *something*(C)
  * *something*(B) **OP** *something*(A)&nbsp;&nbsp;&nbsp;**OP** __~__*something*(C)
  * *something*(B) **OP** __~__*something*(A)&nbsp;**OP** __~__*something*(C)

### experiment design
* *something*: word2vec character-embeddings
* **OP**: cosadd or cosmul
* __~__: negation

### todo
* Tensor-based embeddings
  * Better negative-sampling 
* Better __~__
* Induce morphosyntactical category of characters
 
### references
* [Tensor Network and Natural Language](https://hackpad.com/Tensor-Network-and-Natural-Language-zkA5N1DcnYT)
* [Evaluation via Negativa of Chinese Word Segmentation for Information Retrieval](https://www.researchgate.net/publication/264742378_Evaluation_via_Negativa_of_Chinese_Word_Segmentation_for_Information_Retrieval)
