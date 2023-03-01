from flask import Flask, request, abort
from lib.utility import *
import requests
import json

class OpenAIService:
    def __init__(self):
        self.name = "OpenAIService"
        self.user_agent = None
        self.model = ""
        self.temperature = 0
        self.max_tokens = 1000
        self.img_cnt = 2
        self.img_size = "1024x1024"
        self.url = {
            "talk": "https://api.openai.com/v1/completions",
            "img": "https://api.openai.com/v1/images/generations"
        }
        self.host = ""
        self.port = None
        self.is_init = False
        self.app = Flask(__name__)
        self.app.add_url_rule("/check", methods=['POST'], view_func= self.checkFun) 
        self.app.add_url_rule("/talk", methods=['POST'], view_func= self.talkFun)
        self.app.add_url_rule("/img", methods=['POST'], view_func= self.imgFun)

        self.init()
        
    def init(self):
        try:
            with open('option.json', 'r') as f:
                cfg = json.load(f)
                f.close()
                Log(cfg)
                if self.name not in cfg:
                    return
                if "host" in cfg[self.name]:
                    self.host = cfg[self.name]["host"]
                if "port" in cfg[self.name]:
                    self.port = cfg[self.name]["port"]
                if "key" in cfg[self.name]:
                    self.key = "Bearer " + cfg[self.name]["key"]
                if "talk_url" in cfg[self.name]:
                    self.url["talk"] = cfg[self.name]["talk_url"]
                if "img_url" in cfg[self.name]:
                    self.url["img"] = cfg[self.name]["img_url"]
                if "model" in cfg[self.name]:
                    self.model = cfg[self.name]["model"]
                if "temperature" in cfg[self.name]:
                    self.temperature = cfg[self.name]["temperature"]
                if "max_tokens" in cfg[self.name]:
                    self.max_tokens = cfg[self.name]["max_tokens"]
                if "img_cnt" in cfg[self.name]:
                    self.img_cnt = cfg[self.name]["img_cnt"]
                if "img_size" in cfg[self.name]:
                    self.img_size = cfg[self.name]["img_size"]
                # init ok here
                self.is_init = True
                Log(self.name + " init ok.")
        except:
            Log(self.name + " init eror!")
            return False
        return True
    
    def run(self):
        if self.is_init is False:
            return
        self.app.run(self.host, self.port)
    
    def checkFun(self):
        text = 'check ok!'
        return text
    
    def talkFun(self):
        try:
            data = request.data
            obj = json.loads(data)
            question = obj["question"]
            Log(question)
            user_agent = {
                "Content-Type": "application/json",
                "Authorization": self.key
            }
            url = self.url["talk"]
            data = {
                "model": self.model, 
                "prompt": question, 
                "temperature": self.temperature, 
                "max_tokens": self.max_tokens
            }
            response = requests.post(url, headers= user_agent, data = json.dumps(data))
            if response.status_code == 200:
                response_text = json.loads(response.text)["choices"][0]["text"]
            Log("ChatGPT response={0}".format(response_text))
            return response_text
        except Exception as e:
            Log("action except!:{0}".format(str(e)))
        return "error!"
    
    def imgFun(self):
        try:
            data = request.data
            obj = json.loads(data)
            question = obj["question"]
            Log(question)
            user_agent = {
                "Content-Type": "application/json",
                "Authorization": self.key
            }
            url = self.url["img"]
            data = {
                "prompt": question, 
                "n": self.img_cnt, 
                "size": self.img_size
            }
            response = requests.post(url, headers= user_agent, data = json.dumps(data))
            if response.status_code == 200:
                imgs = []
                for img in json.loads(response.text)["data"]:
                    imgs.append(img["url"])
            Log("ChatGPT response={0}".format(imgs))
            return "{0}".format(imgs)
        except Exception as e:
            Log("action except!:{0}".format(str(e)))
        return "error!"
    