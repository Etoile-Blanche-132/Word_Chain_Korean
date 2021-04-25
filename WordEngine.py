from Dataset import WordData

class WordEngine:
    def __init__(self) -> None:
        self.wordData = WordData()
        self.reset()

    def getWord(self, mode: str, frontChar: str) -> str:
        def getAtkWord(frontChar: str) -> str:
            if frontChar in self.atkWordDict.keys() and len(self.atkWordDict) > 0:
                word = self.atkWordDict[frontChar][0]
                print('get: ', word)

                del self.atkWordDict[frontChar][0]

                return word

        def getLongWord(frontChar: str) -> str:
            if frontChar in self.longWordDict.keys() and len(self.longWordDict) > 0:
                word = self.longWordDict[frontChar][0]
                print('get: ', word)

                del self.longWordDict[frontChar][0]

                return word

        if mode == "atk":
            return getAtkWord(frontChar)
        elif mode == 'long':
            return getLongWord(frontChar)
        else:
            return 'Wrong Mode!'

    def reset(self) -> None:
        self.atkWordDict, self.longWordDict = self.wordData.loadData()

        print("reset words")