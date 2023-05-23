import requests
import json
from tools.json_package.json_package import json_package


# 纪律榜
def discipline_list(headers, data):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/game/loadGamePunishRankList.php"
    rep = requests.post(url=url, headers=headers, data=data)
    rep.encoding = "utf-8"
    rep = rep.text.replace("﻿", "")
    rep = json.loads(rep)
    # print(rep)
    rep_count = int(len(rep["returndata"]))
    disciplineList = []
    for r_count in range(rep_count):
        disciplineDict = {}
        json_package(rep["returndata"][r_count], "teamId", "", disciplineDict)
        json_package(rep["returndata"][r_count], "teamName", "", disciplineDict)
        json_package(rep["returndata"][r_count], "teamIcon", "", disciplineDict)
        json_package(rep["returndata"][r_count], "totalRedCard", "", disciplineDict)
        json_package(rep["returndata"][r_count], "totalYellowCard", "", disciplineDict)
        json_package(rep["returndata"][r_count], "deductPoints", "", disciplineDict)
        players_count = int(len(rep["returndata"][r_count]["players"]))
        players_list = []
        for p_count in range(players_count):
            players_dict = {}
            json_package(rep["returndata"][r_count]["players"][p_count], "uid", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "userName", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "playerNumber", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "userIcon", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "RedCard", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "YellowCard", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "suspendMatches", "", players_dict)
            json_package(rep["returndata"][r_count]["players"][p_count], "suspendCount", "", players_dict)
            players_dict["userIcon"] = ""
            players_list.append(players_dict)
        disciplineDict["players"] = players_list
        disciplineList.append(disciplineDict)
    # print(disciplineList)
    return disciplineList

    # ss = rep["returndata"][r_count]
    # print(ss)


if __name__ == '__main__':
    gameId = "33426"
    data = 'json={"gameId":"' + gameId + '","orderType":"1","version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"061d5798459f7dab2937971d1172c8689a817f79"}'
    headers = {'Host': 'online.greenplayer.cn', 'Connection': 'close', 'Accept': 'application/json,text/plain,*/*',
               'Origin': 'https',
               'User-Agent': 'Dalvik/2.1.0(Linux;U;Android5.1.1;HMA-AL00Build/LMY48Z)/GreenAppVersionCode=85/GreenAppVersionName=8.5.1_Android',
               'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https',
               'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
               'X-Requested-With': 'cn.greenplayer.zuqiuke'}
    discipline_list(headers, data)
