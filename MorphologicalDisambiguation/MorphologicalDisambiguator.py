from abc import abstractmethod

from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus


class MorphologicalDisambiguator:

    @abstractmethod
    def train(self, corpus: DisambiguationCorpus):
        """
        Method to train the given DisambiguationCorpus.

        PARAMETERS
        ----------
        corpus : DisambiguationCorpus
            DisambiguationCorpus to train.
        """
        pass

    def disambiguate(self, fsmParses: list) -> list:
        """
        Method to disambiguate the given FsmParseList.

        PARAMETERS
        ----------
        fsmParses : list
            FsmParseList to disambiguate.

        RETURNS
        -------
        list
            List of FsmParse.
        """
        pass
