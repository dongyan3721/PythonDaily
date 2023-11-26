import random
import time
from ProjectUtils import *


if __name__ == '__main__':
    toSelCourList = []
    while 1:
        ins = input("请输入你要抢的课程号(输入-1结束)")
        if ins == "-1":
            break
        else:
            toSelCourList.append(ins)

    op = None
    while 1:
        op = input("若你想选通识课（不含体育），请输入G，若要选学科基础专业课，请输入C")
        if op != "G" and op != "C":
            print("输入有误！")
            continue
        else:
            break

    provider = CookieProvider()
    cookie = provider.getCookie()
    # print(cookie)
    grabber = ClassGrabber(cookie)
    while 1:
        grabber.grab(toSelCourList, op=op)
        time.sleep(random.randint(2, 5))
