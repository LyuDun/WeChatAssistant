import json

class jsonManage(object):
    def __init__(self):
        pass

    def writejson(self, filename, data):
        with open(filename, 'w',encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False)

    def readjson(self, filename):
        with open(filename,'r',encoding="utf-8") as f:
            read_dict = json.load(f)
        return read_dict