from tools.headers import headers_header
import json
import requests
from tools.big_data.exponential_extract import *
from tools.response_api import response_api


# 指数 MatchID=303580977&SportType=1&ModeType=7&minTime=
def exponential_json(matchId, home_name, away_name):
    exponential_list = {}
    exponential_list["matchId"] = matchId
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    # matchId=303496801&sectionType=17&sportType=0
    data_url = "https://mobile-gate.611.com/api/LiveMatchOdds"
    data_data = {"matchId": matchId, "sectionType": "17", "sportType": "0"}
    data_headers = {"source": source,
                    "lytime": lytime,
                    "deviceid": deviceid,
                    "deviceaid": deviceaid,
                    "requestRam": requestRam,
                    "sign": sign}
    rep_data = requests.post(url=data_url, data=data_data, headers=data_headers).text
    rep_data = json.loads(rep_data)
    exponential = {}
    exponential["matchId"] = matchId
    exponential["exponential"] = rep_data["data"]
    # print("指数", exponential)
    response_api("/leyuzuqiu/save_zhishu", exponential)
