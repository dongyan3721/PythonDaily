import os
import shutil
import sqlite3

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jwcATK.ProjectUtils import PlainJsonReader
from MessApis import *


def copy_and_rename_file(source_dir, target_dir, file_name, new_file_name):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    source_file_path = os.path.join(source_dir, file_name)
    target_file_path = os.path.join(target_dir, new_file_name)

    if os.path.exists(source_file_path):
        shutil.copy(source_file_path, target_file_path)
        print(f"File {source_file_path} copied to {target_file_path}")
    else:
        print(f"File {file_name} does not exist in {source_dir}.")


class GenshinGrabber:
    def __init__(self):
        browserOption = Options()
        self.chrome = webdriver.Chrome(browserOption.add_argument("--headless"))
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
        allBasicInfo = []
        allAttributes = []
        allOutBreak = [[], [], [], [], [], [], []]
        allConstellation = [[], [], [], []]
        allTalentInfo = []
        allTalentUpgradeBenefits = []
        allSkillCost = [[], [], [], [], [], []]
        soup = BeautifulSoup(paseSource, "lxml")
        roles = soup.select(".g")
        for i in range(0, 80):
            print(len(roles))
            print(i)
            n = roles[i].select(".L")[0].string.replace("\n", "")
            if n == "派蒙" or n == "旅行者(无)":
                continue
            self.__imageDownload(roles[i].select("a img")[0]["src"], self.session, n, "avatar_storage")
            avatar = "./static/avatar/" + n + ".png"
            self.chrome.get(self.reader.read("base_url")[:-2] + roles[i].select("a")[1]["href"])
            source = BeautifulSoup(self.chrome.page_source, "lxml").select(".poke-bg")
            baseDict = parseBasicInfo(source[0])
            attributes = parseAttributeInfo(source[1], n)
            outBreak = parseOutbreak(source[2], n)
            if n == "旅行者(无)":
                constellations = [[], [], [], []]
            else:
                constellations = parseConstellation(source[6], n)
            talent = parseTalent(source[7], n)
            skillCost = parseSkillUpgradeCost(source[8], n)
            preview = parsePreview(source[3])
            baseDict["avatar"] = avatar
            baseDict["preview"] = preview
            baseDict["name"] = n
            print(baseDict)
            baseList = []
            for key in baseDict.keys():
                baseList.append(baseDict[key])
            allBasicInfo.append(baseList)
            print(attributes)
            allAttributes += attributes
            print(outBreak)
            for j in range(7):
                allOutBreak[j] += outBreak[j]
            print(constellations)
            for j in range(4):
                allConstellation[j] += constellations[j]
            print(talent)
            allTalentInfo += talent[0]
            allTalentUpgradeBenefits += talent[1]
            print(skillCost)
            for j in range(6):
                allSkillCost[j] += skillCost[j]

        exportToExcelColumns(allBasicInfo, ["称号", "全名", "所属国家", "星级", "常驻/限定", "属性",
                                            "武器类型", "始基力", "命座", "性别", "种族", "特殊食材", "上线日期",
                                            "tags", "简介", "头像地址", "立绘地址", "姓名"], "角色基础信息表")
        exportToExcelColumns(allTalentUpgradeBenefits, ['详细属性', "LV1", "LV2", "LV3", "LV4", "LV5", "LV6",
                                                        "LV7", "LV8", "LV9", "LV10", "LV11", "LV12", "LV13",
                                                        "LV14", "LV15", '增益技能名'], "技能升级增益效果表")
        # print(allTalentUpgradeBenefits)
        exportToExcelIndex(allConstellation, ["命座名称", "命座效果", "命座图片", "命座归属人"], "命座表")

        # print(allConstellation)
        exportToExcelColumns(allAttributes, ['等级', '突破前生命上限', '突破后生命上限', '突破前攻击力上限',
                                             '突破后攻击力上限', '突破前防御力上限', "突破后防御力上限",
                                             '突破前元素伤害加成', '突破后元素伤害加成', '突破人'], '属性信息表')
        # print(allAttributes)
        exportToExcelIndex(allSkillCost, [
            '技能升级区间', '一技能升级消耗物品种类', '一技能升级消耗物品数量',
            '二三仅能升级消耗物品种类', '二三技能升级消耗物品数量', '技能升级人'
        ], "技能升级消耗表")
        # print(allSkillCost)
        exportToExcelColumns(allTalentInfo, [
            '天赋名', "天赋图", "天赋描述", "天赋持有人"
        ], "天赋表")
        # print(allTalentInfo)
        exportToExcelIndex(allOutBreak, [
            '突破等级', "突破消耗资源种类", "突破消耗资源数量",
            "前一突破等级升级至现等级消耗资源类型", "前一突破等级升级至现等级消耗资源数量(约)", '突破解锁天赋', '突破人'
        ], "突破资源消耗表")
        # print(allOutBreak)


def exportToExcelColumns(data, columns, tableName):
    conn = sqlite3.connect("gen_shin")
    table = pd.DataFrame(data)
    table.columns = columns
    table.to_excel(tableName + ".xlsx")
    table.to_sql(tableName, conn, index=False, if_exists="replace")


def exportToExcelIndex(data, index, tableName):
    conn = sqlite3.connect("gen_shin")
    table = pd.DataFrame(data)
    table.index = index
    table = table.T
    table.to_excel(tableName + ".xlsx")
    table.to_sql(tableName, conn, index=False, if_exists="replace")


if __name__ == '__main__':
    g = GenshinGrabber()
    g.roleSplit(g.grabBasicRoleInfo())
