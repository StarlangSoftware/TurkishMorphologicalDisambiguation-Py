# Morphological Disambiguation

## Task Definition

Morphological disambiguation is the problem of selecting accurate morphological parse of a word given its possible parses. These parses are generated by a morphological analyzer. In morphologically rich languages like Turkish, the number of possible parses for a given word is generally more than one. Each parse is considered as a different interpretation of a single word. Each interpretation consists of a root word and sequence of inflectional and derivational suffixes. The following table illustrates different interpretations of the word ‘‘üzerine’’.

üzer+Noun+A3sg+P3sg+Dat  
üzer+Noun+A3sg+P2sg+Dat  
üz+Verb+Pos+Aor+^DB+Adj+Zero+^DB+Noun+Zero+A3sg+P3sg+Dat  
üz+Verb+Pos+Aor+^DB+Adj+Zero+^DB+Noun+Zero+A3sg+P2sg+Dat

As seen above, the first two parses share the same root but different suffix sequences. Similarly, the last two parses also share the same root, however sequence of morphemes are different. Given a parse such as

üz+Verb+Pos+Aor+^DB+Adj+Zero+^DB+Noun+Zero+A3sg+P3sg+Dat

each item is separated by ‘‘+’’ is a morphological feature such as Pos or Aor. Inflectional groups are identified as sequence of morphological features separated by derivational boundaries ^DB. The sequence of inflectional groups forms the term tag. Root word plus tag is named as word form.  So, a word form is defined as follows:

IGroot+IG<sub>1</sub>+^DB+IG<sub>2</sub>+^DB+...+^DB+IG<sub>n</sub>

Then the morphological disambiguation problem can be defined as follows: For a given sentence represented by a sequence of words W = w<sub>1</sub><sup>n</sup> = w<sub>1</sub>, w<sub>2</sub>, ..., w<sub>n</sub>, determine the sequence of parses T = t<sub>1</sub><sup>n</sup> = t<sub>1</sub>, t<sub>2</sub>, ..., t<sub>n</sub>; where t<sub>i</sub> represents the correct parse of the word w<sub>i</sub>.

## Data Annotation

### Preparation

1. Collect a set of sentences to annotate. 
2. Each sentence in the collection must be named as xxxx.yyyyy in increasing order. For example, the first sentence to be annotated will be 0001.train, the second 0002.train, etc.
3. Put the sentences in the same folder such as *Turkish-Phrase*.
4. Build the [Java](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation) project and put the generated sentence-morphological-analyzer.jar file into another folder such as *Program*.
5. Put *Turkish-Phrase* and *Program* folders into a parent folder.

### Annotation

1. Open sentence-morphological-analyzer.jar file.
2. Wait until the data load message is displayed.
3. Click Open button in the Project menu.
4. Choose a file for annotation from the folder *Turkish-Phrase*.  
5. For each word in the sentence, click the word, and choose correct morphological analysis for that word.
6. Click one of the next buttons to go to other files.

## Classification DataSet Generation

