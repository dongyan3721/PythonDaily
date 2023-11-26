import json
import pandas


def spec2xlsx(filename: str):
    f = open(filename, "r", encoding='utf-8')
    fn = f.read()
    ind = json.loads(fn)
    name = []
    id = []
    dept = []
    for i in ind["enrollments"]:
        name.append(i["user"]["name"])
        id.append(i["user"]["user_no"])
        dept.append(i["user"]["department"]["name"])
    dat = pandas.DataFrame([name, id, dept])
    dat = dat.T
    dat.columns = ["姓名", "学号", "部门"]
    dat.to_excel(f"{filename}.xlsx")
    f.close()


if __name__ == "__main__":
    spec2xlsx("Web.json")
    spec2xlsx("移动应用开发.json")
