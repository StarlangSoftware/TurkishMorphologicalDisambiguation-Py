import unittest

from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer

from MorphologicalDisambiguation.RootWordStatistics import RootWordStatistics


class RootWordStatisticsTest(unittest.TestCase):

    def test_RootWordStatistics(self):
        fsm = FsmMorphologicalAnalyzer("../turkish_dictionary.txt", "../turkish_misspellings.txt",
                                       "../turkish_finite_state_machine.xml")
        rootWordStatistics = RootWordStatistics("../penntreebank_statistics.txt")
        self.assertTrue(rootWordStatistics.containsKey("yasasını"))
        self.assertTrue(rootWordStatistics.containsKey("yapılandırıyorlar"))
        self.assertTrue(rootWordStatistics.containsKey("çöküşten"))
        self.assertEqual("yasa", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("yasasını"), 0.0))
        self.assertEqual("karşılaş", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("karşılaşabilir"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("karşılaşabilir"), 0.7))
        self.assertEqual("anlat", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("anlattı"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("anlattı"), 0.9))
        self.assertEqual("ver", rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("vermesini"), 0.0))
        self.assertIsNone(rootWordStatistics.bestRootWord(fsm.morphologicalAnalysis("vermesini"), 0.9))


if __name__ == '__main__':
    unittest.main()
