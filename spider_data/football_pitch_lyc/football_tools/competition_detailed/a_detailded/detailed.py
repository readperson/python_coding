import sys

sys.path.append("/opt/data_captureAPP")
from football_pitch_lyc.football_tools.competition_detailed.headers_json import headers_json
import requests
import json
from tools.json_package.json_package import json_package
from tools.ID_file.gameid_return_list import gameid_return_list
from tools.response_api import response_api


def detailed(gameId):
    url = "https://online.greenplayer.cn/E901D2019YBT/api/game/gameBasicInfo.php"
    data = 'json={"gameId":"' + str(
        gameId) + '","uid":5481238,"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"372ea54eb6b929c5c35752aa3e33f7ea79d73a75"}'
    headers = headers_json()
    response_text = requests.post(url=url, headers=headers, data=data)
    response_text.encoding = "utf-8"
    response_text = str(response_text.text).replace("﻿", "").replace("null", '""').replace("false",
                                                                                           '""')
    response_text = json.loads(response_text)
    # print("response_text",response_text)
    detailed = {}
    detailed["gameId"] = gameId
    json_package(response_text["returndata"], "gameId", "", detailed)
    json_package(response_text["returndata"], "enrollmentDeadline", "", detailed)
    json_package(response_text["returndata"], "enrollmentStartTime", "", detailed)
    json_package(response_text["returndata"], "starttime", "", detailed)
    json_package(response_text["returndata"], "endtime", "", detailed)
    json_package(response_text["returndata"], "area", "", detailed)
    json_package(response_text["returndata"], "rule_name", "", detailed)
    json_package(response_text["returndata"], "teamNumber", "", detailed)
    json_package(response_text["returndata"], "contactName", "", detailed)
    json_package(response_text["returndata"], "contactTel", "", detailed)
    possibleCourtList_count = int(len(response_text["returndata"]["possibleCourtList"]))
    for p_count in range(possibleCourtList_count):
        json_package(response_text["returndata"]["possibleCourtList"][p_count], "name", "", detailed)

    # /lyc/save_saishi_xiangxi
    url = "/lyc/save_saishi_xiangxi"
    response_api(url, detailed)
    # print(detailed)
    # return detailed


if __name__ == '__main__':
    gameID_list = gameid_return_list()
    gameid_count = int(len(gameID_list))
    for g_count in range(gameid_count):
        print("共有详细数据", gameid_count, "条，正在处理第", g_count + 1, "条数据")
        detailed(gameID_list[g_count])
