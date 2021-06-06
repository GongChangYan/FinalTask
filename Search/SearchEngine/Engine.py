import json
from elasticsearch import Elasticsearch as ES
import time

def getkey(elem):
    return elem["_score"] 

class Engine():
    def __init__(self):
        engine = ES(["127.0.0.1:9200"])
        mappings = {
            "mappings": {                      
                "properties": {
                    "全文": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    },
                    "文首": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    },
                    "标准法院名称": {                            
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    }, 
                    "案件类别": {                              
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    }, 
                    "文书种类": {                            
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    }, 
                    "审判程序": {                            
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    },
                    "案件类型": {                            
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart"
                    },
                    "当事人": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "analyzer": "ik_smart"
                    },
                    "案件基本情况": {
                        "type": "text", 
                        "index": "false"
                    },
                    "裁判分析过程": {
                        "type": "text",
                        "index": "false"
                    },
                    "判决结果": {
                        "type": "text", 
                        "index": "false"
                    },
                    "文尾": {
                        "type": "text",
                        "analyzer": "ik_max_word"
                    },
                    "法律法条": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart" 
                    }
                }
            }
        }
        # engine.indices.delete("test")
        if engine.indices.exists("test") == False:
            res = engine.indices.create(index="test", body=mappings, ignore=400)
            print(res)
            self.ls = []
            for i in range(0, 500):
                file = open("miniData/" + str(i)+".json", "r", encoding="utf-8")
                js = json.loads(file.read())
                res = engine.index(index="test", id=i, body=js)
                file.close()
            engine.indices.refresh(index="test")
    
    def Search(self, key, target):
        if target == " " or target == "":
            return 0, 0.0, []
        engine = ES(["127.0.0.1:9200"])
        search_body = {
            "query": {
                "match": {
                    key: target
                }
            }
        }
        begin_time = time.time()
        result = engine.search(index="test", body=search_body, size = 10000)
        cost_time = time.time() - begin_time
        num = int(result["hits"]['total']["value"])
        return num, cost_time, result["hits"]["hits"]

    def searchAllText(self, target="浙江"):
        return self.Search("全文", target)

    def searchPerson(self, target="洪德河"):
        return self.Search("当事人", target)

    def searchCaseType(self, target="民事案件"):
        return self.Search("案件类别", target)

    def searchCourt(self, target="晋江市人民法院"):
        return self.Search("标准法院名称", target)
    
    def searchLaw(self, target="中华人民共和国合同法"):
        return self.Search("法律法条", target)
    
    def searchJudge(self, target="陈昌演"):
        return self.Search("文尾", target)

    def searchByID(self, id):
        engine = ES(["127.0.0.1:9200"])
        id = str(id)
        search_body = {
            "query": {
                "ids":{
                    "values":id
                }
            }
        }
        return engine.search(index="test", body=search_body)["hits"]["hits"][0]
    
    def searchSimilarCase(self, id):
        engine = ES(["127.0.0.1:9200"])
        search_body = {
            "query": {
                "more_like_this": {
                    "fields": [
                        "全文"
                    ],
                    "like": [
                        {
                        "_id": str(id)
                        }
                    ]
                }
            }
        }
        result = engine.search(index="test", body=search_body, size = 10)
        return result["hits"]["hits"]
    
    def searchSimilarLaws(self, id):
        engine = ES(["127.0.0.1:9200"])
        search_body = {
            "query": {
                "more_like_this": {
                    "fields": [
                        "法律法条"
                    ],
                    "like": [
                        {
                        "_id": str(id)
                        }
                    ]
                }
            }
        }
        result = engine.search(index="test", body=search_body, size = 10)
        return result["hits"]["hits"]

    '''这里的content为一个列表，长度为6，分别对应全文，当事人，案件类别，标准法院名称，法律法条，文尾六项搜索内容，
    如果内容为空，对应的字符串应该为" "（仅有一个空格）'''
    def fancySearch(self, content):
        # if (content[0] == " "):
        #     print("[ERROR] content[0] for fancy search can't be empty")
        #     return 0, 0.0, []
        num1, time1, res1 = self.Search("全文",content[0])
        num2, time2, res2 = self.Search("当事人",content[1])
        num3, time3, res3 = self.Search("案件类别",content[2])
        num4, time4, res4 = self.Search("标准法院名称",content[3])
        num5, time5, res5 = self.Search("法律法条",content[4])
        num6, time6, res6 = self.Search("文尾",content[5])
        # print(num6)
        set1 = set()
        set2 = set()
        set3 = set()
        set4 = set()
        set5 = set()
        set6 = set()
        for res in res1:
            set1.add(res["_id"])
        for res in res2:
            set2.add(res["_id"])
        for res in res3:
            set3.add(res["_id"])
        for res in res4:
            set4.add(res["_id"])
        for res in res5:
            set5.add(res["_id"])
        for res in res6:
            set6.add(res["_id"])
        s = set1 | set2 | set3 | set4 | set5 | set6
        if len(set1) != 0:
            s = s & set1
        if len(set2) != 0:
            s = s & set2
        if len(set3) != 0:
            s = s & set3
        if len(set4) != 0:
            s = s & set4
        if len(set5) != 0:
            s = s & set5
        if len(set6) != 0:
            s = s & set6 
        result = []
        dic = {}
        for id in s:
            dic[id] = 0
            for res in res1:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            for res in res2:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            for res in res3:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            for res in res4:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            for res in res5:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            for res in res6:
                if res['_id'] == id:
                    dic[id] = max(dic[id], float(res['_id']))
            r = self.searchByID(id)
            r['_score'] = dic[id]
            result.append(r)
        def getScore(ress):
            return ress["_score"]
        result.sort(key=getScore, reverse=True)
        num = len(s)
        time = max(time1, time2, time3, time4, time5, time6)
        return num, time, result


    def getGuideString(self, content):
        begin_time = time.time()
        t, num, res = self.searchAllText(content)
        guideString = set()
        for i in range(0, len(res)):
            if res[i]["_source"]["全文"].find(content) != -1:
                begin = res[i]["_source"]["全文"].find(content)
                end = min(res[i]["_source"]["全文"].find("，", begin),res[i]["_source"]["全文"].find(" ", begin), res[i]["_source"]["全文"].find("。", begin))
                guideString.add(res[i]["_source"]["全文"][begin:end])
        end_time = time.time()
        print(end_time - begin_time)
        result = []
        for s in guideString:
            result.append(s)
        def getLen(ress):
            return len(ress)
        result.sort(key=getLen)
        return result[0:min(10, len(result))]

# engine = Engine()
# num, tim, res = engine.fancySearch(["杭州", "过学超", "", "", "", "章建荣"])
# print(num)
# print(res[0]["_source"]["文尾"])
# print(res[1]["_source"]["文尾"])
def init():
    global _engine
    _engine = Engine()
    print("init")

def getEngine():
    global _engine
    return _engine