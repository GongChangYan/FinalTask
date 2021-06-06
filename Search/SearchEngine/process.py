import os
import json

def process():
    path = "JSON/"
    num = 0
    dirList = os.listdir("xml_1")
    ls = ["全文", "文首", "标准法院名称", "案件类别", "文书种类", "审判程序", "案件类型", "当事人", "案件基本情况", "裁判分析过程", "判决结果", "文尾"]
    for dir in dirList:
        dir = "xml_1/" + dir
        fileList = os.listdir(dir)
        for filename in fileList:
            if filename.find(".txt") == -1:
                filename = dir + '/' + filename
                input = open(filename, encoding="utf-8").read()
                dic = {}
                for key in ls:
                    loc = input.find("\"" + key + "\"")
                    if loc != -1:
                        begin = input.find("\"", loc + 1)
                        end = input.find("\"", begin + 1)
                        begin = input.find("\"", end + 1)
                        dic[key] = input[end + 1:begin]
                    else:
                        dic[key] = " "
                loc = input.find("FT value=\"")
                laws = ""
                while loc != -1:
                    begin = input.find("\"", loc + 1)
                    end = input.find("\"", begin + 1)
                    laws = laws + " + " + input[begin+1:end]
                    loc = input.find("FT value=\"", end + 1)
                dic["法律法条"] = laws
                print(num)
                output = open(path + str(num) + ".json",encoding="utf-8", mode="w")
                num += 1
                json.dump(dic, output, ensure_ascii=False)
                output.close()

process()
