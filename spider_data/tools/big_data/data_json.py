import requests
import json
from tools.headers import headers_header
from tools.big_data.record_extract import record_extract


# 数据
def data_json(matchId, home_name, away_name):
    source, lytime, deviceid, deviceaid, requestRam, sign = headers_header()
    print("数据")
    data_url = "https://mobile-gate.611.com/api/LiveDetail"
    data_data = {"MatchID": matchId, "SportType": "0", "ModeType": "13"}
    data_headers = {"source": source,
                    "lytime": lytime,
                    "deviceid": deviceid,
                    "deviceaid": deviceaid,
                    "requestRam": requestRam,
                    "sign": sign}
    rep_data = requests.post(url=data_url, data=data_data, headers=data_headers).text
    rep_data = json.loads(rep_data)
    data_list = {}
    for j in range(int(len(rep_data["data"]["modeData"]["listData"]))):
        guessSuccessData = {}
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "猜胜负":
            print("  猜胜负")
            guessSuccessData["sectionName"] = "猜胜负"
            guessSuccessData["guessSuccessData"] = rep_data["data"]["modeData"]["listData"][j]["guessSuccessData"]
            data_list["guessSuccess"] = guessSuccessData

        # pre_competition_index
        pre_competition_index = {}
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "赛前指数":
            pre_competition_index["sectionName"] = "赛前指数"
            matchOddsDatas_count = int(len(rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"]))
            print("  赛前指数", matchOddsDatas_count)
            matchOddsDatas_list = []
            for mat_count in range(matchOddsDatas_count):
                matchOddsDatas_dict = {}
                oddsName = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["oddsName"]
                indexName = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["indexName"]
                if "stHome" in rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]:
                    stHome = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["stHome"]
                else:
                    stHome = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count].setdefault(
                        "stHome", "")

                if "stFlat" in rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]:
                    stFlat = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["stFlat"]
                else:
                    stFlat = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count].setdefault(
                        "stFlat", "")

                if "stAway" in rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]:
                    stAway = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["stAway"]
                else:
                    stAway = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count].setdefault(
                        "stAway", "")
                instFlat = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["instFlat"]

                if "instAway" in rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]:
                    instAway = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count]["instAway"]
                else:
                    instAway = rep_data["data"]["modeData"]["listData"][j]["matchOddsDatas"][mat_count].setdefault(
                        "instAway", "")
                matchOddsDatas_dict["oddsName"] = oddsName
                matchOddsDatas_dict["indexName"] = indexName
                matchOddsDatas_dict["stHome"] = stHome
                matchOddsDatas_dict["stFlat"] = stFlat
                matchOddsDatas_dict["stAway"] = stAway
                matchOddsDatas_dict["instFlat"] = instFlat
                matchOddsDatas_dict["instAway"] = instAway
                matchOddsDatas_list.append(matchOddsDatas_dict)
            pre_competition_index["matchOddsDatas"] = matchOddsDatas_list
            data_list["pre_competition"] = pre_competition_index

        distribution_of_goals = {}
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "进球分布":
            leagueMatchHeader = rep_data["data"]["modeData"]["listData"][j]["leagueMatchHeader"]
            jqfb_count = int(len(leagueMatchHeader))
            if jqfb_count > 0:
                print("  进球分布", jqfb_count)
            leagueMatchHeader_list = []
            for fs_count in range(jqfb_count):
                distribution_of_goals["sectionName"] = "进球分布"
                fs_list = str(leagueMatchHeader[fs_count]).replace("'", "").replace('"', "")
                leagueMatchHeader_list.append(fs_list)
                distribution_of_goals["leagueMatchHeader"] = leagueMatchHeader_list
            distribution_of_goals["leagueMatchList"] = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]
            data_list["distribution_goals"] = distribution_of_goals

        scoreboards = {}
        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "积分榜":

            # sectionName = rep_data["data"]["modeData"]["listData"][j]["sectionName"]
            leagueMatchHeader = rep_data["data"]["modeData"]["listData"][j]["leagueMatchHeader"]
            scoreboards_data_List = []
            jf_count = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
            if jf_count > 0:
                print("  积分榜", jf_count)
            for k in range(jf_count):
                scoreboards["sectionName"] = "积分榜"
                scoreboards["leagueMatchHeader"] = leagueMatchHeader
                scoreboards_data_dict = {}
                teamId = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamId"]
                teamName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamName"]
                leagueMatchData = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k][
                    "leagueMatchData"]
                scoreboards_data_dict["teamId"] = teamId
                scoreboards_data_dict["teamName"] = teamName
                scoreboards_data_dict["leagueMatchData"] = leagueMatchData
                scoreboards_data_List.append(scoreboards_data_dict)
                scoreboards["leagueMatchList"] = scoreboards_data_List
            data_list["scoreboards"] = scoreboards

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "历史交锋":
            sectionName = "历史交锋"
            historical_exchanges = record_extract(rep_data, j, sectionName, home_name, away_name)
            data_list["historical"] = historical_exchanges

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "近期战绩":
            sectionName = "近期战绩"
            recent_achievements = record_extract(rep_data, j, sectionName, home_name, away_name)
            data_list["recentAchievements"] = recent_achievements

        if rep_data["data"]["modeData"]["listData"][j]["sectionName"] == "未来三场":
            three_next_dict = {}
            three_next_dict["sectionName"] = "未来三场"
            # sectionName = rep_data["data"]["modeData"]["listData"][j]["sectionName"]

            leagueMatchList_list = []
            wlcs_count = int(len(rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"]))
            if wlcs_count > 0:
                print("  未来三场", wlcs_count)

            for k in range(wlcs_count):
                leagueMatchList_dict = {}
                teamId = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamId"]
                teamName = rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["teamName"]
                leagueMatchList_dict["teamId"] = teamId
                leagueMatchList_dict["teamName"] = teamName
                leagueMatchList_dict["competitionDataOdds"] = \
                    rep_data["data"]["modeData"]["listData"][j]["leagueMatchList"][k]["competitionDataOdds"]
                leagueMatchList_list.append(leagueMatchList_dict)
            three_next_dict["competitionDataOdds"] = leagueMatchList_list
            data_list["three_next"] = three_next_dict
    return data_list
