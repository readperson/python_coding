import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
from tools.requests_api import requests_api
from tools.json_package.json_package import json_package
import requests
import json
from tools.response_api import response_api


# 比赛报名中
def competition_registration():
    url = "https://online.greenplayer.cn/E901D2019YBT/api/common/baseApiEntry.php"
    headers = headers_json()
    data = 'json={"uid":5481238,"method":"game_common_getGameList","gameStatus":1,"areaId":"22","condition":"","page":1,"limit":10,"sportType":"1","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"0319d4eaaf6b48c1aef68c5fe2987b2ec582601e"}'
    response_text = requests_api(url=url, headers=headers, data=data)
    # print(response_text)
    response_count = int(len(response_text["returndata"]["gameList"]))
    for re_count in range(response_count):
        response_dict = {}
        json_package(response_text["returndata"], "gameNum", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "gameId", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "gamename", "", response_dict)
        response_dict["gamename"] = str(response_dict["gamename"]).replace("彩票", "")
        json_package(response_text["returndata"]["gameList"][re_count], "teamnumber", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "starttime", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "portrait", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "gametype", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "game_status", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "roundRobin", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "ruleName", "", response_dict)
        json_package(response_text["returndata"]["gameList"][re_count], "teamNum", "", response_dict)
        teamList_count = int(len(response_text["returndata"]["gameList"][re_count]["teamList"]))
        team_list = []
        for t_count in range(teamList_count):
            team_dict = {}
            json_package(response_text["returndata"]["gameList"][re_count]["teamList"][t_count], "teamId", "",
                         team_dict)
            json_package(response_text["returndata"]["gameList"][re_count]["teamList"][t_count], "teamName", "",
                         team_dict)
            json_package(response_text["returndata"]["gameList"][re_count]["teamList"][t_count], "portrait", "",
                         team_dict)
            team_list.append(team_dict)
        response_dict["teamList"] = team_list

        #
        gameId = response_dict["gameId"]
        detailed_url = "https://online.greenplayer.cn/E901D2019YBT/api/game/gameBasicInfo.php"
        detailed_data = 'json={"uid":5481238,"gameId":"' + gameId + '","version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"498c32270f89e2957c960325a1743f65a118c7a5"}'
        response_detailed = requests.post(url=detailed_url, headers=headers, data=detailed_data)
        response_detailed.encoding = "utf-8"
        response_detailed = json.loads(response_detailed.text.replace("﻿", ""))
        # print(response_detailed)
        response_detailed_dict = {}
        json_package(response_detailed["returndata"], "portrait", "", response_detailed_dict)
        json_package(response_detailed["returndata"], "gamename", "", response_detailed_dict)
        response_detailed_dict["gamename"] = str(response_detailed_dict["gamename"]).replace("彩票", "")
        json_package(response_detailed["returndata"], "rule_name", "", response_detailed_dict)
        json_package(response_detailed["returndata"], "teamNumber", "", response_detailed_dict)
        basic_document = {}
        json_package(response_detailed["returndata"], "starttime", "", basic_document)
        json_package(response_detailed["returndata"], "endtime", "", basic_document)
        json_package(response_detailed["returndata"], "contactName", "", basic_document)
        json_package(response_detailed["returndata"], "contactTel", "", basic_document)
        # possibleCourtList
        possibleCourtList_count = int(len(response_detailed["returndata"]["possibleCourtList"]))
        possibleCourtList_list = []
        for pl_count in range(possibleCourtList_count):
            possibleCourtList_dict = {}
            json_package(response_detailed["returndata"]["possibleCourtList"][pl_count], "name", '',
                         possibleCourtList_dict)
            json_package(response_detailed["returndata"]["possibleCourtList"][pl_count], "address", '',
                         possibleCourtList_dict)
            possibleCourtList_list.append(possibleCourtList_dict)
        basic_document["possibleCourtList"] = possibleCourtList_list
        basic_document["sponsor"] = response_detailed["returndata"]["sponsor"]
        basic_document["coSponsor"] = response_detailed["returndata"]["coSponsor"]
        basic_document["contractor"] = response_detailed["returndata"]["contractor"]
        response_detailed_dict["basic_document"] = basic_document

        registration_team_count = int(len(response_detailed["returndata"]["enrollmentList"]))
        registration_team_list = []
        for t_count in range(registration_team_count):
            registration_team_dict = {}
            json_package(response_detailed["returndata"]["enrollmentList"][t_count], "teamName", "",
                         registration_team_dict)
            json_package(response_detailed["returndata"]["enrollmentList"][t_count], "teamId", "",
                         registration_team_dict)
            json_package(response_detailed["returndata"]["enrollmentList"][t_count], "icon", "", registration_team_dict)
            json_package(response_detailed["returndata"]["enrollmentList"][t_count], "status", "",
                         registration_team_dict)
            registration_team_list.append(registration_team_dict)
        response_detailed_dict["registration_team"] = registration_team_list

        response_dict["detailed"] = response_detailed_dict
        url = "/lyc/save_baomingzhong"
        response_api(url, response_dict)

        # print("json", str(response_dict).replace("'", '"'))


if __name__ == '__main__':
    competition_registration()
