import time

from selenium import webdriver
from bs4 import BeautifulSoup
from MessApis import *
import pandas as pd

# chrome = webdriver.Chrome()

# chrome.get("https://wiki.biligame.com/ys/%E8%BF%AA%E5%B8%8C%E9%9B%85")

# page = chrome.page_source
# print(page)
# cl = BeautifulSoup(page, "lxml")

# resu = cl.select(".poke-bg")[3]

# print(parseBasicInfo(resu))

# print("\n\n")

# print(parsePreview(resu))

# data = pd.DataFrame(parseOutbreak(resu))
# data = data.T
# data.columns = ["等级", "突破需要耗材名称", "突破需要耗材数量",
#                 "升级至该等级需消耗耗材", "升级至该等级约需消耗耗材数量", "解锁天赋"]

# print(data)
# print(resu[0])

# tables = resu[7].select(".wikitable")

# 0, 5

# for i in range(len(tables)):
#     print(i)
#     print(tables[i])

for i in range(1, 16):
    print(f"\"LV{i}\"", end=", ")
while 1:
    time.sleep(10)
    print("000----0000")
