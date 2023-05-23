import sys

sys.path.append("/opt/data_captureAPP")

from tools.headers_json.headers_json import headers_json
from tools.requests_api import requests_api
from tools.json_package.json_package import json_None
import math
from tools.response_api import response_api
from football_pitch_lyc.football_tools.match.gameId_w import gameId_w
from football_pitch_lyc.football_tools.match.matchId import matchId_w
from football_pitch_lyc.football_tools.match.TeamId import teamid_w


# 比赛中的列表数据
def match():
    # 准备中 type 1  进行中 type 4 已结束 type 2
    # https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php
    # json={"method":"match_match_getAllMatchesListByType","uid":5481238,"areaId":"22","page":1,"limit":10,"type":1,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"6016b31dcd44e1259eb997e11119a7c1469a3212"}
    # 已结束 type 2
    # json={"method":"match_match_getAllMatchesListByType","uid":5481238,"areaId":"22","page":1,"limit":10,"type":2,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"615f241bb7a2ffe7d27c3089a7185abb9093cb75"}
    # 进行中 type 4
    # json={"method":"match_match_getAllMatchesListByType","uid":5481238,"areaId":"22","page":1,"limit":10,"type":4,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"c702d7082f46e8dc9614e1b0b8fd692df94f83e2"}
    game_id_list = []
    matchId_list = []
    teamId_list = []
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    headers = headers_json()
    type_list = [1, 2, 4]
    for t_conut in range(int(len(type_list))):
        type_index = str(type_list[t_conut])
        data = 'json={"method":"match_match_getAllMatchesListByType","uid":5481238,"areaId":"22","page":1,"limit":10,"type":' + type_index + ',"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"615f241bb7a2ffe7d27c3089a7185abb9093cb75"}'
        rep = requests_api(url, headers, data)
        # print(rep)
        page_count = math.ceil(int(rep["matchNum"]) / 10)
        if page_count > 10:
            page_count = 10
        page = 1
        for p in range(page_count):
            data = 'json={"method":"match_match_getAllMatchesListByType","uid":5481238,"areaId":"22","page":' + str(
                page) + ',"limit":10,"type":' + type_index + ',"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"615f241bb7a2ffe7d27c3089a7185abb9093cb75"}'
            response_info = requests_api(url, headers, data)
            response_info_count = int(len(response_info["returndata"]))
            for ri_count in range(response_info_count):
                print("共有", page_count, "页,正在处理第", page, "页", "第", ri_count + 1, "条数据")
                response_info_dict = {}
                response_info_dict["type"] = type_index
                json_None(response_info["returndata"][ri_count], "gameName", "", response_info_dict)
                response_info_dict["gameName"] = str(response_info_dict["gameName"]).replace("彩票", "")
                json_None(response_info["returndata"][ri_count], "turnsName", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "fieldNumber", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "court_number_id", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "court_id", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "game_id", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "matchId", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "matchTime", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "courtName", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "homeTeamId", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "awayTeamId", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "homeName", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "awayName", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "homeIcon", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "awayIcon", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "homeScore", "", response_info_dict)
                json_None(response_info["returndata"][ri_count], "awayScore", "", response_info_dict)
                print(response_info_dict)
                game_id = response_info_dict["game_id"]
                game_id_list.append(response_info_dict["game_id"])
                matchId_list.append(response_info_dict["matchId"])
                teamId_list.append(response_info_dict["homeTeamId"])
                teamId_list.append(response_info_dict["awayTeamId"])
                print("game_id", game_id)
                bisai_url = "/lyc/save_bisai"
                response_api(bisai_url, response_info_dict)
                # print("")
            page = page + 1
    gameId_w(game_id_list)
    matchId_w(matchId_list)
    teamid_w(teamId_list)


if __name__ == '__main__':
    match()
