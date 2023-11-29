import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from jwcATK.ProjectUtils import PlainJsonReader
from MessApis import *

class GenshinGrabber:
    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.reader = PlainJsonReader("properties.json")
        self.session = requests.session()

    def grabBasicRoleInfo(self):
        self.chrome.get(self.reader.read("base_url") + "/角色")
        return self.chrome.page_source

    def __imageDownload(self, src, session: requests.Session, name: str, kind: str):
        content = session.get(src).content
        with open(self.reader.read(kind) + name + ".png", "wb+") as f:
            f.write(content)
            f.close()

    def roleSplit(self, paseSource):
        soup = BeautifulSoup(paseSource, "lxml")
        roles = soup.select(".g")
        for i in roles:
            n = i.select(".L")[0].string
            self.__imageDownload(i.select("a img")[0]["src"], self.session, n, "avatar_storage")


if __name__ == '__main__':
    g = GenshinGrabber()
    g.roleSplit(g.grabBasicRoleInfo())
