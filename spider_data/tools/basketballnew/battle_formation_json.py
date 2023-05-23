from tools.headers import headers_header
import json
import requests
from tools.response_api import response_api

# 阵容
def battle_formation(matchId):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    data_url = "https://mobile-gate.611.com/api/LiveDetail"
    # MatchID=303490581&SportType=0&ModeType=11&minTime=
    data_data = {"MatchID": matchId, "SportType": "1", "ModeType": "11", "minTime": ""}
    data_headers = {"source": source,
                    "lytime": lytime,
                    "deviceid": deviceid,
                    "deviceaid": deviceaid,
                    "requestRam": requestRam,
                    "sign": sign}
    rep_data = requests.post(url=data_url, data=data_data, headers=data_headers).text
    rep_data = json.loads(rep_data)
    # print("阵容 ", len(rep_data["data"]["modeData"]["listData"]))
    data_dict = {}
    data_dict["matchId"] = matchId
    data_dict["listData"] = rep_data["data"]["modeData"]["listData"]
    # print("阵容:", data_dict)
    response_api("/leyulanqiu/save_zhenrong",data_dict)

if __name__ == '__main__':
    battle_formation(str(303490581))
