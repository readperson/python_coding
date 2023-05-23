import sys
sys.path.append("/opt/data_captureAPP")
import requests
import json
from tools.headers import headers_header
from tools.random_number import random_color_list
from tools.time_treatment import now_time
from tools.basketball.data_json import data_json
from tools.basketball.chat_json import chat_json
from tools.basketball.events_json import events_json
from tools.response_api import response_api
from tools.random_number import random_beginTime
from tools.base_count import base_count
import datetime

def amidithion_basketball():
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    nowtime = (datetime.datetime.now() + datetime.timedelta(minutes=-10)).strftime("%Y-%m-%d %H:%M:%S")
    url_base = "https://mobile-gate.611.com/api/LiveScoreMatches"
    data_base = {"sportType": "1", "date": nowtime, "minTime": "", "LiveScoreType": "0"}
    headers_base = {"source": source,
               "lytime": lytime,
               "deviceid": deviceid,
               "deviceaid": deviceaid,
               "requestRam": requestRam,
               "sign": sign}

    rep = requests.post(url=url_base, data=data_base, headers=headers_base).text
    rep = json.loads(rep)
    count = len(rep["data"])
    be_count = base_count(int(count))
    base_info_list = []
    for i in range(be_count):

        base = {}
        home = {}
        away = {}
        base_info_dict = {}

        competetionShortName = rep["data"][i]["competetionShortName"]
        beginTime = rep["data"][i]["beginTime"]
        matchId = str(rep["data"][i]["matchId"])
        matchDate = rep["data"][i]["matchDate"]
        status = rep["data"][i]["status"]

        base["competetionShortName"] = competetionShortName
        base["beginTime"] = str(beginTime)[2:]
        base["matchId"] = matchId
        base["status"] = str(status)
        base["matchDate"] = matchDate
        # competition_status 2 赛果
        base["competition_status"] = "2"
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
        home_id = rep["data"][i]["home"]["id"]
        base["come_from"] = "乐鱼体育"
        base["capture_time"] = now_time()
        base["capture_type"] = "篮球"
        home_name = rep["data"][i]["home"]["name"]
        home_zhtName = rep["data"][i]["home"]["zhtName"]
        home_enName = str(rep["data"][i]["home"]["enName"]).replace("'"," ").replace('"'," ")
        home_logo = rep["data"][i]["home"]["logo"]
        home_score = str(rep["data"][i]["home"]["score"])
        home_btbScore = rep["data"][i]["home"]["btbScore"]
        home["id"] = home_id
        home["name"] = home_name
        home["zhtName"] = home_zhtName
        home["enName"] = home_enName
        home["logo"] = home_logo
        home["score"] = home_score
        home["btbScore"] = home_btbScore
        base["home"] = home

        away_id = rep["data"][i]["away"]["id"]
        away_name = rep["data"][i]["away"]["name"]
        away_zhtName = rep["data"][i]["away"]["zhtName"]
        away_enName = str(rep["data"][i]["away"]["enName"]).replace("'"," ").replace('"'," ")
        away_logo = rep["data"][i]["away"]["logo"]
        away_score = str(rep["data"][i]["away"]["score"])
        away_btbScore = rep["data"][i]["away"]["btbScore"]

        away["id"] = away_id
        away["name"] = away_name
        away["zhtName"] = away_zhtName
        away["enName"] = away_enName
        away["logo"] = away_logo
        away["score"] = away_score
        away["btbScore"] = away_btbScore
        base["away"] = away
        i = i + 1
        base_info = str(base).replace("'",'"')
        base_info_dict["base_info"+str(1)] = base_info
        base_info_list.append(base_info_dict)
        print("共[", be_count, "]条数据,正在处理第[", i, "]条数据", "处理时间[", now_time(), "]")
        print("主：", home_name, "客：", away_name)

        # 数据处理
        base["competition_data"] = data_json(matchId, home_name, away_name)

        # 聊天处理
        base["chat"] = chat_json(matchId)

        # 赛况处理
        base["events"] = events_json(matchId)

        url_tj = "/basketball/save_competetion_data"
        response_api(url_tj, base)


if __name__ == '__main__':
    amidithion_basketball()
