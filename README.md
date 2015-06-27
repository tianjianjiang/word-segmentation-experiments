# Character-embbeding based Word Segmentation

### prerequisite
1. [CRFsuite](http://www.chokkan.org/software/crfsuite/)
2. [gensim.models.word2vec](http://radimrehurek.com/gensim/models/word2vec.html)
3. [The Second International Chinese Word Segmentation Bakeoff's data and score.pl](http://sighan.cs.uchicago.edu/bakeoff2005/)
  * A known issue of `score.pl`: it uses GNU diffutils which isn't always reliable with encoding. Compare *Our Baseline/Topline* with *2005 Baseline/Topline* listed in the paper "[Enhancement of Feature Engineering for Conditional Random Field Learning in Chinese Word Segmentation Using Unlabeled Data][1]" to see how significant the impact is.
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
* Replace `score.pl` with one respects character encoding<sup>[1]</sup> and supports full confusion matrix<sup>[2]</sup>.
* Tensor-based embeddings<sup>[3]</sup>
  * Better negative-sampling<sup>[2]</sup>
* Better __~__
* Induce morphosyntactical category of characters
 
### references
1. [Enhancement of Feature Engineering for Conditional Random Field Learning in Chinese Word Segmentation Using Unlabeled Data][1]
2. [Evaluation via Negativa of Chinese Word Segmentation for Information Retrieval][2]
3. [Tensor Network and Natural Language][3]

[1]: https://www.researchgate.net/publication/264742309_Enhancement_of_Feature_Engineering_for_Conditional_Random_Field_Learning_in_Chinese_Word_Segmentation_Using_Unlabeled_Data
[2]: https://www.researchgate.net/publication/264742378_Evaluation_via_Negativa_of_Chinese_Word_Segmentation_for_Information_Retrieval
[3]: https://hackpad.com/Tensor-Network-and-Natural-Language-zkA5N1DcnYT
