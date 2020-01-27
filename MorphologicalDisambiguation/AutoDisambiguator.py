from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalDisambiguation.RootWordStatistics import RootWordStatistics


class AutoDisambiguator:

    morphologicalAnalyzer: FsmMorphologicalAnalyzer
    rootWordStatistics: RootWordStatistics