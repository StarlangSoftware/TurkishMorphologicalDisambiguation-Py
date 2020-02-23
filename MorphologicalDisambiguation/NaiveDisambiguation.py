from NGram.NGram import NGram

from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator


class NaiveDisambiguation(MorphologicalDisambiguator):

    wordUniGramModel: NGram
    igUniGramModel: NGram

    def saveModel(self):
        """
        The saveModel method writes the specified objects i.e wordUniGramModel and igUniGramModel to the
        words1.txt and igs1.txt.
        """
        self.wordUniGramModel.saveAsText("words1.txt")
        self.igUniGramModel.saveAsText("igs1.txt")

    def loadModel(self):
        """
        The loadModel method reads objects at the words1.txt and igs1.txt to the wordUniGramModel and igUniGramModel.
        """
        self.wordUniGramModel = NGram("words1.txt")
        self.igUniGramModel = NGram("igs1.txt")
