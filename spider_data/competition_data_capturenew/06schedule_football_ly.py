import sys

sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.headers import headers_header
from tools.footballnew.data_json import data_json
from tools.footballnew.chat_json import chat_json
from tools.footballnew.events_json import event_json
from tools.footballnew.battle_formation_json import battle_formation
from tools.footballnew.exponential_json import exponential_json
from tools.random_number import random_color_list
from tools.time_treatment import now_time
from tools.response_api import response_api
from tools.base_count import base_count
import datetime


def immediately_footall():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowtime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    url = "https://mobile-gate.611.com/api/LiveScoreMatches"
    data = {"sportType": "0", "date": nowtime, "minTime": "", "LiveScoreType": "1"}
    headers = {"source": source,
               "lytime": lytime,
               "deviceid": deviceid,
               "deviceaid": deviceaid,
               "requestRam": requestRam,
               "sign": sign}

    rep = requests.post(url=url, data=data, headers=headers).text
    rep = json.loads(rep)
    print(rep["data"])
    count = len(rep["data"])
    be_count = base_count(int(count))
    for i in range(be_count):
        base = {}
        home = {}
        away = {}
        matchId = rep["data"][i]["matchId"]
        base["matchId"] = str(matchId)
        base["matchDate"] = rep["data"][i]["matchDate"]
        base["competetionId"] = rep["data"][i]["competetionId"]
        base["status"] = str(rep["data"][i]["status"])
        base["competetionShortName"] = rep["data"][i]["competetionShortName"]
        base["beginTime"] = str(rep["data"][i]["beginTime"])[2:]
        base["half"] = rep["data"][i]["half"]
        base["competition_status"] = "3"

        if "oddsInfo" in rep["data"][i]:
            oddsInfo = rep["data"][i]["oddsInfo"]
            oddsInfo["isSeal"] = "false"
        else:
            oddsInfo = {}

        if "euOddsInfo" in rep["data"][i]:
            euOddsInfo = rep["data"][i]["euOddsInfo"]
            euOddsInfo["isSeal"] = "false"
        else:
            euOddsInfo = {}

        if "ballOddsInfo" in rep["data"][i]:
            ballOddsInfo = rep["data"][i]["ballOddsInfo"]
            ballOddsInfo["isSeal"] = "false"
        else:
            ballOddsInfo = {}

        base["oddsInfo"] = oddsInfo
        base["euOddsInfo"] = euOddsInfo
        base["ballOddsInfo"] = ballOddsInfo

        base["color"] = random_color_list()
        base["come_from"] = "乐鱼体育"
        base["capture_time"] = now_time()
        base["capture_type"] = "足球"
        home["id"] = rep["data"][i]["home"]["id"]
        home_name = rep["data"][i]["home"]["name"]
        home["name"] = home_name
        home["zhtName"] = rep["data"][i]["home"]["zhtName"]
        if "enName" in rep["data"][i]["home"]:
            home["enName"] = str(rep["data"][i]["home"]["enName"]).replace('"', " ")
        else:
            home["enName"] = rep["data"][i]["home"].setdefault("enName", "")

        home["logo"] = rep["data"][i]["home"]["logo"]
        home["score"] = str(rep["data"][i]["home"]["score"])
        home["corner"] = str(rep["data"][i]["home"]["corner"])
        if "rank" in rep["data"][i]["home"]:
            home["rank"] = str(rep["data"][i]["home"]["rank"])
        else:
            home["rank"] = str(rep["data"][i]["home"].setdefault("rank", ""))
        base["home"] = home

        away["id"] = rep["data"][i]["away"]["id"]
        away_name = rep["data"][i]["away"]["name"]
        away["name"] = away_name
        away["zhtName"] = rep["data"][i]["away"]["zhtName"]

        if "enName" in rep["data"][i]["away"]:
            away["enName"] = str(rep["data"][i]["away"]["enName"]).replace('"', " ")
        else:
            away["enName"] = rep["data"][i]["away"].setdefault("enName", "")

        away["logo"] = rep["data"][i]["away"]["logo"]
        away["score"] = str(rep["data"][i]["away"]["score"])
        away["corner"] = str(rep["data"][i]["away"]["corner"])
        if "rank" in rep["data"][i]["away"]:
            away["rank"] = str(rep["data"][i]["away"]["rank"])
        else:
            away["rank"] = str(rep["data"][i]["away"].setdefault("rank", ""))
        base["away"] = away

        print("共", be_count, "条数据,正在处理第", i + 1, "条数据", "处理时间", now_time())
        print("主", rep["data"][i]["home"]["name"], "客", rep["data"][i]["away"]["name"])

        print("base:", base)
        # 聊天处理
        # chat_json(matchId)
        # 赛况处理
        event_json(matchId)
        # 数据处理
        data_json(matchId, home_name, away_name)
        # 阵容
        battle_formation(matchId)
        # 指数
        exponential_json(matchId, home_name, away_name)

        response_api("/leyuzuqiu/save_jichuxinxi", base)


if __name__ == '__main__':
    immediately_footall()
