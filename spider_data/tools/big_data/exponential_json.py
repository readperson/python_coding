from tools.headers import headers_header
import json
import requests
from tools.big_data.exponential_extract import *

# 指数
def exponential_json(matchId, home_name, away_name):
    exponential_list = {}
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    print("指数")
    # 亚盘
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
    # print("rep_data------", rep_data)
    if "oddsHeader" in  rep_data["data"]:
        asia_pacific = exponential_extract(rep_data, "亚盘")
        exponential_list["asia_pacific"] = asia_pacific

        # 球大小 ball_size
        data_ball_size = {"matchId": matchId, "sectionType": "18", "sportType": "0"}
        data_ball_size = requests.post(url=data_url, data=data_ball_size, headers=data_headers).text
        data_ball_size = json.loads(data_ball_size)
        ball_size = exponential_extract(data_ball_size, "球大小")
        exponential_list["ball_size"] = ball_size

        # 欧赔 european_compensation
        data_european_compensation = {"matchId": matchId, "sectionType": "16", "sportType": "0"}
        data_european_compensation = requests.post(url=data_url, data=data_european_compensation, headers=data_headers).text
        data_european_compensation = json.loads(data_european_compensation)

        oddsOtAvgList_count = int(len(data_european_compensation["data"]["oddsOtAvgList"]))
        oddsOtAvgList = []
        for oddAvg_count in range(oddsOtAvgList_count):
            oddsOtAvgDict = {}
            name = data_european_compensation["data"]["oddsOtAvgList"][oddAvg_count]["name"]
            highNum = data_european_compensation["data"]["oddsOtAvgList"][oddAvg_count]["highNum"]
            lowNum = data_european_compensation["data"]["oddsOtAvgList"][oddAvg_count]["lowNum"]
            avgNum = data_european_compensation["data"]["oddsOtAvgList"][oddAvg_count]["avgNum"]
            avgNumRiseOrfall = data_european_compensation["data"]["oddsOtAvgList"][oddAvg_count]["avgNumRiseOrfall"]
            oddsOtAvgDict["name"] = name
            oddsOtAvgDict["highNum"] = highNum
            oddsOtAvgDict["lowNum"] = lowNum
            oddsOtAvgDict["avgNum"] = avgNum
            oddsOtAvgDict["avgNumRiseOrfall"] = avgNumRiseOrfall
            oddsOtAvgList.append(oddsOtAvgDict)
        # print("oddsOtAvgList",oddsOtAvgList)

        indexOtAvgList_count = int(len(data_european_compensation["data"]["oddsAvgList"]))
        indexOtAvgList = []
        for indexAvg_count in range(indexOtAvgList_count):
            indexOtAvgDict = {}
            name = data_european_compensation["data"]["oddsAvgList"][indexAvg_count]["name"]
            highNum = data_european_compensation["data"]["oddsAvgList"][indexAvg_count]["highNum"]
            lowNum = data_european_compensation["data"]["oddsAvgList"][indexAvg_count]["lowNum"]
            avgNum = data_european_compensation["data"]["oddsAvgList"][indexAvg_count]["avgNum"]
            avgNumRiseOrfall = data_european_compensation["data"]["oddsAvgList"][indexAvg_count]["avgNumRiseOrfall"]
            indexOtAvgDict["name"] = name
            indexOtAvgDict["highNum"] = highNum
            indexOtAvgDict["lowNum"] = lowNum
            indexOtAvgDict["avgNum"] = avgNum
            indexOtAvgDict["avgNumRiseOrfall"] = avgNumRiseOrfall
            indexOtAvgList.append(indexOtAvgDict)
        # print("indexOtAvgList",indexOtAvgList)

        european_compensation = exponential_extract_european_compensation(data_european_compensation, "欧赔", oddsOtAvgList,
                                                                          indexOtAvgList)
        exponential_list["european_compensation"] = european_compensation

        return exponential_list
