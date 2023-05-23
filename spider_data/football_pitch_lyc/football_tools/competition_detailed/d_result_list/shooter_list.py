import requests
import json
from tools.json_package.json_package import json_package


# 射手榜
def shooter_list(headers, data):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/game/loadGameScoreRankList.php"
    rep = requests.post(url=url, headers=headers, data=data)
    rep.encoding = "utf-8"
    rep = rep.text.replace("﻿", "")
    rep = json.loads(rep)
    rep_count = int(len(rep["returndata"]))
    shooterList = []
    # print(rep)
    for r_count in range(rep_count):
        shooterDict = {}
        json_package(rep["returndata"][r_count], "rank", "", shooterDict)
        json_package(rep["returndata"][r_count], "uid", "", shooterDict)
        json_package(rep["returndata"][r_count], "userName", "", shooterDict)
        json_package(rep["returndata"][r_count], "userIcon", "", shooterDict)
        json_package(rep["returndata"][r_count], "playerNumber", "", shooterDict)
        json_package(rep["returndata"][r_count], "teamId", "", shooterDict)
        json_package(rep["returndata"][r_count], "teamName", "", shooterDict)
        json_package(rep["returndata"][r_count], "teamIcon", "", shooterDict)
        json_package(rep["returndata"][r_count], "totalScore", "", shooterDict)
        json_package(rep["returndata"][r_count], "reserved", "", shooterDict)
        shooterDict["userIcon"] = ""
        shooterList.append(shooterDict)
    return shooterList


if __name__ == '__main__':
    gameId = "33426"
    data = 'json={"gameId":"' + gameId + '","rankType":1,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"81f4862645b5ca0d9568c62c87f469fa8e23c80e"}'
    headers = {'Host': 'online.greenplayer.cn', 'Connection': 'close', 'Accept': 'application/json,text/plain,*/*',
               'Origin': 'https',
               'User-Agent': 'Dalvik/2.1.0(Linux;U;Android5.1.1;HMA-AL00Build/LMY48Z)/GreenAppVersionCode=85/GreenAppVersionName=8.5.1_Android',
               'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https',
               'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
               'X-Requested-With': 'cn.greenplayer.zuqiuke'}
    print(shooter_list(headers, data))
