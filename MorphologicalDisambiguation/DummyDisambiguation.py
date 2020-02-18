from random import randrange

from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator


class DummyDisambiguation(MorphologicalDisambiguator):

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
        Overridden disambiguate method takes an array of FsmParseList and loops through its items, if the current
        FsmParseList's size is greater than 0, it adds a random parse of this list to the correctFsmParses list.

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
            if fsmParseList.size() > 0:
                correctFsmParses.append(fsmParseList.getFsmParse(randrange(fsmParseList.size())))
        return correctFsmParses
