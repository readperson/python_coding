import sys

sys.path.append("/opt/data_captureAPP")
from tools.headers_json.headers_json import headers_json
import requests
import json
from tools.json_package.json_package import json_package
from tools.ID_file.matchid_return_list import matchid_return_list
from tools.response_api import response_api


# 事件返回一个list matchId
def team_event(matchId):
    eventInfo = {}
    headers = headers_json()
    url = "https://online.greenplayer.cn/E901D2019YBT/api/match/loadMatchAllPartEventList.php"

    data = 'json={"uid":5481238,"matchId":' + matchId + ',"version":"h5 1.0.0","secretkey":"9c64c5c81e0b0ab03eeac45cf565a32d90f142f1","token":"a8125e0b7064299c98e1f2d64daec26019fd0eb6","sign":"78165b331c14f5ca0cdf83f8a634ca76fd01bbfe"}'
    response_event = requests.post(url=url, headers=headers, data=data)
    response_event.encoding = "utf-8"
    response_event = json.loads(response_event.text.replace("﻿", ""))
    # print("response_event", response_event)
    response_event_count = int(len(response_event["returndata"]))
    for rep_count in range(response_event_count):
        eventInfo_count = int(len(response_event["returndata"][rep_count]["eventInfo"]))
        eventInfo_list = []
        for e_count in range(eventInfo_count):
            eventInfo_dict = {}
            json_package(response_event["returndata"][rep_count]["eventInfo"][e_count], "eventId", "", eventInfo_dict)
            json_package(response_event["returndata"][rep_count]["eventInfo"][e_count], "teamId", "", eventInfo_dict)
            json_package(response_event["returndata"][rep_count]["eventInfo"][e_count], "AddTime", "", eventInfo_dict)
            json_package(response_event["returndata"][rep_count]["eventInfo"][e_count], "HappenTime", "",
                         eventInfo_dict)

            playerList_count = int(len(response_event["returndata"][rep_count]["eventInfo"][e_count]["playerList"]))
            player_List = []
            for p_count in range(playerList_count):
                player_dict = {}
                json_package(response_event["returndata"][rep_count]["eventInfo"][e_count]["playerList"][p_count],
                             "playerName", "", player_dict)
                json_package(response_event["returndata"][rep_count]["eventInfo"][e_count]["playerList"][p_count],
                             "playerPortrait", "", player_dict)
                json_package(response_event["returndata"][rep_count]["eventInfo"][e_count]["playerList"][p_count],
                             "memberNumber", "", player_dict)
                player_dict["playerName"] = str(player_dict["playerName"]).replace("None", "")
                player_dict["memberNumber"] = str(player_dict["memberNumber"]).replace("None", "")
                player_List.append(player_dict)
            eventInfo_dict["playerList"] = player_List
            eventInfo_list.append(eventInfo_dict)
        eventInfo["matchId"] = matchId
        eventInfo["eventInfo_list"] = eventInfo_list
        url_event = "/lyc/save_shijian"
        response_api(url_event, eventInfo)
        # return eventInfo


if __name__ == '__main__':
    matchId_list = matchid_return_list()
    print(int(len(matchId_list)))
    for m_index in range(int(len(matchId_list))):
        print("共有事件数据：", int(len(matchId_list)), "条", "正在处理", m_index + 1, "条")
        matchId = matchId_list[m_index]
        # print(matchId)
        team_event(matchId)
        # print(te)
