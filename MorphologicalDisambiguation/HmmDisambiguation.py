import math

from Dictionary.Word import Word
from MorphologicalAnalysis.FsmParse import FsmParse
from NGram.LaplaceSmoothing import LaplaceSmoothing
from NGram.NGram import NGram

from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.NaiveDisambiguation import NaiveDisambiguation


class HmmDisambiguation(NaiveDisambiguation):

    wordBiGramModel: NGram
    igBiGramModel: NGram

    def train(self, corpus: DisambiguationCorpus):
        """
        The train method gets sentences from given DisambiguationCorpus and both word and the next word of that sentence
        at each iteration. Then, adds these words together with their part of speech tags to word unigram and bigram
        models. It also adds the last inflectional group of word to the ig unigram and bigram models.

        At the end, it calculates the NGram probabilities of both word and ig unigram models by using LaplaceSmoothing,
        and both word and ig bigram models by using InterpolatedSmoothing.

        PARAMETERS
        ----------
        corpus : DisambiguationCorpus
            DisambiguationCorpus to train.
        """
        words1 = [None]
        igs1 = [None]
        words2 = [None, None]
        igs2 = [None, None]
        self.wordUniGramModel = NGram(1)
        self.igUniGramModel = NGram(1)
        self.wordBiGramModel = NGram(2)
        self.igBiGramModel = NGram(2)
        for sentence in corpus.sentences:
            for j in range(sentence.wordCount() - 1):
                word = sentence.getWord(j)
                nextWord = sentence.getWord(j + 1)
                words2[0] = word.getParse().getWordWithPos()
                words1[0] = words2[0]
                words2[1] = nextWord.getParse().getWordWithPos()
                self.wordUniGramModel.addNGram(words1)
                self.wordBiGramModel.addNGram(words2)
                for k in range(nextWord.getParse().size()):
                    igs2[0] = Word(word.getParse().getLastInflectionalGroup().__str__())
                    igs2[1] = Word(nextWord.getParse().getInflectionalGroup(k).__str__())
                    self.igBiGramModel.addNGram(igs2)
                    igs1[0] = igs2[1]
                    self.igUniGramModel.addNGram(igs1)
        self.wordUniGramModel.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.igUniGramModel.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.wordBiGramModel.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.igBiGramModel.calculateNGramProbabilitiesSimple(LaplaceSmoothing())

    def disambiguate(self, fsmParses: list) -> list:
        """
        The disambiguate method takes FsmParseList as an input and gets one word with its part of speech tags, then gets
        its probability from word unigram model. It also gets ig and its probability. Then, hold the logarithmic value
        of the product of these probabilities in an array. Also by taking into consideration the parses of these word it
        recalculates the probabilities and returns these parses.

        PARAMETERS
        ----------
        fsmParses : list
            FsmParseList to disambiguate.

        RETURNS
        -------
        list
            List of FsmParses.
        """
        if len(fsmParses) == 0:
            return None
        for i in range(len(fsmParses)):
            if fsmParses[i].size() == 0:
                return None
        correctFsmParses = []
        probabilities = [[0.0 for _ in range(fsmParses[i].size())] for i in range(len(fsmParses))]
        best = [[0 for _ in range(fsmParses[i].size())] for i in range(len(fsmParses))]
        for i in range(fsmParses[0].size()):
            currentParse = fsmParses[0].getFsmParse(i)
            if isinstance(currentParse, FsmParse):
                w1 = currentParse.getWordWithPos()
                probability = self.wordUniGramModel.getProbability(w1)
                for j in range(currentParse.size()):
                    ig1 = Word(currentParse.getInflectionalGroup(j).__str__())
                    probability *= self.igUniGramModel.getProbability(ig1)
                probabilities[0][i] = math.log(probability)
        for i in range(1, len(fsmParses)):
            for j in range(fsmParses[i].size()):
                bestProbability = -10000
                bestIndex = -1
                currentParse = fsmParses[i].getFsmParse(j)
                if isinstance(currentParse, FsmParse):
                    for k in range(fsmParses[i - 1].size()):
                        previousParse = fsmParses[i - 1].getFsmParse(k)
                        w1 = previousParse.getWordWithPos()
                        w2 = currentParse.getWordWithPos()
                        probability = probabilities[i - 1][k] + math.log(self.wordBiGramModel.getProbability(w1, w2))
                        for t in range(fsmParses[i].getFsmParse(j).size()):
                            ig1 = Word(previousParse.lastInflectionalGroup().__str__())
                            ig2 = Word(currentParse.getInflectionalGroup(t).__str__())
                            probability += math.log(self.igBiGramModel.getProbability(ig1, ig2))
                        if probability > bestProbability:
                            bestIndex = k
                            bestProbability = probability
                probabilities[i][j] = bestProbability
                best[i][j] = bestIndex
        bestProbability = -10000
        bestIndex = -1
        for i in range(fsmParses[len(fsmParses) - 1].size()):
            if probabilities[len(fsmParses) - 1][i] > bestProbability:
                bestProbability = probabilities[len(fsmParses) - 1][i]
                bestIndex = i
        if bestIndex == -1:
            return None
        correctFsmParses.append(fsmParses[len(fsmParses) - 1].getFsmParse(bestIndex))
        for i in range(len(fsmParses) - 2, -1, -1):
            bestIndex = best[i + 1][bestIndex]
            if bestIndex == -1:
                return None
            correctFsmParses.insert(0, fsmParses[i].getFsmParse(bestIndex))
        return correctFsmParses

    def saveModel(self):
        """
        Method to save unigrams and bigrams.
        """
        super().saveModel()
        self.wordBiGramModel.saveAsText("words2.txt")
        self.igBiGramModel.saveAsText("igs2.txt")

    def loadModel(self):
        """
        Method to load unigrams and bigrams.
        """
        super().loadModel()
        self.wordBiGramModel = NGram("words2.txt")
        self.igBiGramModel = NGram("igs2.txt")
