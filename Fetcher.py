from bs4 import BeautifulSoup
import requests
from urllib.parse import quote


class WordFetcher():
    def __init__(self, join=";\n"):
        self.ua = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.provider = {}
        self.join = join

        # 必应
        def Bing(word):
            r = requests.get(
                "https://cn.bing.com/dict/clientsearch?mkt=zh-CN&setLang=zh&form=BDVEHC&ClientVer=BDDTV3.5.1.4320&q=" + word, headers=self.ua).text
            soup = BeautifulSoup(r, "lxml")
            Chinese = []
            English = []
            r = soup.find_all(name="div", attrs={"class": "defitemcon"})
            for i in r:
                soup_each = BeautifulSoup(str(i), "lxml")
                cn = soup_each.find(name="span", attrs={
                                    "class": "itemname"}).text
                en = soup_each.find(name="span", attrs={
                                    "class": "itmeval"}).text
                Chinese.append(cn)
                English.append(en)
            Chinese = self.join.join(Chinese)
            English = self.join.join(English)
            return {"Chinese": Chinese, "English": English, "Spelling": word}

        self.provider["Bing"] = Bing

        # 剑桥词典
        def Cambridge(word):
            r = requests.get("https://dictionary.cambridge.org/zhs/%E8%AF%8D%E5%85%B8/%E8%8B%B1%E8%AF%AD-%E6%B1%89%E8%AF%AD-%E7%AE%80%E4%BD%93/" + word + "?q=" + word,
                             headers=self.ua).text
            soup = BeautifulSoup(r, "lxml")
            Chinese = self.join.join([i.text for i in soup.find_all(
                "span", attrs={"class": "trans dtrans dtrans-se break-cj"})])
            English = self.join.join(
                [i.text for i in soup.find_all(name="div", attrs={"class": "def ddef_d db"})])
            return {"Chinese": Chinese, "English": English, "Spelling": word}

        self.provider["Cambridge"] = Cambridge

        # 柯林斯
        def Collins(word):
            r = requests.get(
                "https://www.collinsdictionary.com/zh/dictionary/english-chinese/" + word, headers=self.ua).text
            soup = BeautifulSoup(r, "lxml")
            r = soup.find_all(name="div", attrs={"class": "sense"})
            Chinese = []
            for i in r:
                soup = BeautifulSoup(str(i), "lxml")
                Chinese.append(
                    soup.find("span", attrs={"class": "cit type-translation"}).text)
            Chinese = self.join.join(Chinese)
            English = "N/A"
            return {"Chinese": Chinese, "English": English, "Spelling": word}

        self.provider["Collins"] = Collins
        # 设置默认爬虫
        self.defaultProviderName = list(self.provider.keys())[0]
        self.defaultProvider = self.provider[self.defaultProviderName]

    def fetch(self, word):
        return self.defaultProvider(word)

    def setProvider(self, provider):
        self.defaultProvider = self.provider[provider]
        self.defaultProviderName = provider

    def listProvider(self):
        return list(self.provider.keys())


class PhraseFetcher:
    def __init__(self):
        self.ua = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        self.provider = {}

        def Linggle(phrase):
            phrase = quote(phrase)
            res = requests.get("https://www.linggle.com/api/ngram/" +
                               phrase, headers=self.ua).json()["ngrams"]
            sum = 0
            for i in res:
                sum += i[1]
            return [{"Phrase": i[0], "Frequency": str(format(i[1]/sum*100, '.2f')) + "%", "Count":i[1]} for i in res]
        self.provider["Linggle"] = Linggle

        self.defaultProvider = Linggle
        self.defaultProviderName = "Linggle"

    def fetch(self, phrase):
        return self.defaultProvider(phrase)

    def setProvider(self, provider):
        self.defaultProvider = self.provider[provider]
        self.defaultProviderName = provider

    def listProvider(self):
        return list(self.provider.keys())
