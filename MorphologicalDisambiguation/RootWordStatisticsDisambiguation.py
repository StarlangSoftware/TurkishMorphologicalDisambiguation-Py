from MorphologicalDisambiguation.AutoDisambiguator import AutoDisambiguator
from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator
from MorphologicalDisambiguation.RootWordStatistics import RootWordStatistics


class RootWordStatisticsDisambiguation(MorphologicalDisambiguator):

    rootWordStatistics: RootWordStatistics

    def train(self, corpus: DisambiguationCorpus):
        """
        Train method implements method in MorphologicalDisambiguator.

        PARAMETERS
        ----------
        corpus : DisambiguationCorpus
            DisambiguationCorpus to train.
        """
        self.rootWordStatistics = RootWordStatistics("../penntreebank_statistics.txt")

    def disambiguate(self, fsmParses: list) -> list:
        """
        The disambiguate method gets an array of fsmParses. Then loops through that parses and finds the longest root
        word. At the end, gets the parse with longest word among the fsmParses and adds it to the correctFsmParses
        list.

        PARAMETERS
        ----------
        fsmParses : list
            FsmParseList to disambiguate.

        RETURNS
        -------
        list
            CorrectFsmParses list.
        """
        correctFsmParses = []
        i = 0
        for fsmParseList in fsmParses:
            rootWords = fsmParseList.rootWords()
            if "$" in rootWords:
                bestRoot = self.rootWordStatistics.bestRootWord(fsmParseList, 0.0)
                if bestRoot is None:
                    bestRoot = fsmParseList.getParseWithLongestRootWord().getWord().getName()
            else:
                bestRoot = rootWords
            if bestRoot is not None:
                fsmParseList.reduceToParsesWithSameRoot(bestRoot)
                newBestParse = AutoDisambiguator.caseDisambiguator(i, fsmParses, correctFsmParses)
                if newBestParse is not None:
                    bestParse = newBestParse
                else:
                    bestParse = fsmParseList.getFsmParse(0)
            else:
                bestParse = fsmParseList.getFsmParse(0)
            correctFsmParses.append(bestParse)
            i = i + 1
        return correctFsmParses

    def saveModel(self):
        pass

    def loadModel(self):
        pass
