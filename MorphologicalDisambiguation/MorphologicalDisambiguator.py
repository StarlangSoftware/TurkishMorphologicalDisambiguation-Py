from abc import abstractmethod

from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus


class MorphologicalDisambiguator:


    """
    Method to train the given DisambiguationCorpus.

    PARAMETERS
    ----------
    corpus : DisambiguationCorpus
        DisambiguationCorpus to train.
    """
    @abstractmethod
    def train(self, corpus: DisambiguationCorpus):
        pass

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
    def disambiguate(self, fsmParses: list) -> list:
        pass