import requests
from dotenv import load_dotenv
import os 
import json

# load .env
load_dotenv()
APP_KEY=os.environ.get("APP_KEY")
APP_SECRET=os.environ.get("APP_SECRET")
BASE_URL = "https://openapi.ebestsec.co.kr:8080"

class ebest_api():
    def __init__(self):
        self.header=""
        self.param=""
        self.PATH=""
        self.URL=""
        self.header=""
        self.body=""
        
    def login(self):
        self.header = {"content-type": "application/x-www-form-urlencoded"}
        self.param = {
            "grant_type":"client_credentials",
            "appkey": APP_KEY,
            "appsecretkey": APP_SECRET,
            "scope": "oob",
        }
        self.PATH = "oauth2/token"
        self.URL = f"{BASE_URL}/{self.PATH}"
        request = requests.post(self.URL, verify=False, headers=self.header, data=self.param)
        ACCESS_TOKEN = request.json()["access_token"]
        return ACCESS_TOKEN
    
    def check_balance(self, ACCESS_TOKEN):
        self.PATH = "stock/accno"
        self.URL = f"{BASE_URL}/{self.PATH}"
        self.header = {  
            "content-type": "application/json; charset=utf-8", 
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "tr_cd": "CSPAQ12300", 
            "tr_cont": "N",
            "tr_cont_key": "",
        }
        self.body = {
            "CSPAQ12300InBlock1": {    
                "RecCnt": 1,    
                "BalCreTp": "0",    
                "CmsnAppTpCode": "0",    
                "D2balBaseQryTp": "0",    
                "UprcTpCode": "0"  
            }  
        }
        response = requests.post(self.URL, headers=self.header, json=self.body)
        return response.json()



ebest = ebest_api()
try:
    token = ebest.login()
    balance = ebest.check_balance(token)
    print(balance)
except Exception as e:
    print(f"An error occurred: {e}")

