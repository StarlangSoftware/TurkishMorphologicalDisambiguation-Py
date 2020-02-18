from NGram.NGram import NGram

from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator


class NaiveDisambiguation(MorphologicalDisambiguator):

    wordUniGramModel: NGram
    igUniGramModel: NGram