After annotating sentences, you can use [DataGenerator](https://github.com/starlangsoftware/DataGenerator-Py) package to generate classification dataset for the Morphological Disambiguation task.

## Generation of ML Models

After generating the classification dataset as above, one can use the [Classification](https://github.com/starlangsoftware/Classification-Py) package to generate machine learning models for the Morphological Disambiguation task.

Video Lectures
============

[<img src=https://github.com/StarlangSoftware/TurkishMorphologicalDisambiguation/blob/master/video1.jpg width="50%">](https://youtu.be/vhp6Mse1vdM)[<img src=https://github.com/StarlangSoftware/TurkishMorphologicalDisambiguation/blob/master/video2.jpg width="50%">](https://youtu.be/lkFhIKdDSvw)[<img src=https://github.com/StarlangSoftware/TurkishMorphologicalDisambiguation/blob/master/video3.jpg width="50%">](https://youtu.be/ajXkhb8Hg3c)

For Developers
============

You can also see [Cython](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-Cy), [Java](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation), [C++](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-CPP), [C](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-C), 
[Js](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-Js), [Swift](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-Swift), or [C#](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-CS) repository.

## Requirements

* [Python 3.7 or higher](#python)
* [Git](#git)

### Python 

To check if you have a compatible version of Python installed, use the following command:

   	python -V
    
You can find the latest version of Python [here](https://www.python.org/downloads/).

### Git

Install the [latest version of Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Pip Install

	pip3 install NlpToolkit-MorphologicalDisambiguation

## Download Code

In order to work on code, create a fork from GitHub page. 
Use Git for cloning the code to your local or below line for Ubuntu:

	git clone <your-fork-git-link>

A directory called MorphologicalDisambiguation will be created. Or you can use below link for exploring the code:

	git clone https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-Py.git

## Open project with Pycharm IDE

Steps for opening the cloned project:

* Start IDE
* Select **File | Open** from main menu
* Choose `DataStructure-Py` file
* Select open as project option
* Couple of seconds, project will be downloaded. 

Detailed Description
============

+ [Creating MorphologicalDisambiguator](#creating-morphologicaldisambiguator)
+ [Training MorphologicalDisambiguator](#training-morphologicaldisambiguator)
+ [Sentence Disambiguation](#sentence-disambiguation)

## Creating MorphologicalDisambiguator 

MorphologicalDisambiguator provides Turkish morphological disambiguation. There are possible disambiguation techniques. Depending on the technique used, disambiguator can be instantiated as follows:

* Using `RootFirstDisambiguation`, the one that chooses only the root amongst the given analyses

        morphologicalDisambiguator = RootFirstDisambiguation()

* Using `RootWordStatisticsDisambiguation`, the one that chooses the root that is the most frequently used amongst the given analyses

        morphologicalDisambiguator = RootWordStatisticsDisambiguation()

* Using `LongestRootFirstDisambiguation`, the one that chooses the longest root among the given roots
        
        morphologicalDisambiguator = LongestRootFirstDisambiguation()

* Using `HmmDisambiguation`, the one that chooses using an Hmm-based algorithm
        
        morphologicalDisambiguator = HmmDisambiguation()

* Using `DummyDisambiguation`, the one that chooses a random one amongst the given analyses 
     
        morphologicalDisambiguator = DummyDisambiguation()
    

## Training MorphologicalDisambiguator

To train the disambiguator, an instance of `DisambiguationCorpus` object is needed. This can be instantiated and the disambiguator can be trained and saved as follows:

    corpus = DisambiguationCorpus("penn_treebank.txt")
    morphologicalDisambiguator.train(corpus)
    morphologicalDisambiguator.saveModel()
    
      
## Sentence Disambiguation

To disambiguate a sentence, a `FsmMorphologicalAnalyzer` instance is required. This can be created as below, further information can be found [here](https://github.com/starlangsoftware/MorphologicalAnalysis/blob/master/README.md#creating-fsmmorphologicalanalyzer).

    fsm = FsmMorphologicalAnalyzer()
    
A sentence can be disambiguated as follows: 
    
    sentence = Sentence("Yarın doktora gidecekler")
    fsmParseList = fsm.robustMorphologicalAnalysis(sentence)
    print("All parses\n")
    print("--------------------------\n")
    for i in range(len(fsmParseList)):
        print(fsmParseList[i])
    candidateParses = morphologicalDisambiguator.disambiguate(fsmParseList)
    print("Parses after disambiguation\n")
    print("--------------------------"\n)
    for i in range(candidateParses.size()):
        print(candidateParses.get(i) + "\n")

Output

    
    All parses
    --------------------------
    yar+NOUN+A3SG+P2SG+NOM
    yar+NOUN+A3SG+PNON+GEN
    yar+VERB+POS+IMP+A2PL
    yarı+NOUN+A3SG+P2SG+NOM
    yarın+NOUN+A3SG+PNON+NOM
    
    doktor+NOUN+A3SG+PNON+DAT
    doktora+NOUN+A3SG+PNON+NOM
    
    git+VERB+POS+FUT+A3PL
    git+VERB+POS^DB+NOUN+FUTPART+A3PL+PNON+NOM
    
    Parses after disambiguation
    --------------------------
    yarın+NOUN+A3SG+PNON+NOM
    doktor+NOUN+A3SG+PNON+DAT
    git+VERB+POS+FUT+A3PL

# Cite

	@InProceedings{gorgunyildiz12,
	author="G{\"o}rg{\"u}n, Onur
	and Yildiz, Olcay Taner",
	editor="Gelenbe, Erol
	and Lent, Ricardo
	and Sakellari, Georgia",
	title="A Novel Approach to Morphological Disambiguation for Turkish",
	booktitle="Computer and Information Sciences II",
	year="2012",
	publisher="Springer London",
	address="London",
	pages="77--83",
	isbn="978-1-4471-2155-8"
	}
