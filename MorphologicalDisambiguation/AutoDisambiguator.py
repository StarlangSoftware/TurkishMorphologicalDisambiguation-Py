from __future__ import annotations
from DataStructure.CounterHashMap import CounterHashMap
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalAnalysis.FsmParse import FsmParse
from MorphologicalAnalysis.FsmParseList import FsmParseList
from MorphologicalAnalysis.MorphologicalTag import MorphologicalTag


class AutoDisambiguator:
    morphologicalAnalyzer: FsmMorphologicalAnalyzer

    @staticmethod
    def isAnyWordSecondPerson(index: int, correctParses: list) -> bool:
        count = 0
        for i in range(index - 1, -1, -1):
            if correctParses[i].containsTag(MorphologicalTag.A2SG) or \
                    correctParses[i].containsTag(MorphologicalTag.P2SG):
                count = count + 1
        return count >= 1

    @staticmethod
    def isPossessivePlural(index: int, correctParses: list) -> bool:
        for i in range(index - 1, -1, -1):
            if correctParses[i].isNoun():
                return correctParses[i].isPlural()
        return False

    @staticmethod
    def nextWordPos(nextParseList: FsmParseList) -> str:
        _map = CounterHashMap()
        for i in range(nextParseList.size()):
            _map.put(nextParseList.getFsmParse(i).getPos())
        return _map.max()

    @staticmethod
    def isBeforeLastWord(index: int, fsmParses: list) -> bool:
        return index + 2 == len(fsmParses)

    @staticmethod
    def nextWordExists(index: int, fsmParses: list) -> bool:
        return index + 1 < len(fsmParses)

    @staticmethod
    def isNextWordNoun(index: int, fsmParses: list) -> bool:
        return index + 1 < len(fsmParses) and AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "NOUN"

    @staticmethod
    def isNextWordNum(index: int, fsmParses: list) -> bool:
        return index + 1 < len(fsmParses) and AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "NUM"

    @staticmethod
    def isNextWordNounOrAdjective(index: int, fsmParses: list) -> bool:
        return index + 1 < len(fsmParses) and (AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "NOUN" or
                                               AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "ADJ" or
                                               AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "DET")

    @staticmethod
    def isFirstWord(index: int) -> bool:
        return index == 0

    @staticmethod
    def containsTwoNeOrYa(fsmParses: list, word: str) -> bool:
        count = 0
        for fsmPars in fsmParses:
            surfaceForm = fsmPars.getFsmParse(0).getSurfaceForm()
            if surfaceForm == word:
                count = count + 1
        return count == 2

    @staticmethod
    def hasPreviousWordTag(index: int, correctParses: list, tag: MorphologicalTag) -> bool:
        return index > 0 and correctParses[index - 1].containsTag(tag)

    @staticmethod
    def selectCaseForParseString(parseString: str, index: int, fsmParses: list, correctParses: list) -> str:
        surfaceForm = fsmParses[index].getFsmParse(0).getSurfaceForm()
        root = fsmParses[index].getFsmParse(0).getWord().getName()
        lastWord = fsmParses[len(fsmParses) - 1].getFsmParse(0).getSurfaceForm()
        # kısmını, duracağını, grubunun #
        if parseString == "P2SG$P3SG":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "P2SG"
            return "P3SG"
        elif parseString == "A2SG+P2SG$A3SG+P3SG":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "A2SG+P2SG"
            return "A3SG+P3SG"
            # BİR #
        elif parseString == "ADJ$ADV$DET$NUM+CARD":
            return "DET"
            # tahminleri, işleri, hisseleri #
        elif parseString == "A3PL+P3PL+NOM$A3PL+P3SG+NOM$A3PL+PNON+ACC$A3SG+P3PL+NOM":
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "A3SG+P3PL+NOM"
            return "A3PL+P3SG+NOM"
            # Ocak, Cuma, ABD #
        elif parseString == "A3SG$PROP+A3SG":
            if index > 0:
                return "PROP+A3SG"
            # şirketin, seçimlerin, borsacıların, kitapların #
        elif parseString == "P2SG+NOM$PNON+GEN":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "P2SG+NOM"
            return "PNON+GEN"
            # FAZLA #
            # ÇOK #
        elif parseString == "ADJ$ADV$DET$POSTP+PCABL" or parseString == "ADJ$ADV$POSTP+PCABL":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            if index + 1 < len(fsmParses):
                if AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "NOUN":
                    return "ADJ"
                elif AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "ADJ" or \
                        AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "ADV" or \
                        AutoDisambiguator.nextWordPos(fsmParses[index + 1]) == "VERB":
                    return "ADV"
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ"
            return "NOUN+A3SG+PNON+NOM"
            # fanatiklerini, senetlerini, olduklarını #
        elif parseString == "A3PL+P2SG$A3PL+P3PL$A3PL+P3SG$A3SG+P3PL":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "A3PL+P2SG"
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "A3SG+P3PL"
            else:
                return "A3PL+P3SG"
        elif parseString == "ADJ$NOUN+PROP+A3SG+PNON+NOM":
            if index > 0:
                return "NOUN+PROP+A3SG+PNON+NOM"
            # BU, ŞU #
        elif parseString == "DET$PRON+DEMONSP+A3SG+PNON+NOM":
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "DET"
            return "PRON+DEMONSP+A3SG+PNON+NOM"
            # gelebilir #
        elif parseString == "AOR+A3SG$AOR^DB+ADJ+ZERO":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "AOR+A3SG"
            elif AutoDisambiguator.isFirstWord(index):
                return "AOR^DB+ADJ+ZERO"
            elif AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "AOR^DB+ADJ+ZERO"
            else:
                return "AOR+A3SG"
        elif parseString == "ADV$NOUN+A3SG+PNON+NOM":
            return "ADV"
        elif parseString == "ADJ$ADV":
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "ADJ"
            return "ADV"
        elif parseString == "P2SG$PNON":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "P2SG"
            return "PNON"
            # etti, kırdı #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO$VERB+POS":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "VERB+POS"
            # İLE #
        elif parseString == "CONJ$POSTP+PCNOM":
            return "POSTP+PCNOM"
            # gelecek #
        elif parseString == "POS+FUT+A3SG$POS^DB+ADJ+FUTPART+PNON":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "POS+FUT+A3SG"
            return "POS^DB+ADJ+FUTPART+PNON"
        elif parseString == "ADJ^DB$NOUN+A3SG+PNON+NOM^DB":
            if root == "yok" or root == "düşük" or root == "eksik" or root == "rahat" or root == "orta" \
                    or root == "vasat":
                return "ADJ^DB"
            return "NOUN+A3SG+PNON+NOM^DB"
            # yaptık, şüphelendik #
        elif parseString == "POS+PAST+A1PL$POS^DB+ADJ+PASTPART+PNON$POS^DB+NOUN+PASTPART+A3SG+PNON+NOM":
            return "POS+PAST+A1PL"
            # ederim, yaparım #
        elif parseString == "AOR+A1SG$AOR^DB+ADJ+ZERO^DB+NOUN+ZERO+A3SG+P1SG+NOM":
            return "AOR+A1SG"
            # geçti, vardı, aldı #
        elif parseString == "ADJ^DB+VERB+ZERO$VERB+POS":
            if root == "var" and not AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "ADJ^DB+VERB+ZERO"
            return "VERB+POS"
            # ancak #
        elif parseString == "ADV$CONJ":
            return "CONJ"
            # yaptığı, ettiği #
        elif parseString == "ADJ+PASTPART+P3SG$NOUN+PASTPART+A3SG+P3SG+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+PASTPART+P3SG"
            return "NOUN+PASTPART+A3SG+P3SG+NOM"
            # ÖNCE, SONRA #
        elif parseString == "ADV$NOUN+A3SG+PNON+NOM$POSTP+PCABL":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            return "ADV"
        elif parseString == "NARR+A3SG$NARR^DB+ADJ+ZERO":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "NARR+A3SG"
            return "NARR^DB+ADJ+ZERO"
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM$NOUN+PROP+A3SG+PNON+NOM":
            if index > 0:
                return "NOUN+PROP+A3SG+PNON+NOM"
            elif AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ"
            return "NOUN+A3SG+PNON+NOM"
            # ödediğim #
        elif parseString == "ADJ+PASTPART+P1SG$NOUN+PASTPART+A3SG+P1SG+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+PASTPART+P1SG"
            return "NOUN+PASTPART+A3SG+P1SG+NOM"
            # O #
        elif parseString == "DET$PRON+DEMONSP+A3SG+PNON+NOM$PRON+PERS+A3SG+PNON+NOM":
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "DET"
            return "PRON+PERS+A3SG+PNON+NOM"
            # BAZI #
        elif parseString == "ADJ$DET$PRON+QUANTP+A3SG+P3SG+NOM":
            return "DET"
            # ONUN, ONA, ONDAN, ONUNLA, OYDU, ONUNKİ #
        elif parseString == "DEMONSP$PERS":
            return "PERS"
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ"
            return "NOUN+A3SG+PNON+NOM"
            # hazineler, kıymetler #
        elif parseString == "A3PL+PNON+NOM$A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A3PL$PROP+A3PL+PNON+NOM":
            if index > 0:
                if fsmParses[index].getFsmParse(0).isCapitalWord():
                    return "PROP+A3PL+PNON+NOM"
                return "A3PL+PNON+NOM"
            # ARTIK, GERİ #
        elif parseString == "ADJ$ADV$NOUN+A3SG+PNON+NOM":
            if root == "artık":
                return "ADV"
            elif AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "ADJ"
            return "ADV"
        elif parseString == "P1SG+NOM$PNON+NOM^DB+VERB+ZERO+PRES+A1SG":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses) or root == "değil":
                return "PNON+NOM^DB+VERB+ZERO+PRES+A1SG"
            return "P1SG+NOM"
            # görülmektedir #
        elif parseString == "POS+PROG2$POS^DB+NOUN+INF+A3SG+PNON+LOC^DB+VERB+ZERO+PRES":
            return "POS+PROG2"
            # NE #
        elif parseString == "ADJ$ADV$CONJ$PRON+QUESP+A3SG+PNON+NOM":
            if lastWord == "?":
                return "PRON+QUESP+A3SG+PNON+NOM"
            if AutoDisambiguator.containsTwoNeOrYa(fsmParses, "ne"):
                return "CONJ"
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "ADJ"
            return "ADV"
            # TÜM #
        elif parseString == "DET$NOUN+A3SG+PNON+NOM":
            return "DET"
            # AZ #
        elif parseString == "ADJ$ADV$POSTP+PCABL$VERB+POS+IMP+A2SG":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ"
            return "ADV"
            # görülmedik #
        elif parseString == "NEG+PAST+A1PL$NEG^DB+ADJ+PASTPART+PNON$NEG^DB+NOUN+PASTPART+A3SG+PNON+NOM":
            if surfaceForm == "alışılmadık":
                return "NEG^DB+ADJ+PASTPART+PNON"
            return "NEG+PAST+A1PL"
        elif parseString == "DATE$NUM+FRACTION":
            return "NUM+FRACTION"
            # giriş, satış, öpüş, vuruş #
        elif parseString == "POS^DB+NOUN+INF3+A3SG+PNON+NOM$RECIP+POS+IMP+A2SG":
            return "POS^DB+NOUN+INF3+A3SG+PNON+NOM"
            # başka, yukarı #
        elif parseString == "ADJ$POSTP+PCABL":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            return "ADJ"
            # KARŞI #
        elif parseString == "ADJ$ADV$NOUN+A3SG+PNON+NOM$POSTP+PCDAT":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.DATIVE):
                return "POSTP+PCDAT"
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "ADJ"
            return "ADV"
            # BEN #
        elif parseString == "NOUN+A3SG$NOUN+PROP+A3SG$PRON+PERS+A1SG":
            return "PRON+PERS+A1SG"
            # yapıcı, verici #
        elif parseString == "ADJ+AGT$NOUN+AGT+A3SG+PNON+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+AGT"
            return "NOUN+AGT+A3SG+PNON+NOM"
            # BİLE #
        elif parseString == "ADV$VERB+POS+IMP+A2SG":
            return "ADV"
            # ortalamalar, uzaylılar, demokratlar #
        elif parseString == "NOUN+ZERO+A3PL+PNON+NOM$VERB+ZERO+PRES+A3PL":
            return "NOUN+ZERO+A3PL+PNON+NOM"
            # yasa, diye, yıla #
        elif parseString == "NOUN+A3SG+PNON+DAT$VERB+POS+OPT+A3SG":
            return "NOUN+A3SG+PNON+DAT"
            # BİZ, BİZE #
        elif parseString == "NOUN+A3SG$PRON+PERS+A1PL":
            return "PRON+PERS+A1PL"
            # AZDI #
        elif parseString == "ADJ^DB+VERB+ZERO$POSTP+PCABL^DB+VERB+ZERO$VERB+POS":
            return "ADJ^DB+VERB+ZERO"
            # BİRİNCİ, İKİNCİ, ÜÇÜNCÜ, DÖRDÜNCÜ, BEŞİNCİ #
        elif parseString == "ADJ$NUM+ORD":
            return "ADJ"
            # AY #
        elif parseString == "INTERJ$NOUN+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            return "NOUN+A3SG+PNON+NOM"
            # konuşmam, savunmam, etmem #
        elif parseString == "NEG+AOR+A1SG$POS^DB+NOUN+INF2+A3SG+P1SG+NOM":
            return "NEG+AOR+A1SG"
            # YA #
        elif parseString == "CONJ$INTERJ":
            if AutoDisambiguator.containsTwoNeOrYa(fsmParses, "ya"):
                return "CONJ"
            if AutoDisambiguator.nextWordExists(index, fsmParses) and \
                    fsmParses[index + 1].getFsmParse(0).getSurfaceForm() == "da":
                return "CONJ"
            return "INTERJ"
        elif parseString == "A3PL+P3PL$A3PL+P3SG$A3SG+P3PL":
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "A3SG+P3PL"
            return "A3PL+P3SG"
            # YÜZDE, YÜZLÜ #
        elif parseString == "NOUN$NUM+CARD^DB+NOUN+ZERO":
            return "NOUN"
            # almanlar, uzmanlar, elmaslar, katiller #
        elif parseString == "ADJ^DB+VERB+ZERO+PRES+A3PL$NOUN+A3PL+PNON+NOM$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A3PL":
            return "NOUN+A3PL+PNON+NOM"
            # fazlası, yetkilisi #
        elif parseString == "ADJ+JUSTLIKE$NOUN+ZERO+A3SG+P3SG+NOM":
            return "NOUN+ZERO+A3SG+P3SG+NOM"
            # HERKES, HERKESTEN, HERKESLE, HERKES #
        elif parseString == "NOUN+A3SG+PNON$PRON+QUANTP+A3PL+P3PL":
            return "PRON+QUANTP+A3PL+P3PL"
            # BEN, BENDEN, BENCE, BANA, BENDE #
        elif parseString == "NOUN+A3SG$PRON+PERS+A1SG":
            return "PRON+PERS+A1SG"
            # karşısından, geriye, geride #
        elif parseString == "ADJ^DB+NOUN+ZERO$NOUN":
            return "ADJ^DB+NOUN+ZERO"
            # gideceği, kalacağı #
        elif parseString == "ADJ+FUTPART+P3SG$NOUN+FUTPART+A3SG+P3SG+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+FUTPART+P3SG"
            return "NOUN+FUTPART+A3SG+P3SG+NOM"
            # bildiğimiz, geçtiğimiz, yaşadığımız #
        elif parseString == "ADJ+PASTPART+P1PL$NOUN+PASTPART+A3SG+P1PL+NOM":
            return "ADJ+PASTPART+P1PL"
            # eminim, memnunum, açım #
        elif parseString == "NOUN+ZERO+A3SG+P1SG+NOM$VERB+ZERO+PRES+A1SG":
            return "VERB+ZERO+PRES+A1SG"
            # yaparlar, olabilirler, değiştirirler #
        elif parseString == "AOR+A3PL$AOR^DB+ADJ+ZERO^DB+NOUN+ZERO+A3PL+PNON+NOM":
            return "AOR+A3PL"
            # san, yasa #
        elif parseString == "NOUN+A3SG+PNON+NOM$NOUN+PROP+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            if index > 0:
                return "NOUN+PROP+A3SG+PNON+NOM"
            # etmeyecek, yapmayacak, koşmayacak #
        elif parseString == "NEG+FUT+A3SG$NEG^DB+ADJ+FUTPART+PNON":
            return "NEG+FUT+A3SG"
            # etmeli, olmalı #
        elif parseString == "POS+NECES+A3SG$POS^DB+NOUN+INF2+A3SG+PNON+NOM^DB+ADJ+WITH":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "POS+NECES+A3SG"
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "POS^DB+NOUN+INF2+A3SG+PNON+NOM^DB+ADJ+WITH"
            return "POS+NECES+A3SG"
            # DE #
        elif parseString == "CONJ$NOUN+PROP+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            if index > 0:
                return "NOUN+PROP+A3SG+PNON+NOM"
            # GEÇ, SIK #
        elif parseString == "ADJ$ADV$VERB+POS+IMP+A2SG":
            if surfaceForm == "sık":
                previousWord = ""
                nextWord = ""
                if index - 1 > -1:
                    previousWord = fsmParses[index - 1].getFsmParse(0).getSurfaceForm()
                if index + 1 < len(fsmParses):
                    nextWord = fsmParses[index + 1].getFsmParse(0).getSurfaceForm()
                if previousWord == "sık" or nextWord == "sık":
                    return "ADV"
                if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                    return "ADJ"
            return "ADV"
            # BİRLİKTE #
        elif parseString == "ADV$POSTP+PCINS":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.INSTRUMENTAL):
                return "POSTP+PCINS"
            return "ADV"
            # yavaşça, dürüstçe, fazlaca #
        elif parseString == "ADJ+ASIF$ADV+LY$NOUN+ZERO+A3SG+PNON+EQU":
            return "ADV+LY"
            # FAZLADIR, FAZLAYDI, ÇOKTU, ÇOKTUR #
        elif parseString == "ADJ^DB$POSTP+PCABL^DB":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL^DB"
            return "ADJ^DB"
            # kaybettikleri, umdukları, gösterdikleri #
        elif parseString == "ADJ+PASTPART+P3PL$NOUN+PASTPART+A3PL+P3PL+NOM$NOUN+PASTPART+A3PL+P3SG+NOM$NOUN+PASTPART" \
                            "+A3SG+P3PL+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+PASTPART+P3PL"
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "NOUN+PASTPART+A3SG+P3PL+NOM"
            return "NOUN+PASTPART+A3PL+P3SG+NOM"
            # yılın, yolun #
        elif parseString == "NOUN+A3SG+P2SG+NOM$NOUN+A3SG+PNON+GEN$VERB+POS+IMP+A2PL$VERB^DB+VERB+PASS+POS+IMP+A2SG":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "NOUN+A3SG+P2SG+NOM"
            return "NOUN+A3SG+PNON+GEN"
            # sürmekte, beklenmekte, değişmekte #
        elif parseString == "POS+PROG2+A3SG$POS^DB+NOUN+INF+A3SG+PNON+LOC":
            return "POS+PROG2+A3SG"
            # KİMSE, KİMSEDE, KİMSEYE #
        elif parseString == "NOUN+A3SG+PNON$PRON+QUANTP+A3SG+P3SG":
            return "PRON+QUANTP+A3SG+P3SG"
            # DOĞRU #
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM$POSTP+PCDAT":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.DATIVE):
                return "POSTP+PCDAT"
            return "ADJ"
            # ikisini, ikisine, fazlasına #
        elif parseString == "ADJ+JUSTLIKE^DB+NOUN+ZERO+A3SG+P2SG$NOUN+ZERO+A3SG+P3SG":
            return "NOUN+ZERO+A3SG+P3SG"
            # kişilerdir, aylardır, yıllardır #
        elif parseString == "A3PL+PNON+NOM^DB+ADV+SINCE$A3PL+PNON+NOM^DB+VERB+ZERO+PRES+COP+A3SG$A3SG+PNON+NOM^DB" \
                            "+VERB+ZERO+PRES+A3PL+COP":
            if root == "yıl" or root == "süre" or root == "zaman" or root == "ay":
                return "A3PL+PNON+NOM^DB+ADV+SINCE"
            else:
                return "A3PL+PNON+NOM^DB+VERB+ZERO+PRES+COP+A3SG"
            # HEP #
        elif parseString == "ADV$PRON+QUANTP+A3SG+P3SG+NOM":
            return "ADV"
            # O #
        elif parseString == "DET$NOUN+PROP+A3SG+PNON+NOM$PRON+DEMONSP+A3SG+PNON+NOM$PRON+PERS+A3SG+PNON+NOM":
            if AutoDisambiguator.isNextWordNoun(index, fsmParses):
                return "DET"
            else:
                return "PRON+PERS+A3SG+PNON+NOM"
            # yapmalıyız, etmeliyiz, alınmalıdır #
        elif parseString == "POS+NECES$POS^DB+NOUN+INF2+A3SG+PNON+NOM^DB+ADJ+WITH^DB+VERB+ZERO+PRES":
            return "POS+NECES"
            # kızdı, çekti, bozdu #
        elif parseString == "ADJ^DB+VERB+ZERO$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO$VERB+POS":
            return "VERB+POS"
            # BİZİMLE #
        elif parseString == "NOUN+A3SG+P1SG$PRON+PERS+A1PL+PNON":
            return "PRON+PERS+A1PL+PNON"
            # VARDIR #
        elif parseString == "ADJ^DB+VERB+ZERO+PRES+COP+A3SG$VERB^DB+VERB+CAUS+POS+IMP+A2SG":
            return "ADJ^DB+VERB+ZERO+PRES+COP+A3SG"
            # Mİ #
        elif parseString == "NOUN+A3SG+PNON+NOM$QUES+PRES+A3SG":
            return "QUES+PRES+A3SG"
            # BENİM #
        elif parseString == "NOUN+A3SG+P1SG+NOM$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A1SG$PRON+PERS+A1SG+PNON" \
                            "+GEN$PRON+PERS+A1SG+PNON+NOM^DB+VERB+ZERO+PRES+A1SG":
            return "PRON+PERS+A1SG+PNON+GEN"
            # SUN #
        elif parseString == "NOUN+PROP+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            return "NOUN+PROP+A3SG+PNON+NOM"
        elif parseString == "ADJ+JUSTLIKE$NOUN+ZERO+A3SG+P3SG+NOM$NOUN+ZERO^DB+ADJ+ALMOST":
            return "NOUN+ZERO+A3SG+P3SG+NOM"
            # düşündük, ettik, kazandık #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PAST+A1PL$VERB+POS+PAST+A1PL$VERB+POS^DB+ADJ+PASTPART" \
                            "+PNON$VERB+POS^DB+NOUN+PASTPART+A3SG+PNON+NOM":
            return "VERB+POS+PAST+A1PL"
            # komiktir, eksiktir, mevcuttur, yoktur #
        elif parseString == "ADJ^DB+VERB+ZERO+PRES+COP+A3SG$NOUN+A3SG+PNON+NOM^DB+ADV+SINCE$NOUN+A3SG+PNON+NOM^DB" \
                            "+VERB+ZERO+PRES+COP+A3SG":
            return "ADJ^DB+VERB+ZERO+PRES+COP+A3SG"
            # edeceğim, ekeceğim, koşacağım, gideceğim, savaşacağım, olacağım  #
        elif parseString == "POS+FUT+A1SG$POS^DB+ADJ+FUTPART+P1SG$POS^DB+NOUN+FUTPART+A3SG+P1SG+NOM":
            return "POS+FUT+A1SG"
            # A #
        elif parseString == "ADJ$INTERJ$NOUN+PROP+A3SG+PNON+NOM":
            return "NOUN+PROP+A3SG+PNON+NOM"
            # BİZİ #
        elif parseString == "NOUN+A3SG+P3SG+NOM$NOUN+A3SG+PNON+ACC$PRON+PERS+A1PL+PNON+ACC":
            return "PRON+PERS+A1PL+PNON+ACC"
            # BİZİM #
        elif parseString == "NOUN+A3SG+P1SG+NOM$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A1SG$PRON+PERS+A1PL+PNON" \
                            "+GEN$PRON+PERS+A1PL+PNON+NOM^DB+VERB+ZERO+PRES+A1SG":
            return "PRON+PERS+A1PL+PNON+GEN"
            # erkekler, kadınlar, madenler, uzmanlar#
        elif parseString == "ADJ^DB+VERB+ZERO+PRES+A3PL$NOUN+A3PL+PNON+NOM$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES" \
                            "+A3PL$NOUN+PROP+A3PL+PNON+NOM":
            return "NOUN+A3PL+PNON+NOM"
            # TABİ #
        elif parseString == "ADJ$INTERJ":
            return "ADJ"
        elif parseString == "AOR+A2PL$AOR^DB+ADJ+ZERO^DB+ADJ+JUSTLIKE^DB+NOUN+ZERO+A3SG+P2PL+NOM":
            return "AOR+A2PL"
            # ayın, düşünün#
        elif parseString == "NOUN+A3SG+P2SG+NOM$NOUN+A3SG+PNON+GEN$VERB+POS+IMP+A2PL":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "VERB+POS+IMP+A2PL"
            return "NOUN+A3SG+PNON+GEN"
            # ödeyecekler, olacaklar #
        elif parseString == "POS+FUT+A3PL$POS^DB+NOUN+FUTPART+A3PL+PNON+NOM":
            return "POS+FUT+A3PL"
            # 9:30'daki #
        elif parseString == "P3SG$PNON":
            return "PNON"
            # olabilecek, yapabilecek #
        elif parseString == "ABLE+FUT+A3SG$ABLE^DB+ADJ+FUTPART+PNON":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ABLE^DB+ADJ+FUTPART+PNON"
            return "ABLE+FUT+A3SG"
            # düşmüş duymuş artmış #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+NARR+A3SG$VERB+POS+NARR+A3SG$VERB+POS+NARR^DB+ADJ+ZERO":
            if AutoDisambiguator.isBeforeLastWord(index, fsmParses):
                return "VERB+POS+NARR+A3SG"
            return "VERB+POS+NARR^DB+ADJ+ZERO"
            # BERİ, DIŞARI, AŞAĞI #
        elif parseString == "ADJ$ADV$NOUN+A3SG+PNON+NOM$POSTP+PCABL":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            return "ADV"
            # TV, CD #
        elif parseString == "A3SG+PNON+ACC$PROP+A3SG+PNON+NOM":
            return "A3SG+PNON+ACC"
            # değinmeyeceğim, vermeyeceğim #
        elif parseString == "NEG+FUT+A1SG$NEG^DB+ADJ+FUTPART+P1SG$NEG^DB+NOUN+FUTPART+A3SG+P1SG+NOM":
            return "NEG+FUT+A1SG"
            # görünüşe, satışa, duruşa #
        elif parseString == "POS^DB+NOUN+INF3+A3SG+PNON+DAT$RECIP+POS+OPT+A3SG":
            return "POS^DB+NOUN+INF3+A3SG+PNON+DAT"
            # YILDIR, AYDIR, YOLDUR #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+ADV+SINCE$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+COP+A3SG$VERB^DB" \
                            "+VERB+CAUS+POS+IMP+A2SG":
            if root == "yıl" or root == "ay":
                return "NOUN+A3SG+PNON+NOM^DB+ADV+SINCE"
            else:
                return "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+COP+A3SG"
            # BENİ #
        elif parseString == "NOUN+A3SG+P3SG+NOM$NOUN+A3SG+PNON+ACC$PRON+PERS+A1SG+PNON+ACC":
            return "PRON+PERS+A1SG+PNON+ACC"
            # edemezsin, kanıtlarsın, yapamazsın #
        elif parseString == "AOR+A2SG$AOR^DB+ADJ+ZERO^DB+ADJ+JUSTLIKE^DB+NOUN+ZERO+A3SG+P2SG+NOM":
            return "AOR+A2SG"
            # BÜYÜME, ATAMA, KARIMA, KORUMA, TANIMA, ÜREME #
        elif parseString == "NOUN+A3SG+P1SG+DAT$VERB+NEG+IMP+A2SG$VERB+POS^DB+NOUN+INF2+A3SG+PNON+NOM":
            if root == "karı":
                return "NOUN+A3SG+P1SG+DAT"
            return "VERB+POS^DB+NOUN+INF2+A3SG+PNON+NOM"
            # HANGİ #
        elif parseString == "ADJ$PRON+QUESP+A3SG+PNON+NOM":
            if lastWord == "?":
                return "PRON+QUESP+A3SG+PNON+NOM"
            return "ADJ"
            # GÜCÜNÜ, GÜCÜNÜN, ESASINDA #
        elif parseString == "ADJ^DB+NOUN+ZERO+A3SG+P2SG$ADJ^DB+NOUN+ZERO+A3SG+P3SG$NOUN+A3SG+P2SG$NOUN+A3SG+P3SG":
            return "NOUN+A3SG+P3SG"
            # YILININ, YOLUNUN, DİLİNİN #
        elif parseString == "NOUN+A3SG+P2SG+GEN$NOUN+A3SG+P3SG+GEN$VERB^DB+VERB+PASS+POS+IMP+A2PL":
            return "NOUN+A3SG+P3SG+GEN"
            # ÇIKARDI #
        elif parseString == "VERB+POS+AOR$VERB^DB+VERB+CAUS+POS":
            return "VERB+POS+AOR"
            # sunucularımız, rakiplerimiz, yayınlarımız #
        elif parseString == "P1PL+NOM$P1SG+NOM^DB+VERB+ZERO+PRES+A1PL":
            return "P1PL+NOM"
            # etmiştir, artmıştır, düşünmüştür, alınmıştır #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+NARR+A3SG+COP$VERB+POS+NARR+COP+A3SG":
            return "VERB+POS+NARR+COP+A3SG"
            # hazırlandı, yuvarlandı, temizlendi #
        elif parseString == "VERB+REFLEX$VERB^DB+VERB+PASS":
            return "VERB^DB+VERB+PASS"
            # KARA, ÇEK, SOL, KOCA #
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM$NOUN+PROP+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            if index > 0:
                if fsmParses[index].getFsmParse(0).isCapitalWord():
                    return "NOUN+PROP+A3SG+PNON+NOM"
                return "ADJ"
            # YÜZ #
        elif parseString == "NOUN+A3SG+PNON+NOM$NUM+CARD$VERB+POS+IMP+A2SG":
            if AutoDisambiguator.isNextWordNum(index, fsmParses):
                return "NUM+CARD"
            return "NOUN+A3SG+PNON+NOM"
        elif parseString == "ADJ+AGT^DB+ADJ+JUSTLIKE$NOUN+AGT+A3SG+P3SG+NOM$NOUN+AGT^DB+ADJ+ALMOST":
            return "NOUN+AGT+A3SG+P3SG+NOM"
            # artışın, düşüşün, yükselişin#
        elif parseString == "POS^DB+NOUN+INF3+A3SG+P2SG+NOM$POS^DB+NOUN+INF3+A3SG+PNON+GEN$RECIP+POS+IMP+A2PL":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "POS^DB+NOUN+INF3+A3SG+P2SG+NOM"
            return "POS^DB+NOUN+INF3+A3SG+PNON+GEN"
            # VARSA #
        elif parseString == "ADJ^DB+VERB+ZERO+COND$VERB+POS+DESR":
            return "ADJ^DB+VERB+ZERO+COND"
            # DEK #
        elif parseString == "NOUN+A3SG+PNON+NOM$POSTP+PCDAT":
            return "POSTP+PCDAT"
            # ALDIK #
        elif parseString == "ADJ^DB+VERB+ZERO+PAST+A1PL$VERB+POS+PAST+A1PL$VERB+POS^DB+ADJ+PASTPART+PNON$VERB+POS^DB" \
                            "+NOUN+PASTPART+A3SG+PNON+NOM":
            return "VERB+POS+PAST+A1PL"
            # BİRİNİN, BİRİNE, BİRİNİ, BİRİNDEN #
        elif parseString == "ADJ^DB+NOUN+ZERO+A3SG+P2SG$ADJ^DB+NOUN+ZERO+A3SG+P3SG$NUM+CARD^DB+NOUN+ZERO+A3SG" \
                            "+P2SG$NUM+CARD^DB+NOUN+ZERO+A3SG+P3SG":
            return "NUM+CARD^DB+NOUN+ZERO+A3SG+P3SG"
            # ARTIK #
        elif parseString == "ADJ$ADV$NOUN+A3SG+PNON+NOM$NOUN+PROP+A3SG+PNON+NOM":
            return "ADV"
            # BİRİ #
        elif parseString == "ADJ^DB+NOUN+ZERO+A3SG+P3SG+NOM$ADJ^DB+NOUN+ZERO+A3SG+PNON+ACC$NUM+CARD^DB+NOUN+ZERO+A3SG" \
                            "+P3SG+NOM$NUM+CARD^DB+NOUN+ZERO+A3SG+PNON+ACC":
            return "NUM+CARD^DB+NOUN+ZERO+A3SG+P3SG+NOM"
            # DOĞRU #
        elif parseString == "ADJ$NOUN+A3SG+PNON+NOM$NOUN+PROP+A3SG+PNON+NOM$POSTP+PCDAT":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.DATIVE):
                return "POSTP+PCDAT"
            return "ADJ"
            # demiryolları, havayolları, milletvekilleri #
        elif parseString == "P3PL+NOM$P3SG+NOM$PNON+ACC":
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "P3PL+NOM"
            return "P3SG+NOM"
            # GEREK #
        elif parseString == "CONJ$NOUN+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            if AutoDisambiguator.containsTwoNeOrYa(fsmParses, "gerek"):
                return "CONJ"
            return "NOUN+A3SG+PNON+NOM"
            # bilmediğiniz, sevdiğiniz, kazandığınız #
        elif parseString == "ADJ+PASTPART+P2PL$NOUN+PASTPART+A3SG+P2PL+NOM$NOUN+PASTPART+A3SG+PNON+GEN^DB+VERB+ZERO" \
                            "+PRES+A1PL":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+PASTPART+P2PL"
            return "NOUN+PASTPART+A3SG+P2PL+NOM"
            # yapabilecekleri, edebilecekleri, sunabilecekleri #
        elif parseString == "ADJ+FUTPART+P3PL$NOUN+FUTPART+A3PL+P3PL+NOM$NOUN+FUTPART+A3PL+P3SG+NOM$NOUN+FUTPART+A3PL" \
                            "+PNON+ACC$NOUN+FUTPART+A3SG+P3PL+NOM":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+FUTPART+P3PL"
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "NOUN+FUTPART+A3SG+P3PL+NOM"
            return "NOUN+FUTPART+A3PL+P3SG+NOM"
            # KİM #
        elif parseString == "NOUN+PROP$PRON+QUESP":
            if lastWord == "?":
                return "PRON+QUESP"
            return "NOUN+PROP"
            # ALINDI #
        elif parseString == "ADJ^DB+NOUN+ZERO+A3SG+P2SG+NOM^DB+VERB+ZERO$ADJ^DB+NOUN+ZERO+A3SG+PNON+GEN^DB+VERB" \
                            "+ZERO$VERB^DB+VERB+PASS+POS":
            return "VERB^DB+VERB+PASS+POS"
            # KIZIM #
        elif parseString == "ADJ^DB+VERB+ZERO+PRES+A1SG$NOUN+A3SG+P1SG+NOM$NOUN+A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A1SG":
            return "NOUN+A3SG+P1SG+NOM"
            # etmeliydi, yaratmalıydı #
        elif parseString == "POS+NECES$POS^DB+NOUN+INF2+A3SG+PNON+NOM^DB+ADJ+WITH^DB+VERB+ZERO":
            return "POS+NECES"
            # HERKESİN #
        elif parseString == "NOUN+A3SG+P2SG+NOM$NOUN+A3SG+PNON+GEN$PRON+QUANTP+A3PL+P3PL+GEN":
            return "PRON+QUANTP+A3PL+P3PL+GEN"
        elif parseString == "ADJ+JUSTLIKE^DB+NOUN+ZERO+A3SG+P2SG$ADJ+JUSTLIKE^DB+NOUN+ZERO+A3SG+PNON$NOUN+ZERO+A3SG" \
                            "+P3SG":
            return "NOUN+ZERO+A3SG+P3SG"
            # milyarlık, milyonluk, beşlik, ikilik #
        elif parseString == "NESS+A3SG+PNON+NOM$ZERO+A3SG+PNON+NOM^DB+ADJ+FITFOR":
            return "ZERO+A3SG+PNON+NOM^DB+ADJ+FITFOR"
            # alınmamaktadır, koymamaktadır #
        elif parseString == "NEG+PROG2$NEG^DB+NOUN+INF+A3SG+PNON+LOC^DB+VERB+ZERO+PRES":
            return "NEG+PROG2"
            # HEPİMİZ #
        elif parseString == "A1PL+P1PL+NOM$A3SG+P3SG+GEN^DB+VERB+ZERO+PRES+A1PL":
            return "A1PL+P1PL+NOM"
            # KİMSENİN #
        elif parseString == "NOUN+A3SG+P2SG$NOUN+A3SG+PNON$PRON+QUANTP+A3SG+P3SG":
            return "PRON+QUANTP+A3SG+P3SG"
            # GEÇMİŞ, ALMIŞ, VARMIŞ #
        elif parseString == "ADJ^DB+VERB+ZERO+NARR+A3SG$VERB+POS+NARR+A3SG$VERB+POS+NARR^DB+ADJ+ZERO":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "VERB+POS+NARR^DB+ADJ+ZERO"
            return "VERB+POS+NARR+A3SG"
            # yapacağınız, konuşabileceğiniz, olacağınız #
        elif parseString == "ADJ+FUTPART+P2PL$NOUN+FUTPART+A3SG+P2PL+NOM$NOUN+FUTPART+A3SG+PNON+GEN^DB+VERB+ZERO+PRES" \
                            "+A1PL":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+FUTPART+P2PL"
            return "NOUN+FUTPART+A3SG+P2PL+NOM"
            # YILINA, DİLİNE, YOLUNA #
        elif parseString == "NOUN+A3SG+P2SG+DAT$NOUN+A3SG+P3SG+DAT$VERB^DB+VERB+PASS+POS+OPT+A3SG":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "NOUN+A3SG+P2SG+DAT"
            return "NOUN+A3SG+P3SG+DAT"
            # MİSİN, MİYDİ, MİSİNİZ #
        elif parseString == "NOUN+A3SG+PNON+NOM^DB+VERB+ZERO$QUES":
            return "QUES"
            # ATAKLAR, GÜÇLER, ESASLAR #
        elif parseString == "ADJ^DB+NOUN+ZERO+A3PL+PNON+NOM$ADJ^DB+VERB+ZERO+PRES+A3PL$NOUN+A3PL+PNON+NOM$NOUN+A3SG" \
                            "+PNON+NOM^DB+VERB+ZERO+PRES+A3PL":
            return "NOUN+A3PL+PNON+NOM"
        elif parseString == "A3PL+P3SG$A3SG+P3PL$PROP+A3PL+P3PL":
            return "PROP+A3PL+P3PL"
            # pilotunuz, suçunuz, haberiniz #
        elif parseString == "P2PL+NOM$PNON+GEN^DB+VERB+ZERO+PRES+A1PL":
            return "P2PL+NOM"
            # yıllarca, aylarca, düşmanca #
        elif parseString == "ADJ+ASIF$ADV+LY":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ+ASIF"
            return "ADV+LY"
            # gerçekçi, alıcı #
        elif parseString == "ADJ^DB+NOUN+AGT+A3SG+PNON+NOM$NOUN+A3SG+PNON+NOM^DB+ADJ+AGT":
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "NOUN+A3SG+PNON+NOM^DB+ADJ+AGT"
            return "ADJ^DB+NOUN+AGT+A3SG+PNON+NOM"
            # havayollarına, gözyaşlarına #
        elif parseString == "P2SG$P3PL$P3SG":
            if AutoDisambiguator.isAnyWordSecondPerson(index, correctParses):
                return "P2SG"
            if AutoDisambiguator.isPossessivePlural(index, correctParses):
                return "P3PL"
            return "P3SG"
            # olun, kurtulun, gelin #
        elif parseString == "VERB+POS+IMP+A2PL$VERB^DB+VERB+PASS+POS+IMP+A2SG":
            return "VERB+POS+IMP+A2PL"
        elif parseString == "ADJ+JUSTLIKE^DB$NOUN+ZERO+A3SG+P3SG+NOM^DB":
            return "NOUN+ZERO+A3SG+P3SG+NOM^DB"
            # oluşmaktaydı, gerekemekteydi #
        elif parseString == "POS+PROG2$POS^DB+NOUN+INF+A3SG+PNON+LOC^DB+VERB+ZERO":
            return "POS+PROG2"
            # BERABER #
        elif parseString == "ADJ$ADV$POSTP+PCINS":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.INSTRUMENTAL):
                return "POSTP+PCINS"
            if AutoDisambiguator.isNextWordNounOrAdjective(index, fsmParses):
                return "ADJ"
            return "ADV"
            # BİN, KIRK #
        elif parseString == "NUM+CARD$VERB+POS+IMP+A2SG":
            return "NUM+CARD"
            # ÖTE #
        elif parseString == "NOUN+A3SG+PNON+NOM$POSTP+PCABL":
            if AutoDisambiguator.hasPreviousWordTag(index, correctParses, MorphologicalTag.ABLATIVE):
                return "POSTP+PCABL"
            return "NOUN+A3SG+PNON+NOM"
            # BENİMLE #
        elif parseString == "NOUN+A3SG+P1SG$PRON+PERS+A1SG+PNON":
            return "PRON+PERS+A1SG+PNON"
            # Accusative and Ablative Cases#
        elif parseString == "ADV+WITHOUTHAVINGDONESO$NOUN+INF2+A3SG+PNON+ABL":
            return "ADV+WITHOUTHAVINGDONESO"
        elif parseString == "ADJ^DB+NOUN+ZERO+A3SG+P3SG+NOM$ADJ^DB+NOUN+ZERO+A3SG+PNON+ACC$NOUN+A3SG+P3SG+NOM$NOUN" \
                            "+A3SG+PNON+ACC":
            return "ADJ^DB+NOUN+ZERO+A3SG+P3SG+NOM"
        elif parseString == "P3SG+NOM$PNON+ACC":
            if fsmParses[index].getFsmParse(0).getFinalPos() == "PROP":
                return "PNON+ACC"
            else:
                return "P3SG+NOM"
        elif parseString == "A3PL+PNON+NOM$A3SG+PNON+NOM^DB+VERB+ZERO+PRES+A3PL":
            return "A3PL+PNON+NOM"
        elif parseString == "ADV+SINCE$VERB+ZERO+PRES+COP+A3SG":
            if root == "yıl" or root == "süre" or root == "zaman" or root == "ay":
                return "ADV+SINCE"
            else:
                return "VERB+ZERO+PRES+COP+A3SG"
        elif parseString == "CONJ$VERB+POS+IMP+A2SG":
            return "CONJ"
        elif parseString == "NEG+IMP+A2SG$POS^DB+NOUN+INF2+A3SG+PNON+NOM":
            return "POS^DB+NOUN+INF2+A3SG+PNON+NOM"
        elif parseString == "NEG+OPT+A3SG$POS^DB+NOUN+INF2+A3SG+PNON+DAT":
            return "POS^DB+NOUN+INF2+A3SG+PNON+DAT"
        elif parseString == "NOUN+A3SG+P3SG+NOM$NOUN^DB+ADJ+ALMOST":
            return "NOUN+A3SG+P3SG+NOM"
        elif parseString == "ADJ$VERB+POS+IMP+A2SG":
            return "ADJ"
        elif parseString == "NOUN+A3SG+PNON+NOM$VERB+POS+IMP+A2SG":
            return "NOUN+A3SG+PNON+NOM"
        elif parseString == "INF2+A3SG+P3SG+NOM$INF2^DB+ADJ+ALMOST$":
            return "INF2+A3SG+P3SG+NOM"
        return None

    def caseDisambiguator(index: int, fsmParses: list, correctParses: list) -> FsmParse:
        fsmParseList = fsmParses[index]
        defaultCase = AutoDisambiguator.selectCaseForParseString(fsmParses[index].parsesWithoutPrefixAndSuffix(), index,
                                                                 fsmParses, correctParses)
        if defaultCase is not None:
            for i in range(fsmParseList.size()):
                fsmParse = fsmParseList.getFsmParse(i)
                if defaultCase in fsmParse.transitionList():
                    return fsmParse
        return None
