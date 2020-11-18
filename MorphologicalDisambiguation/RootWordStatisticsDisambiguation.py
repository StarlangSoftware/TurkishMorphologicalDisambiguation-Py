from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus
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
        for fsmParseList in fsmParses:
            bestRoot = self.rootWordStatistics.bestRootWord(fsmParseList, 0.0)
            if bestRoot is not None:
                fsmParseList.reduceToParsesWithSameRoot(bestRoot)
                newBestParse = fsmParseList.caseDisambiguator()
                if newBestParse is not None:
                    bestParse = newBestParse
                else:
                    bestParse = fsmParseList.getFsmParse(0)
            else:
                bestParse = fsmParseList.getFsmParse(0)
            correctFsmParses.append(bestParse)
        return correctFsmParses

    def saveModel(self):
        pass

    def loadModel(self):
        pass
