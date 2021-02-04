For Developers
============

You can also see [Python](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-Py), [Java](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation), [C++](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-CPP), or [C#](https://github.com/starlangsoftware/TurkishMorphologicalDisambiguation-CS) repository.

## Requirements

* [Python 3.7 or higher](#python)
* [Git](#git)

### Python 

To check if you have a compatible version of Python installed, use the following command:

    python -V
    
You can find the latest version of Python [here](https://www.python.org/downloads/).

### Git

Install the [latest version of Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

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
* Choose `DataStructure-PY` file
* Select open as project option
* Couple of seconds, project will be downloaded. 

For Developers
============

+ [Creating MorphologicalDisambiguator](#creating-morphologicaldisambiguator)
+ [Training MorphologicalDisambiguator](#training-morphologicaldisambiguator)
+ [Sentence Disambiguation](#sentence-disambiguation)

## Creating MorphologicalDisambiguator 

MorphologicalDisambiguator provides Turkish morphological disambiguation. There are possible disambiguation techniques. Depending on the technique used, disambiguator can be instantiated as follows:

* Using `RootFirstDisambiguation`, the one that chooses only the root amongst the given analyses

        morphologicalDisambiguator = RootFirstDisambiguation()

* Using `LongestRootFirstDisambiguation`, the one that chooses the root that is the most frequently used amongst the given analyses

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
