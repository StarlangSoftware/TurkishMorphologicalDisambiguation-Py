import unittest

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer

from MorphologicalDisambiguation.RootWordStatistics import RootWordStatistics


class RootWordStatisticsTest(unittest.TestCase):

    def test_RootWordStatistics(self):
        fsm = FsmMorphologicalAnalyzer("../turkish_dictionary.txt", "../turkish_misspellings.txt",
                                       "../turkish_finite_state_machine.xml")
        rootWordStatistics = RootWordStatistics("../penntreebank_statistics.txt")
        self.assertTrue(rootWordStatistics.containsKey("it$iti$itici"))
        self.assertTrue(rootWordStatistics.containsKey("yas$yasa$yasama"))
        self.assertTrue(rootWordStatistics.containsKey("tutuk$tutukla"))
        self.assertEqual("çık", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("çıkma"), 0.0))
        self.assertEqual("danışman", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("danışman"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("danışman"), 0.7))
        self.assertEqual("görüşme", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("görüşme"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("görüşme"), 0.7))
        self.assertEqual("anlaş", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("anlaşma"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("anlaşma"), 0.7))


if __name__ == '__main__':
    unittest.main()
