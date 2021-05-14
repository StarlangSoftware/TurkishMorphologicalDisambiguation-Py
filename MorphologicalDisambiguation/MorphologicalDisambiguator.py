from abc import abstractmethod

from DisambiguationCorpus.DisambiguationCorpus import DisambiguationCorpus


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

    @abstractmethod
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

    @abstractmethod
    def saveModel(self):
        """
        Method to save a model.
        """
        pass

    @abstractmethod
    def loadModel(self):
        """
        Method to load a model.
        """
        pass
