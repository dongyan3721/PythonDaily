from jwcATK.ProjectUtils import PlainJsonReader
import pandas as pd


def exportToExcelIndex(data, index, tableName):
    table = pd.DataFrame(data)
    table.index = index
    table = table.T
    table.to_excel(tableName + ".xlsx")


def exportToExcelColumns(data, columns, tableName):
    table = pd.DataFrame(data)
    table.columns = columns
    table.to_excel(tableName + ".xlsx")



reader = PlainJsonReader("f.json")
methods = reader.read("methods")
twoDem = []
for i in methods:
    for j in range(len(i["scenes"])):
        baseLine = [i["ID"], i["scenes"][j],  i["traffics"][j]]
        twoDem.append(baseLine)

exportToExcelColumns(twoDem, ["ID", "景点", "交通工具"], "出行表")
