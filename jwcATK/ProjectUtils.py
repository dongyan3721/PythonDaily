"""
运行环境
selenium 4.12.0
requests 2.31.0
"""
import io
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


# 工具类，构建字符串
class StringBuilder:
    def __init__(self):
        self.sb = io.StringIO()

    # 元素添加
    def add(self, val):
        self.sb.write(val)

    # 转字符串
    def toString(self) -> str:
        return self.sb.getvalue()

    def clear(self):
        self.sb = io.StringIO()


# 工具类，单嵌套json阅读器
class PlainJsonReader:
    def __init__(self, filename: str):
        file = open(filename, "r", encoding="UTF-8")
        file_cont = file.read()
        self.reader = json.loads(file_cont)
        file.close()

    def read(self, key: str):
        return self.reader[key]


# 启动selenium模块，提供cookie数据
class CookieProvider:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.reader = PlainJsonReader("properties.json")

    def getCookie(self):
        self.browser.get(self.reader.read("login_interface"))
        self.browser.find_element(by=By.ID, value="username").send_keys(self.reader.read("user_id"))
        self.browser.find_element(by=By.ID, value="password").send_keys(self.reader.read("user_pwd"))
        self.browser.find_element(by=By.CLASS_NAME, value="auth_login_btn").click()
        self.browser.get(self.reader.read("cour_sel_interface"))
        self.browser.refresh()
        sb = StringBuilder()
        for item in reversed(self.browser.get_cookies()):
            sb.add(item["name"])
            sb.add("=")
            sb.add(item["value"])
            sb.add("; ")

        return sb.toString()[:-2]


# 课程实体类，记录发送请求必须的三个属性
class CourseSelectorDataProvider:
    def __init__(self, kch_id, kch, jxbmc):
        self.kch_id = kch_id
        self.kch = kch
        self.jxbmc = jxbmc

    def toString(self):
        sb = StringBuilder()
        sb.add("CourseSelectorDataProvider{")
        sb.add("kch_id=" + self.kch_id)
        sb.add("kch=" + self.kch)
        sb.add("jxbmc=" + self.jxbmc)
        sb.add("}")
        return sb.toString()


# 选课类，支持完成选课操作
class ClassGrabber:
    def __init__(self, cookie):
        self.session = requests.session()
        self.reader = PlainJsonReader("properties.json")
        preHeader = self.reader.read("general_request_header")
        preHeader["Cookie"] = cookie
        self.headers = preHeader

        # 获取选课所使用的教学班id

    def __getJxbId(self, info: CourseSelectorDataProvider):
        dat = self.reader.read("query_single_jxb_id_dat")
        dat["filter_list[0]"] = info.jxbmc
        dat["kch_id"] = info.kch_id
        resp = self.session.post(url=self.reader.read("get_jxb_id_url"), headers=self.headers,
                                 data=dat).json()
        # time.sleep(2)
        return resp[0]["do_jxb_id"]

    # 选课操作函数
    def grab(self, targetClassIndexList: list, op):
        containList = []
        getAvailableCour_dat = None

        # G = general 通识， C = core 核心
        if op == "G":
            getAvailableCour_dat = self.reader.read("query_all_available_from_data_general")
        else:
            getAvailableCour_dat = self.reader.read("query_all_available_from_data_core")

        resp_available_jxb = self.session.post(url=self.reader.read("query_all_available_url"), headers=self.headers,
                                               data=getAvailableCour_dat).json()
        # 本次查询所获得的有余量的课程
        print(resp_available_jxb)
        resp_available_jxb = resp_available_jxb["tmpList"]
        # 这个设置的延迟酌情取消
        # time.sleep(2)

        # 检测要的课在不在可选课程里面
        for traCls in targetClassIndexList:
            for cls in resp_available_jxb:
                if traCls in cls["jxbmc"]:
                    t = CourseSelectorDataProvider(cls["kch_id"], cls["kch"], cls["jxbmc"])
                    containList.append(t)
                    targetClassIndexList.remove(traCls)

        # 没课能选就直接开始下一次查询
        if len(containList) == 0:
            print("你要的课都没有余量")
            return
        # 拿选课表单数据
        sel_data = self.reader.read("sel_cour_dat")

        for co in containList:
            doJxbId = self.__getJxbId(co)
            sel_data["jxb_ids"] = doJxbId
            sel_data["kch_id"] = co.kch_id
            print(co.toString())
            print("jxbid=" + doJxbId)
            # 最终的选课操作
            finalResp = self.session.post(url=self.reader.read("sel_cour_url"), headers=self.headers,
                                          data=sel_data)
            print(finalResp.json())
    # def grabAllAvailable(self):
