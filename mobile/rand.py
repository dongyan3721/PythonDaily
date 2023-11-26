import random
import string

def generate_random_string(length):
    letters = string.ascii_letters  # 包含所有字母的字符串
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

def generate_random_digits(length):
    digits = [str(random.randrange(10)) for _ in range(length)]
    random_digits_string = ''.join(digits)
    return random_digits_string

def generateList():
    random_numbers = random.sample(range(15), 3)
    return random_numbers


if __name__=='__main__':
    fp = open("dat.csv", "w")
    fp2 = open("st.csv", "w")
    cour = [
        "算法设计分析", "JavaWeb程序设计", "软件工程", "计算机视觉基础", "人工智能",
        "数字图像处理", "网络安全", "信息论基础", "机器学习", "数据库系统概念(双语)",
        "计算机组成原理", "软件协同设计","分布式计算", "大数据分析", "多媒体技术",
        "项目管理与过程改进", "编译原理", "软件测试", "区块链技术", "嵌入式系统",
        "信息安全", "软件测试", "移动应用开发", "计算机网络", "数据结构A"
        ]
    tea = [
            "袁健", "李锐", "刘亚", "欧广宇", "曹春萍",
            "薛海", "裴颂文", "马立新", "陈庆奎", "赵海燕",
            "张艳", "魏赟", "张冰雪", "赵逢禹", "卢菁"
    ]

    maxCap = 120
    for i in range(25):
        courId = random.randint(0, 1145141) + 10000000
        teaInd = generateList()
        for j in range(3):
            cap = random.randint(1, maxCap)
            fp.write(f"{courId}-0{j+1},{cour[i]},{tea[teaInd[j]]},{cap},3\n")
            for k in range(random.randint(1, int(cap / 2))):
                fp2.write(f"{courId}-0{j+1},{generate_random_digits(10)},{generate_random_string(8)},{generate_random_digits(11)},{random.randint(0, 100)}\n")
    fp.close()
    fp2.close()



