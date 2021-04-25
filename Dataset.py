import pickle
import requests
from bs4 import BeautifulSoup

class WordData:
    def getSoup(self, url : str, params = None) -> BeautifulSoup:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        timeout = 3

        while True:
            try:
                if params != None:
                    response = requests.get(url, headers = header, params = params, timeout = timeout)
                else:
                    response = requests.get(url, headers = header, timeout = timeout)
                break
            except:
                pass

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def isVaild(self, string : str) -> bool:
        UNICODE_KOR_START = 0xAC00
        UNICODE_KOR_END = 0xD7A3
        
        return any([UNICODE_KOR_START <= ord(i) <= UNICODE_KOR_END for i in string])

    def getLongWordNamuwiki(self) -> list:
        USELESS_CHARACTERS = ['♥', '★']
        START_INDEX = 14 # From this point onwards, Namuwiki's Table row (<tr>) not returns the useless data

        wordList = []

        link = "https://namu.wiki/w/%EB%81%84%ED%88%AC/%ED%95%9C%EA%B5%AD%EC%96%B4/%EA%B8%B4%20%EB%8B%A8%EC%96%B4"
        soup = self.getSoup(link)
        wordSource = soup.find_all('tr')[START_INDEX:]

        for word in wordSource:
            try:
                word = word.contents[1].text
                
                for uselessCharacter in USELESS_CHARACTERS:
                    word = word.replace(uselessCharacter, '')

                if self.isVaild(word):
                    wordList.append(word)
            except:
                pass
            
        return wordList

    def getAtkWordNamuwiki(self) -> list:
        USELESS_CHARACTERS = ['♥', '★']
        START_INDEX = 14 # From this point onwards, Namuwiki's Table row (<tr>) not returns the useless data

        wordList = []

        link = "https://namu.wiki/w/%EB%81%84%ED%88%AC/%ED%95%9C%EA%B5%AD%EC%96%B4/%EA%B3%B5%EA%B2%A9%20%EB%B0%8F%20%EB%B0%A9%EC%96%B4%20%EB%8B%A8%EC%96%B4"
        soup = self.getSoup(link)
        wordSource = soup.find_all('tr')[START_INDEX:]
    
        for word in wordSource:
            try:
                word = word.text

                for uselessCharacter in USELESS_CHARACTERS:
                    word = word.replace(uselessCharacter, '')

                if '[' not in word and self.isVaild(word):
                    wordList.append(word)
            except:
                pass
            
        return wordList

    def getLongWordKkukowiki(self) -> list:
        NO_PAPER = '(없는 문서)'
        END_INDEX = -9 # Before this point onwards, KkutuWiki's anchor (<a>) not returns the useless data
        
        wordList = []

        linkList = ["https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%84%B1",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%84%B4",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%84%B7",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%84%B9",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%81",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%82",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%85",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%87",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%88",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%8A",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%8B",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%8C",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%8D",
                    "https://kkukowiki.kr/w/%EA%B8%B4_%EB%8B%A8%EC%96%B4/%ED%95%9C%EA%B5%AD%EC%96%B4/%E3%85%8E"]

        for link in linkList:
            soup = self.getSoup(link)
            wordSource = soup.find_all("a")[:END_INDEX]

            for word in wordSource:
                if "title" in word.attrs.keys():
                    word = word.text.replace(NO_PAPER, "")

                    if self.isVaild(word):
                        wordList.append(word)
                else:
                    continue
                
        return wordList
    
    def saveData(self) -> None:
        def sortByLength(wordDict : dict) -> dict:
            for key in wordDict.keys():
                wordDict[key].sort(key = len, reverse = True)
            
            return wordDict

        def wordClassify(wordList : list) -> dict:
            wordDict = {}

            for word in wordList:
                key = word[0]

                if key in wordDict.keys():
                    wordDict[key].append(word.replace('[한방]', ''))
                else:
                    wordDict[key] = []
                    wordDict[key].append(word.replace('[한방]', ''))

            return wordDict

        namuwikiLongwordList = self.getLongWordNamuwiki()
        namuwikiAtkwordList = self.getAtkWordNamuwiki()
        kkukowikiLongwordList = self.getLongWordKkukowiki()

        atkWordList = namuwikiAtkwordList
        longWordList = list(set(namuwikiLongwordList + kkukowikiLongwordList))

        atkWordDict = wordClassify(atkWordList)
        longWordDict = wordClassify(longWordList)

        atkWordDict = sortByLength(atkWordDict)
        longWordDict = sortByLength(longWordDict)

        with open('.\Data\AttackWords.pickle', 'wb') as fw:
            pickle.dump(atkWordDict, fw)

        with open('.\Data\LongWords.pickle', 'wb') as fw:
            pickle.dump(longWordDict, fw)

    def loadData(self) -> tuple:
        with open('.\Data\AttackWords.pickle', 'rb') as fr:
            atkWordDict = pickle.load(fr)

        with open('.\Data\LongWords.pickle', 'rb') as fr:
            longWordDict = pickle.load(fr)

        return atkWordDict, longWordDict

if __name__ == '__main__': # For test and make files
    WordData = WordData()

    WordData.saveData()