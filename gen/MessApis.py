import re

import requests

from jwcATK.ProjectUtils import StringBuilder
import bs4
from grabBasic import copy_and_rename_file


# 解析基本词条
def parseBasicInfo(htmlSource: bs4.Tag):
    retDict = {
        "designation": None,
        "full_name": None,
        "country": None,
        "rarity": None,
        "frequent": None,
        "character": None,
        "weapon": None,
        "initial_power": None,
        "constellation": None,
        "gender": None,
        "race": None,
        "speciality": None,
        "online_date": None,
        "tags": None,
        "simple_introduce": None
    }
    table = htmlSource.select(".wikitable")[0]
    for row in table.find_all('tr'):
        tHead = row.find("th")
        if tHead.string is not None:
            if tHead.string.replace(" ", "").replace("\n", "") == '称号':
                retDict['designation'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '全名/本名':
                retDict['full_name'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '所在国家':
                retDict['country'] = row.select("td a")[1].string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '稀有度':
                retDict['rarity'] = row.select("td img")[0]["alt"][0]
            elif tHead.string.replace(" ", "").replace("\n", "") == '常驻/限定':
                retDict['frequent'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "")[:-1] == '神之':
                retDict['character'] = re.findall("<td>(.+?)<span", str(row))[0]
            elif tHead.string.replace(" ", "").replace("\n", "") == '武器类型':
                retDict['weapon'] = re.findall("<td>(.+?)<span", str(row))[0]
            elif tHead.string.replace(" ", "").replace("\n", "") == '始基力':
                retDict['initial_power'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '命之座':
                try:
                    retDict['constellation'] = re.sub("<span>.+?</span>", "",
                                                      str(row.find("td")).replace("\n", "").replace(" ", ""))
                    retDict['constellation'] = re.sub("<.+?>", "", retDict['constellation'])
                except:
                    retDict['constellation'] = re.sub("<.+?>", "", str(row.find("td")))
                retDict["constellation"] = re.findall('(^.+?座)', retDict["constellation"])[0]
            elif tHead.string.replace(" ", "").replace("\n", "") == '性别':
                retDict['gender'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '种族':
                try:
                    retDict['race'] = re.findall("td>(.+?)</td", str(row).replace("\n", ""))[0].replace("\n", "")
                except:
                    retDict['race'] = ''
            elif tHead.string.replace(" ", "").replace("\n", "") == '特殊料理':
                try:
                    retDict['speciality'] = row.select("td a")[1].string.replace("\n", '')
                except:
                    retDict['speciality'] = ''
                # retDict['speciality'] = row.select("td a")[1].string if row.find("td").string.replace("\n", "") != "" else ''
            elif tHead.string.replace(" ", "").replace("\n", "") == '实装日期':
                retDict['online_date'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == 'TAG':
                retDict['tags'] = row.find("td").string.replace("\n", "")
            elif tHead.string.replace(" ", "").replace("\n", "") == '介绍':
                try:
                    retDict['simple_introduce'] = row.find("td").find("p").string.replace("\n", "")
                except:
                    retDict['simple_introduce'] = re.sub("<.+?>", "",
                                                         str(row.find("td")).replace(" ", "").replace("\n", ""))

    return retDict


# 解析属性数据
def parseAttributeInfo(htmlSource: bs4.Tag, roleName):
    ret = []
    table = htmlSource.select(".wikitable")[0]
    rows = table.find_all('tr')
    for i in range(len(rows)):
        if i >= 2:
            single = []
            for tds in rows[i].select("td"):
                single.append(tds.string.replace('\n', ''))
            ret.append(single)
    ret[0].insert(2, ret[0][1])
    ret[0].insert(4, ret[0][3])
    ret[0].insert(6, ret[0][5])
    ret[0].insert(8, ret[0][7])
    ret[1].append(ret[0][-1])
    ret[1].append(ret[0][-1])
    for i in ret:
        i.append(roleName)
    return ret


# 解析突破消耗数据
def parseOutbreak(htmlSource, roleName):
    talents = []
    # 突破耗材名称
    upgradeCostNames = []
    # 突破耗材数量
    upgradeCostCounts = []
    # 升级耗材名称
    previousUpgradeCostNames = []
    # 升级耗材数量
    previousUpgradeCostCounts = []
    table = htmlSource.select(".wikitable")[0]
    rows = table.find_all('tr')
    for i in range(len(rows)):
        if i in [0, 3, 5, 7, 10, 12, 14]:
            sbPreUpgradeNames = StringBuilder()
            sbPreUpgradeCosts = StringBuilder()
            trString = str(rows[i]).replace("\n", "").replace(" ", "")
            for cost in re.findall("×(.+?[与万])", trString):
                sbPreUpgradeCosts.add(cost.replace("\xa0", "").replace("与", "") + ",")
            aList = rows[i].select("a")
            for j in range(len(aList)):
                if j in [1, 3]:
                    sbPreUpgradeNames.add(aList[j]["title"] + ",")
            previousUpgradeCostCounts.append(sbPreUpgradeCosts.toString()[:-1])
            previousUpgradeCostNames.append(sbPreUpgradeNames.toString()[:-1])

        elif i in [1, 4, 6, 8, 11, 13]:
            sbUpName = StringBuilder()
            sbUpCost = StringBuilder()
            nums = rows[i].select(".ys-iconLTop")
            names = rows[i].select(".ys-iconLarge")
            for name in names:
                sbUpName.add(name.select("a")[0]["title"] + ",")
            for num in nums:
                sbUpCost.add(num.string.replace("\n", '') + ",")
            upgradeCostNames.append(sbUpName.toString()[:-1])
            upgradeCostCounts.append(sbUpCost.toString()[:-1])

        else:
            talents.append(rows[i].select("a")[1].string.replace("\n", ''))

    grades = [20, 40, 50, 60, 70, 80, 90]
    upgradeCostCounts.append("-")
    upgradeCostNames.append("-")
    tal = []
    roleNames = []
    talIdx = 0
    for i in range(7):
        roleNames.append(roleName)
        if i in [0, 3]:
            tal.append(talents[talIdx])
            talIdx += 1
        else:
            tal.append("-")
    return [grades, upgradeCostNames, upgradeCostCounts, previousUpgradeCostNames, previousUpgradeCostCounts, tal,
            roleNames]


# 解析命座
def parseConstellation(htmlSource, roleName):
    session = requests.session()
    desc = []
    addr = []
    conNames = []
    BASE_STORAGE = "./static/constellation/"
    table = htmlSource.select(".wikitable")[0]
    rows = table.find_all('td')
    roleNames = []
    for i in range(len(rows)):
        tdString = str(rows[i]).replace("\n", "").replace("\xa0", '').replace(" ", '')
        if i % 2:
            tdString = re.sub("<.+?>", "", tdString)
            desc.append(tdString)
            roleNames.append(roleName)
        else:
            name = re.findall("</span>(.+?)</td>", tdString)[0]
            imgName = BASE_STORAGE + name
            conNames.append(name)
            try:
                imgUrl = rows[i].select("img")[0]["src"]
                imageDownload(imgUrl, session, imgName)
            except:
                copy_and_rename_file(".", BASE_STORAGE[:-1], "fail.png", re.findall("</span>(.+?)</td>", tdString)[0])
            addr.append(imgName + ".png")
    return [conNames, desc, addr, roleNames]


# 解析天赋
def parseTalent(htmlSource: bs4.Tag, roleName):
    BASE_STORAGE = "./static/talent/"
    session = requests.session()
    contentList = htmlSource.select(".resp-tab-content")
    attrs = []
    info = []
    for i in range(len(contentList)):
        basicLine = []
        titleDiv = contentList[i].select(".r-skill-title-1")[0]
        titleStr = str(titleDiv).replace("\n", "").replace(" ", "")
        title = re.sub("<.+>", "", re.findall("\xa0\xa0(.+?)</div>", titleStr)[0])
        try:
            skillImageSrc = titleDiv.select("img")[0]["src"]
            imageDownload(skillImageSrc, session, BASE_STORAGE + title)
        except:
            copy_and_rename_file(".", BASE_STORAGE[:-1], "fail.png", title + ".png")

        try:
            description = str(contentList[i].select(".r-skill-bg .r-skill-bg-2 .row .col-sm-9")[0])
            des_content = description.replace(" ", "").replace("\n", "").replace("<br/>", "\n")
            # print(i)
            # print(des_content)
            des_content = re.sub("<.+?>", "", des_content)
            # print(des_content)
        except:
            description = str(contentList[i].select(".r-skill-bg .r-skill-bg-2 .row .col-sm-12")[0])
            des_content = description.replace(" ", "").replace("\n", "").replace("<br/>", "\n")
            # print(i)
            # print(des_content)
            des_content = re.sub("<.+?>", "", des_content)
            # print(des_content)
        basicLine.append(title)
        basicLine.append(BASE_STORAGE + title + ".png")
        basicLine.append(des_content)
        if i in [0, 1, 2]:
            attrTable = contentList[i].select(".wikitable")[0]
            rows = attrTable.find_all('tr')
            tb = []
            for row in rows:
                if row.find_all("td"):
                    if row.find_all("td")[0].string is None:
                        continue
                    else:
                        line = []
                        for cell in row.find_all("td"):
                            line.append(cell.string)
                        line.append(title)
                        tb.append(line)
            if tb:
                attrs += tb
        basicLine.append(roleName)
        info.append(basicLine)
    return info, attrs


# 解析技能升级材料
def parseSkillUpgradeCost(htmlSource: bs4.Tag, roleName):
    grades = []
    skillOCost = []
    skillONames = []
    skillTHCost = []
    skillTHNames = []
    roleNames = []
    table = htmlSource.select(".wikitable")[0]
    rows = table.find_all('tr')
    for i in range(1, len(rows)):
        tds = rows[i].find_all("td")
        roleNames.append(roleName)
        for j in range(len(tds)):
            if j % 2 == 0:
                grades.append(tds[j].string.replace("\n", ""))
            else:
                splitTds = str(tds[j]).split("<br/>")
                skillO = bs4.BeautifulSoup(splitTds[0].replace("<td>", ""), "lxml")
                skillTH = bs4.BeautifulSoup(splitTds[0].replace("</td>", ""), "lxml")
                picIco1 = skillO.select(".ys-iconLarge")
                sbSkillONames = StringBuilder()
                sbSkillOCost = StringBuilder()
                for pic in picIco1:
                    sbSkillONames.add(pic.select("a")[0]["title"] + ",")
                    sbSkillOCost.add(pic.select(".ys-iconLTop")[0].string.replace("\n", "") + ",")
                skillONames.append(sbSkillONames.toString()[:-1])
                skillOCost.append(sbSkillOCost.toString()[:-1])
                picIco2 = skillTH.select(".ys-iconLarge")
                sbSkillTHName = StringBuilder()
                sbSkillTHCost = StringBuilder()
                for pic in picIco2:
                    sbSkillTHName.add(pic.select("a")[0]["title"] + ",")
                    sbSkillTHCost.add(pic.select(".ys-iconLTop")[0].string.replace("\n", "") + ",")
                skillTHNames.append(sbSkillTHName.toString()[:-1])
                skillTHCost.append(sbSkillTHCost.toString()[:-1])
    grades = orderList(grades)
    grades.pop()
    roleNames *= 2
    roleNames.pop()
    return grades, orderList(skillONames), orderList(skillOCost), orderList(skillTHNames), orderList(
        skillTHCost), roleNames


# 傻逼一样的上面那个表格一定要做成1->2 6->7 这个样子，哪个杀卵写的网页
def orderList(l):
    return [l[i] for i in range(0, len(l), 2)] + [l[i] for i in range(1, len(l), 2)]


def parsePreview(pageSource: bs4.Tag):
    BASE_STORAGE = "./static/preview/"
    src = pageSource.select(".floatnone a img")[0]["src"]
    name = pageSource.select(".floatnone a img")[0]["alt"][:-4]
    imageDownload(src, requests.session(), BASE_STORAGE + name)
    return BASE_STORAGE + name + ".png"


def imageDownload(src, session: requests.Session, name: str):
    content = session.get(src).content
    with open(name + ".png", "wb+") as f:
        f.write(content)
        f.close()
