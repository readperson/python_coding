from tools.requests_api import requests_api
from tools.json_package.json_package import json_package

# 球员积分 球员积分榜
def player_accumulate_points(headers, data):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    rep = requests_api(url=url, headers=headers, data=data)
    player_accumulate_points_list = []
    player_accumulate_points_count = int(len(rep["returndata"]))
    for pap_count in range(player_accumulate_points_count):
        player_accumulate_points_dict = {}
        json_package(rep["returndata"][pap_count], "UserId", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "TeamId", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "totalCount", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "dian", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "scoreNum", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "assistNum", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "redCard", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "yellowCard", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "playerName", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "portrait", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "teamname", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "teamIcon", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "credit", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "totalMatches", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "rank", "", player_accumulate_points_dict)
        json_package(rep["returndata"][pap_count], "playerNumber", "", player_accumulate_points_dict)
        player_accumulate_points_dict["portrait"] = ""
        player_accumulate_points_list.append(player_accumulate_points_dict)
    # print(player_accumulate_points_list)
    return player_accumulate_points_list


if __name__ == '__main__':
    gameId = "33426"
    data = 'json={"method":"match_player_getGameMatchPlayerListByTeamId","uid":5481238,"gameId":"' + gameId + '","teamId":"","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"3bb0892eed713e4ab64776556c29fba22182db50"}'
    headers = {'Host': 'online.greenplayer.cn', 'Connection': 'close', 'Accept': 'application/json,text/plain,*/*',
               'Origin': 'https',
               'User-Agent': 'Dalvik/2.1.0(Linux;U;Android5.1.1;HMA-AL00Build/LMY48Z)/GreenAppVersionCode=85/GreenAppVersionName=8.5.1_Android',
               'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https',
               'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,en-US;q=0.8',
               'X-Requested-With': 'cn.greenplayer.zuqiuke'}
    player_accumulate_points(headers, data)
