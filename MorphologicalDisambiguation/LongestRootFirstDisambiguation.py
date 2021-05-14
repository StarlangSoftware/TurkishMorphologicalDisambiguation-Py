from MorphologicalDisambiguation.AutoDisambiguator import AutoDisambiguator
from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator


class LongestRootFirstDisambiguation(MorphologicalDisambiguator):

    def train(self, corpus: DisambiguationCorpus):
        """
        Train method implements method in MorphologicalDisambiguator.

        PARAMETERS
        ----------
        corpus : DisambiguationCorpus
            DisambiguationCorpus to train.
        """
        pass

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
            bestParse = fsmParseList.getParseWithLongestRootWord()
            fsmParseList.reduceToParsesWithSameRootAndPos(bestParse.getWordWithPos())
            newBestParse = AutoDisambiguator.caseDisambiguator(i, fsmParses, correctFsmParses)
            if newBestParse is not None:
                bestParse = newBestParse
            correctFsmParses.append(bestParse)
            i = i + 1
        return correctFsmParses

    def saveModel(self):
        pass

    def loadModel(self):
        pass
