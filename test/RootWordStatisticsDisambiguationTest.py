import unittest

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer

from MorphologicalDisambiguation.DisambiguatedWord import DisambiguatedWord
from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.RootWordStatisticsDisambiguation import RootWordStatisticsDisambiguation


class RootWordStatisticsDisambiguationTest(unittest.TestCase):

    def test_Disambiguation(self):
        fsm = FsmMorphologicalAnalyzer("../turkish_dictionary.txt", "../turkish_misspellings.txt",
                                       "../turkish_finite_state_machine.xml")
        corpus = DisambiguationCorpus("../penntreebank.txt")
        algorithm = RootWordStatisticsDisambiguation()
        algorithm.train(corpus)
        correctParse = 0
        correctRoot = 0
        for i in range(corpus.sentenceCount()):
            sentenceAnalyses = fsm.robustMorphologicalAnalysis(corpus.getSentence(i))
            fsmParses =  algorithm.disambiguate(sentenceAnalyses)
            for j in range(corpus.getSentence(i).wordCount()):
                word = corpus.getSentence(i).getWord(j)
                if isinstance(word, DisambiguatedWord):
                    if fsmParses[j].transitionList() == word.getParse().__str__():
                        correctParse = correctParse + 1
                    if fsmParses[j].getWord() == word.getParse().getWord():
                        correctRoot = correctRoot + 1
        self.assertAlmostEqual(0.9631, (correctRoot + 0.0) / corpus.numberOfWords(), 3)
        self.assertAlmostEqual(0.8733, (correctParse + 0.0) / corpus.numberOfWords(), 3)


if __name__ == '__main__':
    unittest.main()
