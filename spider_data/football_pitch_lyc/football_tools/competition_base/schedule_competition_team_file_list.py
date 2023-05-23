import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
from tools.requests_api import requests_api
from tools.json_package.json_package import json_package
from tools.ID_file.TeamId import teamid_w
from tools.ID_file.matchId import matchId_w
from tools.ID_file.gameId import gameId_w
import math


# 拉取 homeTeamId  awayTeamId matchId 为球队详情做准备
def lyc_competion():
    home_waay_teamId_list = []
    gameId_list = []
    matchId_list = []
    gamestatus_list = [10, 30]
    gamestatus_count = int(len(gamestatus_list))
    for g_count in range(gamestatus_count):
        gamestatus = gamestatus_list[g_count]
        url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
        data = 'json={"uid":5481238,"method":"game_common_getGameList","gameStatus":' + str(
            gamestatus) + ',"areaId":"22","condition":"","page":1,"limit":10,"sportType":"1","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"1f37caeda1c7109ef006082fb93f47d8f9e90e6c"}'
        # path_file = "../../../tools/headers_json/headers.txt"
        headers = headers_json()
        rep = requests_api(url=url, headers=headers, data=data)
        gameNum = math.ceil(int(rep["returndata"]["gameNum"]) / 10)
        # print("gameNum", gameNum)
        page = 1
        for p in range(gameNum):
            url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
            data = 'json={"uid":5481238,"method":"game_common_getGameList","gameStatus":' + str(
                gamestatus) + ',"areaId":"22","condition":"","page":' + str(
                page) + ',"limit":10,"sportType":"1","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"1f37caeda1c7109ef006082fb93f47d8f9e90e6c"}'
            path_file = "../../../tools/headers_json/headers.txt"
            rep = requests_api(url=url, headers=headers, data=data)
            rep_count = int(len(rep["returndata"]["gameList"]))
            matchList = []
            for r_c in range(rep_count):
                print("gamestatus", gamestatus, "共有", gameNum, "页,正在处理第", page, "页的第", r_c + 1, "条数据")
                base = {}
                base["status"] = "进行中"
                json_package(rep["returndata"]["gameList"][r_c], "gameId", "0", base)
                gameId = base["gameId"]

                # schedule 赛程
                schedule_url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
                schedule_data = 'json={"uid":"5481238","method":"game_common_getGameScheduleMatchListNew","gameId":"' + gameId + '","currentTurn":"","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"e4e50212571c1ac98925460598622e761f83fce6"}'
                info_schedule = requests_api(url=schedule_url, headers=headers, data=schedule_data)
                # print("info_schedule", info_schedule)
                if "returndata" in info_schedule:
                    matchList_count = int(len(info_schedule["returndata"]["matchList"]))
                else:
                    print("")
                    continue
                # print("matchList_count", matchList_count)
                for m_count in range(matchList_count):
                    matchDict = {}
                    json_package(info_schedule["returndata"]["matchList"][m_count], "homeTeamId", "0", matchDict)

                    json_package(info_schedule["returndata"]["matchList"][m_count], "awayTeamId", "0", matchDict)
                    json_package(info_schedule["returndata"]["matchList"][m_count], "gameId", "0", matchDict)
                    json_package(info_schedule["returndata"]["matchList"][m_count], "matchId", "0", matchDict)
                    matchList.append(matchDict)
                    # matchId 为观众席的动态和首页做做准备
                    matchId = str(matchDict["matchId"])
                    matchId_list.append(matchId)
                    gameId_list.append(gameId)
                    homeTeamId = str(matchDict["homeTeamId"])
                    awayTeamId = str(matchDict["awayTeamId"])
                    if homeTeamId != "null":
                        if homeTeamId != "None":
                            if homeTeamId != "-1":
                                home_waay_teamId_list.append(homeTeamId)
                    if awayTeamId != "null":
                        if awayTeamId != "None":
                            if awayTeamId != "-1":
                                home_waay_teamId_list.append(awayTeamId)
                # print("json:", str(base).replace("'", '"'))
            page = page + 1
    matchId_w(matchId_list)
    teamid_w(home_waay_teamId_list)
    gameId_w(gameId_list)


if __name__ == '__main__':
    lyc_competion()
