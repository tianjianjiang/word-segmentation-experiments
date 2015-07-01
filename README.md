# Character-embbeding based Word Segmentation

### prerequisite
1. [CRFsuite](http://www.chokkan.org/software/crfsuite/)
2. [gensim.models.word2vec](http://radimrehurek.com/gensim/models/word2vec.html)
3. [The Second International Chinese Word Segmentation Bakeoff's data and the Perl script `score`](http://sighan.cs.uchicago.edu/bakeoff2005/)
  * Just download and extract http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.rar wherever this project folder is.
  * A known issue of `score`: it uses GNU diffutils which isn't always reliable with encoding. Compare *Our Baseline/Topline* with *2005 Baseline/Topline* listed in the paper "[Enhancement of Feature Engineering for Conditional Random Field Learning in Chinese Word Segmentation Using Unlabeled Data][1]" to see how significant the impact is.

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

### control group
* L-BFGS, L2=0.01

##### tag scheme
`B12IES`, i.e. 6-tag set, e.g.:
```
二	B
百	1
四	2
十	I
八	E
人	S
```

##### feature template
Instead of CRF++ style bi-gram feature, using CRFsuite's `feature.possible_states=1` and `feature.possible_transitions=1`.
```
U01:%x[-1,0]
U02:%x[0,0]
U03:%x[1,0]
U10:%x[-1,0]/%x[0,0]
U11:%x[0,0]/%x[1,0]
U20:%x[-1,0]/%x[1,0]
```
For example:
```
B	U01=戀	U02=二	U03=百	U10=戀/二	U11=二/百	U20=戀/百
1	U01=二	U02=百	U03=四	U10=二/百	U11=百/四	U20=二/四
2	U01=百	U02=四	U03=十	U10=百/四	U11=四/十	U20=百/十
I	U01=四	U02=十	U03=八	U10=四/十	U11=十/八	U20=四/八
E	U01=十	U02=八	U03=人	U10=十/八	U11=八/人	U20=十/人
S	U01=八	U02=人	U03=，	U10=八/人	U11=人/，	U20=八/，
```

### experiment design
* *something*: word2vec character-embeddings
* **OP**: cosadd or cosmul
* __~__: negation

##### Configurations:
* `dXwYnZ`: dimension X, window size Y, negative sample size Z
* `mul|add val|name`: cosmul/cosadd value or name (the "most similar" character)

For example, d300w10n5 mul val:
```
B	U01=戀	U02=二	U03=百	U10=戀/二	U11=二/百	U20=戀/百	U910e=1:2.43977	U920e=1:0.767973	U930e=1:1.28929	U940e=1:0.394474
1	U01=二	U02=百	U03=四	U10=二/百	U11=百/四	U20=二/四	U910e=1:2.45768	U920e=1:0.851389	U930e=1:0.837109	U940e=1:0.631251
2	U01=百	U02=四	U03=十	U10=百/四	U11=四/十	U20=百/十	U910e=1:2.29807	U920e=1:0.854744	U930e=1:0.975768	U940e=1:0.572926
I	U01=四	U02=十	U03=八	U10=四/十	U11=十/八	U20=四/八	U910e=1:2.26732	U920e=1:0.870914	U930e=1:0.996255	U940e=1:0.655787
E	U01=十	U02=八	U03=人	U10=十/八	U11=八/人	U20=十/人	U910e=1:2.33113	U920e=1:1.36989	U930e=1:0.73684	U940e=1:0.47046
S	U01=八	U02=人	U03=，	U10=八/人	U11=人/，	U20=八/，	U910e=1:2.50865	U920e=1:0.959077	U930e=1:1.04594	U940e=1:0.356703
```

### result

###### PKU 2005
Configuration    |Recall|Precision|F1
-----------------|-----:|--------:|---:
control          |.928  |.938     |.933
d300w10n5 mul val|.942  |.948     |.945
d300w2n5  mul val|.938  |.948     |.943

###### CityU 2005
Configuration    |Recall|Precision|F1
-----------------|-----:|--------:|---:
control          |.945  |.948     |.946
d300w10n5 mul val|.940  |.945     |.942

###### MSR 2005
Configuration    |Recall|Precision|F1
-----------------|-----:|--------:|---:
control          |.970  |.973     |.972
d300w10n5 mul val|.969  |.974     |.971

###### AS 2005
Config  |Recall|Precision|F1
--------|-----:|--------:|---:
control |.956  |.945     |.951

### todo
* Replace `score` with one respects character encoding<sup>[1]</sup> and supports full confusion matrix<sup>[2]</sup>.
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
