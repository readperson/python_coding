from tools.requests_api import requests_api
from tools.json_package.json_package import json_package


def hot_ballGame(gameId, headers):
    # 热度 球队 gameId
    hot = {}
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    data = 'json={"method":"game_heat_getGameHeatIdentityDataList","gameId":"' + gameId + '","type":2,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"5bcf0a8e119140ef95785e555585296df1e226dc"}'
    rep = requests_api(url=url, headers=headers, data=data)
    ballgame = str(rep["returndata"]["dataList"])
    if ballgame != "None":
        if "dataList" in rep["returndata"]:
            hot_BallGame_count = int(len(rep["returndata"]["dataList"]))
            hot_BallGame_list = []
            for hb_count in range(hot_BallGame_count):
                hot_BallGame_dict = {}
                json_package(rep["returndata"]["dataList"][hb_count], "concernNumber", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "identityId", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "identityName", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "portrait", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "isVote", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "totalHot", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "ticketNumber", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "browseNumber", "0", hot_BallGame_dict)
                json_package(rep["returndata"]["dataList"][hb_count], "rank", "0", hot_BallGame_dict)
                hot_BallGame_list.append(hot_BallGame_dict)
            hot["hot_ballGame"] = hot_BallGame_list
        else:
            hot["hot_ballGame"] = []
    else:
        hot["hot_ballGame"] = []
    # 热度 球员 gameId
    data_player = 'json={"method":"game_heat_getGameHeatIdentityDataList","gameId":"' + gameId + '","type":1,"version":"h5 1.0.0","uid":"5481238","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"b7cec4a42a679d044834acacd2791245ff17b37c"}'
    rep_player = requests_api(url=url, headers=headers, data=data_player)
    player = str(rep_player["returndata"]["dataList"])
    if player != "None":
        if "dataList" in rep_player["returndata"]:
            player_count = int(len(rep_player["returndata"]["dataList"]))
            hot_player_list = []
            for p_count in range(player_count):
                hot_player_dict = {}
                json_package(rep_player["returndata"]["dataList"][p_count], "concernNumber", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "teamId", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "identityId", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "identityName", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "portrait", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "isVote", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "totalHot", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "ticketNumber", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "browseNumber", "0", hot_player_dict)
                json_package(rep_player["returndata"]["dataList"][p_count], "rank", "0", hot_player_dict)
                hot_player_dict["portrait"] = ""
                hot_player_list.append(hot_player_dict)
            hot["hot_player"] = hot_player_list
        else:
            hot["hot_player"] = []
    else:
        hot["hot_player"] = []
    # print(hot)
    return hot

if __name__ == '__main__':
    gameId = "33426"
    headers = {'Host': 'online.greenplayer.cn', 'Connection': 'close', 'Accept': 'application/json,text/plain,*/*',
               'Origin': 'https',
               'User-Agent': 'Dalvik/2.1.0(Linux;U;Android5.1.1;HMA-AL00Build/LMY48Z)/GreenAppVersionCode=85/GreenAppVersionName=8.5.1_Android',
               'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https',
               'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
               'X-Requested-With': 'cn.greenplayer.zuqiuke'}
    hot_ballGame(gameId,headers)

