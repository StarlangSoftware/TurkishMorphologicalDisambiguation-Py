import math

from Dictionary.Word import Word
from MorphologicalAnalysis.FsmParse import FsmParse
from NGram.LaplaceSmoothing import LaplaceSmoothing
from NGram.NGram import NGram

from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.NaiveDisambiguation import NaiveDisambiguation


class HmmDisambiguation(NaiveDisambiguation):

    word_bi_gram_model: NGram
    ig_bi_gram_model: NGram

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
        self.word_uni_gram_model = NGram(1)
        self.ig_uni_gram_model = NGram(1)
        self.word_bi_gram_model = NGram(2)
        self.ig_bi_gram_model = NGram(2)
        for sentence in corpus.sentences:
            for j in range(sentence.wordCount() - 1):
                word = sentence.getWord(j)
                next_word = sentence.getWord(j + 1)
                words2[0] = word.getParse().getWordWithPos()
                words1[0] = words2[0]
                words2[1] = next_word.getParse().getWordWithPos()
                self.word_uni_gram_model.addNGram(words1)
                self.word_bi_gram_model.addNGram(words2)
                for k in range(next_word.getParse().size()):
                    igs2[0] = Word(word.getParse().getLastInflectionalGroup().__str__())
                    igs2[1] = Word(next_word.getParse().getInflectionalGroup(k).__str__())
                    self.ig_bi_gram_model.addNGram(igs2)
                    igs1[0] = igs2[1]
                    self.ig_uni_gram_model.addNGram(igs1)
        self.word_uni_gram_model.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.ig_uni_gram_model.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.word_bi_gram_model.calculateNGramProbabilitiesSimple(LaplaceSmoothing())
        self.ig_bi_gram_model.calculateNGramProbabilitiesSimple(LaplaceSmoothing())

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
        correct_fsm_parses = []
        probabilities = [[0.0 for _ in range(fsmParses[i].size())] for i in range(len(fsmParses))]
        best = [[0 for _ in range(fsmParses[i].size())] for i in range(len(fsmParses))]
        for i in range(fsmParses[0].size()):
            current_parse = fsmParses[0].getFsmParse(i)
            if isinstance(current_parse, FsmParse):
                w1 = current_parse.getWordWithPos()
                probability = self.word_uni_gram_model.getProbability(w1)
                for j in range(current_parse.size()):
                    ig1 = Word(current_parse.getInflectionalGroup(j).__str__())
                    probability *= self.ig_uni_gram_model.getProbability(ig1)
                probabilities[0][i] = math.log(probability)
        for i in range(1, len(fsmParses)):
            for j in range(fsmParses[i].size()):
                best_probability = -10000
                best_index = -1
                current_parse = fsmParses[i].getFsmParse(j)
                if isinstance(current_parse, FsmParse):
                    for k in range(fsmParses[i - 1].size()):
                        previous_parse = fsmParses[i - 1].getFsmParse(k)
                        w1 = previous_parse.getWordWithPos()
                        w2 = current_parse.getWordWithPos()
                        probability = probabilities[i - 1][k] + math.log(self.word_bi_gram_model.getProbability(w1, w2))
                        for t in range(fsmParses[i].getFsmParse(j).size()):
                            ig1 = Word(previous_parse.lastInflectionalGroup().__str__())
                            ig2 = Word(current_parse.getInflectionalGroup(t).__str__())
                            probability += math.log(self.ig_bi_gram_model.getProbability(ig1, ig2))
                        if probability > best_probability:
                            best_index = k
                            best_probability = probability
                probabilities[i][j] = best_probability
                best[i][j] = best_index
        best_probability = -10000
        best_index = -1
        for i in range(fsmParses[len(fsmParses) - 1].size()):
            if probabilities[len(fsmParses) - 1][i] > best_probability:
                best_probability = probabilities[len(fsmParses) - 1][i]
                best_index = i
        if best_index == -1:
            return None
        correct_fsm_parses.append(fsmParses[len(fsmParses) - 1].getFsmParse(best_index))
        for i in range(len(fsmParses) - 2, -1, -1):
            best_index = best[i + 1][best_index]
            if best_index == -1:
                return None
            correct_fsm_parses.insert(0, fsmParses[i].getFsmParse(best_index))
        return correct_fsm_parses

    def saveModel(self):
        """
        Method to save unigrams and bigrams.
        """
        super().saveModel()
        self.word_bi_gram_model.saveAsText("words2.txt")
        self.ig_bi_gram_model.saveAsText("igs2.txt")

    def loadModel(self):
        """
        Method to load unigrams and bigrams.
        """
        super().loadModel()
        self.word_bi_gram_model = NGram("words2.txt")
        self.ig_bi_gram_model = NGram("igs2.txt")
